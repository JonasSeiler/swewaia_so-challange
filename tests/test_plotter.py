"""Behavior tests for monthly question count plotting."""

from pathlib import Path

import matplotlib
import pandas as pd

from so_challenge import plotter


matplotlib.use("Agg")


def _sample_df() -> pd.DataFrame:
	return pd.DataFrame(
		{
			"year_month": ["2024-01", "2024-02", "2024-03"],
			"question_count": [120, 140, 135],
		}
	)


def test_plot_returns_figure_and_axis_with_required_labels():
	df = _sample_df()

	figure, axis = plotter.plot_monthly_question_counts(df)

	assert figure is not None
	assert axis is not None
	assert axis.get_xlabel() == "Year-Month"
	assert axis.get_ylabel() == "Question Count"
	assert len(axis.lines) == 1

	legend = axis.get_legend()
	assert legend is not None
	assert [text.get_text() for text in legend.get_texts()] == ["Questions"]


def test_plot_saves_figure_when_output_path_is_provided(tmp_path):
	df = _sample_df()
	output_path = tmp_path / "monthly_questions.png"

	figure, _ = plotter.plot_monthly_question_counts(df, output_path=output_path)

	assert isinstance(output_path, Path)
	assert output_path.exists()
	assert output_path.stat().st_size > 0
	figure.clf()


def test_plot_adds_milestone_overlay_and_legend_entry():
	df = _sample_df()
	milestones = [{"year_month": "2024-02", "label": "First milestone"}]

	_, axis = plotter.plot_monthly_question_counts(df, milestones=milestones)

	assert len(axis.lines) == 2
	legend = axis.get_legend()
	assert legend is not None
	legend_labels = [text.get_text() for text in legend.get_texts()]
	assert "Questions" in legend_labels
	assert "First milestone" in legend_labels
