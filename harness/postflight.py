"""
Postflight validation (K⁺).

Reads a finished run directory and validates the outcome. Turns crashes, core dumps,
and garbage metrics into structured status.
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd


@dataclass(frozen=True)
class PostflightStatus:
    """Result of postflight validation.

    Attributes:
        success: True if run completed successfully with valid metrics.
        at_fault_collision: True if the published at-fault flag is set.
            That is collision_at_fault, or front/lateral when that column is absent.
            collision_any is not at-fault: it includes rear contact.
        rear_contact: True if collision_rear is set on any scored step.
        solver_status: The MPC solver status if controller CSV exists, else None.
        error: Human-readable error message if validation failed, else None.
    """

    success: bool
    at_fault_collision: Optional[bool] = None
    rear_contact: Optional[bool] = None
    solver_status: Optional[str] = None
    error: Optional[str] = None


def _is_positive(values) -> bool:
    """True when a metric cell or a sequence of cells contains a non-zero value."""
    if isinstance(values, (list, tuple)):
        return any(_is_positive(item) for item in values)
    if hasattr(values, "__iter__") and not isinstance(values, str):
        try:
            return any(_is_positive(item) for item in values)
        except TypeError:
            pass
    try:
        return float(values) != 0.0
    except (TypeError, ValueError):
        return bool(values)


def _metric_positive(df: pd.DataFrame, name: str) -> Optional[bool]:
    """Max of one metric across every timestep. None when the column is absent."""
    if "name" not in df.columns or name not in set(df["name"]):
        return None
    cells = df.loc[df["name"] == name, "values"]
    return any(_is_positive(cell) for cell in cells)


def _aggregate_file(run_path: Path) -> Optional[Path]:
    """Published eval table, which drops steps outside the scored window."""
    current = run_path if run_path.is_dir() else run_path.parent
    for _ in range(8):
        candidate = current / "aggregate" / "metrics_results.txt"
        if candidate.is_file():
            return candidate
        if current.parent == current:
            return None
        current = current.parent
    return None


def _flags_from_aggregate(path: Path) -> Optional[tuple[bool, bool]]:
    text = path.read_text(errors="replace")
    found: dict[str, float] = {}
    for name in (
        "collision_at_fault",
        "collision_front",
        "collision_lateral",
        "collision_rear",
    ):
        match = re.search(rf"│\s*{name}\s+│\s+([0-9.]+|inf)", text)
        if match:
            found[name] = float(match.group(1))
    if "collision_rear" not in found:
        return None
    if "collision_at_fault" in found:
        at_fault = found["collision_at_fault"] != 0.0
    else:
        at_fault = found.get("collision_front", 0.0) != 0.0 or found.get(
            "collision_lateral", 0.0
        ) != 0.0
    return at_fault, found["collision_rear"] != 0.0


def _flags_from_parquet(df: pd.DataFrame) -> tuple[bool, bool]:
    at_fault = _metric_positive(df, "collision_at_fault")
    if at_fault is None:
        at_fault = bool(_metric_positive(df, "collision_front")) or bool(
            _metric_positive(df, "collision_lateral")
        )
    rear = bool(_metric_positive(df, "collision_rear"))
    return at_fault, rear


def _metrics_file(run_path: Path) -> Optional[Path]:
    """Metrics table for this run.

    A wizard log directory keeps the parquet under ``rollouts/``, not at the root.
    """
    for pattern in ("metrics.parquet", "metrics.pkl"):
        candidate = run_path / pattern
        if candidate.is_file():
            return candidate
    if not run_path.is_dir():
        return None
    nested = sorted(run_path.rglob("metrics.parquet"))
    return nested[0] if nested else None


def validate_postflight(run_dir: str) -> PostflightStatus:
    """
    Validate a finished run directory.

    Reads metrics and controller CSV to assess the run. Fails if metrics are missing.

    Args:
        run_dir: Path to the finished run directory.

    Returns:
        PostflightStatus with outcome and any relevant error details.
    """
    run_path = Path(run_dir)

    if not run_path.is_dir():
        return PostflightStatus(
            success=False, error=f"run_dir does not exist: {run_dir}"
        )

    metrics_file = _metrics_file(run_path)
    if metrics_file is None:
        return PostflightStatus(
            success=False, error="metrics file not found (no metrics.parquet)"
        )

    # Load metrics
    try:
        if metrics_file.suffix == ".parquet":
            df = pd.read_parquet(metrics_file)
        else:
            df = pd.read_pickle(metrics_file)
    except Exception as e:
        return PostflightStatus(
            success=False, error=f"failed to load metrics: {e}"
        )

    aggregate = _aggregate_file(run_path)
    if aggregate is not None:
        parsed = _flags_from_aggregate(aggregate)
        at_fault, rear = parsed if parsed is not None else _flags_from_parquet(df)
    else:
        at_fault, rear = _flags_from_parquet(df)

    # Check for controller CSV and extract solver status
    solver_status = None
    controller_dir = run_path.parent.parent / "controller"
    if controller_dir.exists():
        # Find the controller CSV for this run
        csv_files = list(controller_dir.glob("*.csv"))
        if csv_files:
            controller_csv = csv_files[0]
            try:
                controller_df = pd.read_csv(controller_csv)
                if "status" in controller_df.columns:
                    statuses = controller_df["status"].unique()
                    # Combine all unique statuses
                    solver_status = ",".join(str(s) for s in statuses)
            except Exception:
                pass  # Ignore controller CSV errors

    return PostflightStatus(
        success=True,
        at_fault_collision=at_fault,
        rear_contact=rear,
        solver_status=solver_status,
    )
