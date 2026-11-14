import json
import re
import time

import requests


class OllamaError(RuntimeError):
    pass


class OllamaJSONError(OllamaError):
    def __init__(self, message, raw_content="", metadata=None):
        super().__init__(message)
        self.raw_content = raw_content
        self.metadata = metadata or {}


class OllamaClient:
    """Small streaming Ollama client with schema-constrained JSON output."""

    def __init__(self, config):
        self.config = config

    def verify_model(self):
        try:
            response = requests.get(
                self.config.ollama_host.rstrip("/") + "/api/tags",
                timeout=(10, min(self.config.timeout, 30)),
            )
            response.raise_for_status()
            models = response.json().get("models", [])
        except requests.RequestException as exc:
            raise OllamaError("Cannot reach Ollama: {}".format(exc)) from exc
        names = [item.get("name") for item in models]
        if self.config.model not in names:
            raise OllamaError(
                "Ollama model '{}' not found. Available: {}".format(
                    self.config.model, names
                )
            )
        return names

    @staticmethod
    def _strip_fence(content):
        text = content.strip()
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
        return text.strip()

    def chat_json(self, messages, schema, temperature=None, seed=None):
        effective_temperature = (
            self.config.temperature if temperature is None else float(temperature)
        )
        effective_seed = self.config.seed if seed is None else int(seed)
        payload = {
            "model": self.config.model,
            "messages": messages,
            "stream": True,
            "format": schema,
            "think": False,
            "keep_alive": "30m",
            "options": {
                "temperature": effective_temperature,
                "seed": effective_seed,
                "num_ctx": self.config.num_ctx,
                "num_predict": self.config.num_predict,
            },
        }
        prompt_chars = sum(len(str(x.get("content", ""))) for x in messages)
        started = time.monotonic()
        parts = []
        metadata = {
            "model": self.config.model,
            "temperature": effective_temperature,
            "seed": effective_seed,
            "num_ctx": self.config.num_ctx,
            "num_predict": self.config.num_predict,
            "prompt_chars": prompt_chars,
        }
        try:
            with requests.post(
                self.config.ollama_host.rstrip("/") + "/api/chat",
                json=payload,
                stream=True,
                timeout=(30, self.config.timeout),
            ) as response:
                response.raise_for_status()
                for raw_line in response.iter_lines(decode_unicode=True):
                    if not raw_line:
                        continue
                    chunk = json.loads(raw_line)
                    if chunk.get("error"):
                        raise OllamaError(chunk["error"])
                    parts.append((chunk.get("message") or {}).get("content", ""))
                    for key in (
                        "done", "done_reason", "prompt_eval_count", "eval_count",
                        "prompt_eval_duration", "eval_duration", "total_duration",
                        "load_duration",
                    ):
                        if key in chunk:
                            metadata[key] = chunk[key]
        except requests.RequestException as exc:
            raise OllamaError("Ollama request failed: {}".format(exc)) from exc

        content = "".join(parts)
        metadata["client_elapsed_seconds"] = round(time.monotonic() - started, 3)
        if not content.strip():
            raise OllamaJSONError("Ollama returned empty content", content, metadata)
        try:
            parsed = json.loads(self._strip_fence(content))
        except json.JSONDecodeError as exc:
            raise OllamaJSONError(
                "Model output is not valid JSON: {}".format(exc), content, metadata
            ) from exc
        return {"parsed": parsed, "raw_content": content, "metadata": metadata}
