"""Behavior tests for milestone definitions and filtering."""

import pytest

from so_challenge import milestones


def test_default_milestones_are_well_formed_and_sorted():
	values = milestones.get_default_milestones()

	assert isinstance(values, list)
	assert len(values) > 0
	assert all("year_month" in item and "label" in item for item in values)
	assert [item["year_month"] for item in values] == sorted(
		item["year_month"] for item in values
	)


def test_milestones_for_range_filters_inclusively():
	values = [
		{"year_month": "2008-01", "label": "start"},
		{"year_month": "2012-06", "label": "middle"},
		{"year_month": "2024-12", "label": "end"},
	]

	filtered = milestones.milestones_for_range(values, start_year=2010, end_year=2024)

	assert filtered == [
		{"year_month": "2012-06", "label": "middle"},
		{"year_month": "2024-12", "label": "end"},
	]


def test_validate_milestones_rejects_invalid_entries():
	invalid_values = [{"year_month": "2024/01", "label": "bad-format"}]

	with pytest.raises(ValueError):
		milestones.validate_milestones(invalid_values)
