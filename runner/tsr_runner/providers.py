"""Provider-neutral model access with a full call log (spec section 3).

Every call is appended to <run_dir>/calls.jsonl as
  {ts, role, model, provider, temperature, prompt_sha256, prompt_chars, response, error}
so a run can be replayed from the log without touching a provider.

Providers (no third-party SDKs; urllib only):
  openai_compat : OpenAI, Mistral, Groq, Together, vLLM / Ollama / llama.cpp local endpoints
  anthropic     : Anthropic Messages API
  google        : Gemini generateContent
  replay        : answers from a previous run's calls.jsonl, keyed by prompt hash
  mock          : deterministic, schema-valid output derived from the record (pipeline tests only;
                  never a real run and labelled as such in every artifact)
"""
from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass
class ModelSpec:
    name: str                # e.g. "gpt-4.1", "claude-sonnet-4-5", "gemini-2.5-pro", "mistral-large", "qwen3:32b"
    provider: str            # openai_compat | anthropic | google | mock | replay
    vendor: str              # for the "≥ 3 vendors" gate: openai | anthropic | google | mistral | open-weights | ...
    base_url: str = ""
    api_key_env: str = ""
    open_weights: bool = False


class Provider(Protocol):
    def complete(self, prompt: str, model: str, temperature: float, max_tokens: int = 4000) -> str: ...


def sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


class CallLog:
    def __init__(self, run_dir: Path):
        self.path = Path(run_dir) / "calls.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, **rec):
        rec["ts"] = time.time()
        with open(self.path, "a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    def load(self) -> dict[tuple[str, str, float], str]:
        out = {}
        if not self.path.exists():
            return out
        with open(self.path) as f:
            for line in f:
                r = json.loads(line)
                if r.get("response") is not None:
                    out[(r["prompt_sha256"], r["model"], float(r["temperature"]))] = r["response"]
        return out


# ---------------------------------------------------------------------------
class OpenAICompat:
    def __init__(self, base_url: str = "https://api.openai.com/v1", api_key_env: str = "OPENAI_API_KEY"):
        self.base_url = base_url.rstrip("/")
        self.key = os.environ.get(api_key_env, "")

    def complete(self, prompt, model, temperature, max_tokens=4000):
        body = {"model": model, "temperature": temperature, "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}]}
        req = urllib.request.Request(f"{self.base_url}/chat/completions", data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json",
                                              "Authorization": f"Bearer {self.key}"})
        with urllib.request.urlopen(req, timeout=300) as r:
            d = json.load(r)
        return d["choices"][0]["message"]["content"]


class Anthropic:
    def __init__(self, api_key_env: str = "ANTHROPIC_API_KEY"):
        self.key = os.environ.get(api_key_env, "")

    def complete(self, prompt, model, temperature, max_tokens=4000):
        body = {"model": model, "temperature": temperature, "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}]}
        req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json", "x-api-key": self.key,
                                              "anthropic-version": "2023-06-01"})
        with urllib.request.urlopen(req, timeout=300) as r:
            d = json.load(r)
        return "".join(b.get("text", "") for b in d["content"])


class Google:
    def __init__(self, api_key_env: str = "GOOGLE_API_KEY"):
        self.key = os.environ.get(api_key_env, "")

    def complete(self, prompt, model, temperature, max_tokens=4000):
        body = {"contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens}}
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.key}"
        req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=300) as r:
            d = json.load(r)
        return "".join(p.get("text", "") for p in d["candidates"][0]["content"]["parts"])


class Replay:
    def __init__(self, log: CallLog):
        self.cache = log.load()

    def complete(self, prompt, model, temperature, max_tokens=4000):
        key = (sha(prompt), model, float(temperature))
        if key not in self.cache:
            raise KeyError(f"no logged response for {model} @ {temperature} prompt {key[0][:12]}")
        return self.cache[key]


class Mock:
    """Deterministic stand-in so the pipeline can be exercised end to end without a provider.

    It answers from a side-channel of procedure decisions (set by generate.py for mock runs
    only; real prompts never carry the decision), so it is useful only for plumbing tests.
    Every artifact produced from a Mock run is stamped MOCK.
    """
    decisions: dict[str, dict] = {}
    decoy_key: dict[str, dict] = {}

    def __init__(self, flavour: str = "agree"):
        self.flavour = flavour  # agree | dissent | leak

    @staticmethod
    def _record_id(prompt: str) -> str | None:
        import re
        m = re.search(r'"id":\s*"([^"]+)"', prompt)
        return m.group(1) if m else None

    def complete(self, prompt, model, temperature, max_tokens=4000):
        if "ROLE: judge" in prompt:
            return json.dumps({"verdict": "consistent", "situation": "", "knew_tsr": False})
        if "ROLE: rater" in prompt:
            import re
            ids = re.findall(r"^(S\d+):", prompt, flags=re.M)
            score = {"T": 6, "D": 2, "W": 3}
            return json.dumps({"ratings": {i: score.get(self.decoy_key.get(i, {}).get("version"), 4) for i in ids}, "knew_tsr": False})
        rid = self._record_id(prompt)
        dec = self.decisions.get(rid or "", {})
        shape = dec.get("shape", "keeps")
        if "ROLE: opponent" in prompt:
            return json.dumps({"id": rid, "alternative_shape": None, "rule_compliant": False,
                               "argument": "MOCK: no rule-compliant alternative", "reflected_sentence": "",
                               "knew_tsr": False})
        if "Theory of Lateral Correspondence" in prompt:
            return json.dumps({"id": rid, "reflected_formula": "Pitch = WL × Quickening", "reflected_sentence": "MOCK",
                               "shape": shape, "rule_reason": "MOCK", "new_words": [], "knew_framework": False})
        if self.flavour == "dissent" and model.endswith("-2"):
            shape = "keeps" if shape == "turns around" else "turns around"
        out = {"id": rid, "physical": dec.get("statement", ""), "reflected_formula": dec.get("image", ""),
               "reflected_sentence": "MOCK sentence in frozen words.", "shape": shape,
               "rule_reason": "MOCK: " + "; ".join(dec.get("reasons", [])), "rule_trace": dec.get("trace", []),
               "forced": dec.get("forced", False), "unmapped_terms": dec.get("unmapped", []),
               "new_words": ["Desire-field"] if self.flavour == "leak" else [],
               "monotone_claims": dec.get("monotone_claims", []), "interpretation": "MOCK",
               "conflicts": "none", "sense": 4, "confidence": 5, "closing": "MOCK", "knew_tsr": False}
        return json.dumps(out)


def make_provider(spec: ModelSpec, run_dir: Path | None = None) -> Provider:
    if spec.provider == "openai_compat":
        return OpenAICompat(spec.base_url or "https://api.openai.com/v1", spec.api_key_env or "OPENAI_API_KEY")
    if spec.provider == "anthropic":
        return Anthropic(spec.api_key_env or "ANTHROPIC_API_KEY")
    if spec.provider == "google":
        return Google(spec.api_key_env or "GOOGLE_API_KEY")
    if spec.provider == "replay":
        return Replay(CallLog(run_dir))
    if spec.provider.startswith("mock"):
        return Mock(spec.provider.split(":", 1)[1] if ":" in spec.provider else "agree")
    raise ValueError(f"unknown provider {spec.provider}")


class LoggedModel:
    def __init__(self, spec: ModelSpec, log: CallLog, provider: Provider | None = None):
        self.spec = spec
        self.log = log
        self.provider = provider or make_provider(spec, log.path.parent)

    def __call__(self, prompt: str, role: str, temperature: float = 0.0, max_tokens: int = 4000) -> str:
        h = sha(prompt)
        try:
            resp = self.provider.complete(prompt, self.spec.name, temperature, max_tokens)
            err = None
        except Exception as e:  # logged, not swallowed
            resp, err = None, repr(e)
        self.log.write(role=role, model=self.spec.name, provider=self.spec.provider, vendor=self.spec.vendor,
                       temperature=temperature, prompt_sha256=h, prompt_chars=len(prompt),
                       response=resp, error=err)
        if err:
            raise RuntimeError(f"{self.spec.name}: {err}")
        return resp


def load_models(path: Path) -> list[ModelSpec]:
    import yaml
    with open(path) as f:
        d = yaml.safe_load(f)
    return [ModelSpec(**m) for m in d["models"]]


def check_roster(models: list[ModelSpec], min_models: int = 5, min_vendors: int = 3) -> list[str]:
    problems = []
    if len(models) < min_models:
        problems.append(f"{len(models)} generators; spec needs ≥ {min_models}")
    vendors = {m.vendor for m in models}
    if len(vendors) < min_vendors:
        problems.append(f"{len(vendors)} vendors {sorted(vendors)}; spec needs ≥ {min_vendors}")
    if not any(m.open_weights for m in models):
        problems.append("no open-weights model in the roster")
    return problems
