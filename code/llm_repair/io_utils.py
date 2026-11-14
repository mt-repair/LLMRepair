import json
from pathlib import Path


def load_json(value, label, required=False):
    if value is None:
        if required:
            raise ValueError("{} is required".format(label))
        return None
    if isinstance(value, (dict, list)):
        return value
    path = Path(value).absolute()
    if not path.is_file():
        raise FileNotFoundError("{} does not exist: {}".format(label, path))
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise ValueError("{} is not valid JSON: {}".format(label, exc)) from exc


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def tail_text(value, limit=4000):
    text = "" if value is None else str(value)
    return text if len(text) <= limit else text[-limit:]
