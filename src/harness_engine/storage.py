from __future__ import annotations

from pathlib import Path
from typing import TypeVar

import yaml
from pydantic import BaseModel

ModelT = TypeVar("ModelT", bound=BaseModel)


def dump_model(path: Path, model: BaseModel) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = model.model_dump(mode="json")
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def load_model(path: Path, model_type: type[ModelT]) -> ModelT:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return model_type.model_validate(data)


def next_id(folder: Path, prefix: str) -> str:
    folder.mkdir(parents=True, exist_ok=True)
    existing = []
    for path in folder.glob(f"{prefix}-*.yaml"):
        stem = path.stem
        try:
            existing.append(int(stem.split("-")[-1]))
        except ValueError:
            continue
    return f"{prefix}-{max(existing, default=0) + 1:04d}"

