from dataclasses import dataclass


@dataclass
class LLMRepairConfig:
    """Configuration for the one-stage repair workflow."""

    model: str = "deepseek-r1:14b"
    ollama_host: str = "http://localhost:11434"
    temperature: float = 0.09
    seed: int = 0
    num_ctx: int = 32768
    # Five candidates share one response; allow enough output for long edits.
    num_predict: int = 8192
    timeout: int = 900

    # All candidates are requested together in one model response.
    patch_budget: int = 5
    # Zero means exactly one generation call per evidence scenario.
    max_generation_retries: int = 0
    max_edits: int = 3
    max_total_touched_lines: int = 20
    context_radius: int = 15
    # When a fault line is supplied, every accepted candidate must cover it.
    require_known_line_coverage: bool = True

    compile_timeout: int = 60
    check_timeout: int = 10
    keep_workspaces: bool = False
    verify_ollama_model: bool = True

    def validate(self):
        if self.patch_budget <= 0:
            raise ValueError("patch_budget must be > 0")
        if self.max_generation_retries < 0:
            raise ValueError("max_generation_retries must be >= 0")
        if self.max_edits <= 0:
            raise ValueError("max_edits must be > 0")
        if self.max_total_touched_lines <= 0:
            raise ValueError("max_total_touched_lines must be > 0")
        if self.context_radius < 0:
            raise ValueError("context_radius must be >= 0")
        if self.num_ctx <= 0 or self.num_predict <= 0:
            raise ValueError("num_ctx and num_predict must be > 0")
        if self.timeout <= 0 or self.compile_timeout <= 0 or self.check_timeout <= 0:
            raise ValueError("timeouts must be > 0")
        if self.temperature < 0:
            raise ValueError("temperature must be >= 0")
