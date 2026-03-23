"""Data collection utilities for monthly Stack Overflow question counts."""

from pathlib import Path
import time

import pandas as pd
import requests

DEFAULT_API_URL = "https://api.stackexchange.com/2.3/questions/monthly-counts"
EXPECTED_COLUMNS = ["year_month", "question_count"]


def fetch_monthly_question_counts(
	start_year: int = 2008,
	end_year: int = 2024,
	cache_path: str | Path = "data/so_monthly_counts.csv",
	max_retries: int = 3,
	retry_delay_seconds: float = 1.0,
) -> pd.DataFrame:
	"""Fetch monthly SO question counts and cache as CSV.

	Cached data is returned immediately when the cache file exists.
	Network requests are retried on transient request errors.
	"""

	cache_file = Path(cache_path)
	if cache_file.exists():
		return _read_cached_dataframe(cache_file)

	items = _fetch_with_retries(
		start_year=start_year,
		end_year=end_year,
		max_retries=max_retries,
		retry_delay_seconds=retry_delay_seconds,
	)

	df = _items_to_dataframe(items)
	cache_file.parent.mkdir(parents=True, exist_ok=True)
	df.to_csv(cache_file, index=False)
	return df


def _read_cached_dataframe(cache_file: Path) -> pd.DataFrame:
	cached = pd.read_csv(cache_file)
	return cached.loc[:, EXPECTED_COLUMNS]


def _fetch_with_retries(
	start_year: int,
	end_year: int,
	max_retries: int,
	retry_delay_seconds: float,
) -> list[dict]:
	params = {
		"start_year": start_year,
		"end_year": end_year,
		"interval": "monthly",
	}

	for attempt in range(1, max_retries + 1):
		try:
			response = requests.get(DEFAULT_API_URL, params=params, timeout=30)
			response.raise_for_status()
			payload = response.json()
			return payload.get("items", [])
		except requests.exceptions.RequestException:
			if attempt >= max_retries:
				raise
			time.sleep(retry_delay_seconds)

	return []


def _items_to_dataframe(items: list[dict]) -> pd.DataFrame:
	df = pd.DataFrame(items)
	if df.empty:
		return pd.DataFrame(columns=EXPECTED_COLUMNS)
	return df.loc[:, EXPECTED_COLUMNS]
