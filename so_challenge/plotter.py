"""Visualization utilities for monthly question count plots."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_monthly_question_counts(
	data: pd.DataFrame,
	milestones: list[dict] | None = None,
	output_path: str | Path | None = None,
):
	"""Create a line plot for monthly question counts with optional milestones."""

	frame = data.copy()
	frame["year_month"] = pd.to_datetime(frame["year_month"], format="%Y-%m")

	figure, axis = plt.subplots(figsize=(10, 5))
	axis.plot(frame["year_month"], frame["question_count"], label="Questions")

	if milestones:
		for milestone in milestones:
			x_value = pd.to_datetime(milestone["year_month"], format="%Y-%m")
			axis.axvline(x=x_value, linestyle="--", linewidth=1.5, label=milestone["label"])

	axis.set_xlabel("Year-Month")
	axis.set_ylabel("Question Count")
	axis.legend()
	figure.tight_layout()

	if output_path is not None:
		path = Path(output_path)
		path.parent.mkdir(parents=True, exist_ok=True)
		figure.savefig(path)

	return figure, axis
