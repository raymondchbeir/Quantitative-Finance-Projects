# src/config/settings.py

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient


# -------------------------
# Helpers
# -------------------------

def _read_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing config file: {path}")
    with path.open("r") as f:
        return yaml.safe_load(f) or {}


def _deep_merge(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    """Merge b into a (dicts only)."""
    out = dict(a)
    for k, v in b.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def resolve_project_root() -> Path:
    """
    Resolve `regime_adaptive_alpha/` root assuming this file lives at:
    regime_adaptive_alpha/src/config/settings.py
    """
    return Path(__file__).resolve().parents[2]


def resolve_repo_root(project_root: Path) -> Path:
    """
    Your current layout has .env at quant-github/.env and projects live under quant-github/projects/.
    If regime_adaptive_alpha is at quant-github/projects/regime_adaptive_alpha,
    then repo root is project_root.parent.parent.
    """
    # .../quant-github/projects/regime_adaptive_alpha -> .../quant-github
    return project_root.parent.parent


# -------------------------
# Config object
# -------------------------

@dataclass(frozen=True)
class Settings:
    project_root: Path
    repo_root: Path

    # Config dicts
    cfg_default: Dict[str, Any]
    cfg_universe: Dict[str, Any]
    cfg_backtest: Dict[str, Any]

    # Merged config (optional convenience)
    cfg: Dict[str, Any]

    # Resolved storage paths
    raw_path: Path
    derived_path: Path
    features_path: Path
    universe_path: Path
    reports_path: Path

    # Alpaca
    data_feed: str
    alpaca_client: StockHistoricalDataClient


def load_settings(
    env_path: Path | None = None,
    default_cfg: str = "configs/default.yaml",
    universe_cfg: str = "configs/universe.yaml",
    backtest_cfg: str = "configs/backtest.yaml",
) -> Settings:
    project_root = resolve_project_root()
    repo_root = resolve_repo_root(project_root)

    # Load .env (prefer explicit path; fallback to repo_root/.env)
    if env_path is None:
        env_path = repo_root / ".env"
    load_dotenv(env_path)

    # Secrets (do not store in YAML)
    api_key = os.getenv("ALPACA_API_KEY")
    secret_key = os.getenv("ALPACA_SECRET_KEY")
    if not api_key or not secret_key:
        raise RuntimeError("Missing ALPACA_API_KEY / ALPACA_SECRET_KEY in environment or .env")

    # Load YAML configs
    cfg_default = _read_yaml(project_root / default_cfg)
    cfg_universe = _read_yaml(project_root / universe_cfg)
    cfg_backtest = _read_yaml(project_root / backtest_cfg)

    # Merge into a single cfg (optional)
    cfg = _deep_merge(cfg_default, _deep_merge(cfg_universe, cfg_backtest))

    # Resolve storage paths (relative to project root)
    storage = cfg_default.get("storage", {})
    raw_path = project_root / storage.get("raw_path", "data/raw")
    derived_path = project_root / storage.get("derived_path", "data/derived")
    features_path = project_root / storage.get("features_path", "data/features")
    universe_path = project_root / storage.get("universe_path", "data/universe")
    reports_path = project_root / storage.get("reports_path", "reports")

    # Ensure folders exist
    for p in [raw_path, derived_path, features_path, universe_path, reports_path]:
        p.mkdir(parents=True, exist_ok=True)

    # Data feed: allow env override, fallback to YAML default, fallback "sip"
    data_feed = os.getenv("DATA_FEED") or cfg_default.get("data", {}).get("feed", "sip")

    # Alpaca client
    alpaca_client = StockHistoricalDataClient(api_key, secret_key)

    return Settings(
        project_root=project_root,
        repo_root=repo_root,
        cfg_default=cfg_default,
        cfg_universe=cfg_universe,
        cfg_backtest=cfg_backtest,
        cfg=cfg,
        raw_path=raw_path,
        derived_path=derived_path,
        features_path=features_path,
        universe_path=universe_path,
        reports_path=reports_path,
        data_feed=data_feed,
        alpaca_client=alpaca_client,
    )


# Convenience singletons (optional)
settings = load_settings()
cfg = settings.cfg
client = settings.alpaca_client