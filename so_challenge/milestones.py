"""Milestone definitions and helper utilities."""

import re


_YEAR_MONTH_PATTERN = re.compile(r"^\d{4}-\d{2}$")


def get_default_milestones() -> list[dict]:
	"""Return project milestone markers sorted by year-month."""

	values = [
		{"year_month": "2008-09", "label": "Stack Overflow launch era"},
		{"year_month": "2011-01", "label": "Early growth phase"},
		{"year_month": "2016-01", "label": "Mature adoption phase"},
		{"year_month": "2020-03", "label": "Remote-work shift"},
		{"year_month": "2024-01", "label": "Recent baseline"},
	]
	validate_milestones(values)
	return sorted(values, key=lambda item: item["year_month"])


def validate_milestones(values: list[dict]) -> None:
	"""Validate milestone list shape and year-month format."""

	for item in values:
		if "year_month" not in item or "label" not in item:
			raise ValueError("Each milestone must contain year_month and label fields")
		if not isinstance(item["year_month"], str) or not _YEAR_MONTH_PATTERN.match(
			item["year_month"]
		):
			raise ValueError("Milestone year_month must match YYYY-MM")
		if not isinstance(item["label"], str) or not item["label"].strip():
			raise ValueError("Milestone label must be a non-empty string")


def milestones_for_range(
	values: list[dict], start_year: int = 2008, end_year: int = 2024
) -> list[dict]:
	"""Return milestones with years between start_year and end_year inclusive."""

	validate_milestones(values)
	filtered = [
		item
		for item in values
		if start_year <= int(item["year_month"].split("-", maxsplit=1)[0]) <= end_year
	]
	return sorted(filtered, key=lambda item: item["year_month"])
