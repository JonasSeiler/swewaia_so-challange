"""Behavior tests for monthly Stack Overflow data fetching.

These tests are written before implementation to define expected behavior.
"""

from unittest.mock import Mock, patch

import pandas as pd
import requests

from so_challenge import data_fetcher


def _monthly_payload(start_year: int = 2008, end_year: int = 2024) -> list[dict]:
	payload: list[dict] = []
	for year in range(start_year, end_year + 1):
		for month in range(1, 13):
			payload.append(
				{
					"year_month": f"{year}-{month:02d}",
					"question_count": 100,
				}
			)
	return payload


def _mock_response(items: list[dict]) -> Mock:
	response = Mock()
	response.raise_for_status = Mock()
	response.json.return_value = {"items": items}
	return response


def test_successful_fetch_returns_expected_dataframe_shape(tmp_path):
	expected_items = _monthly_payload(2008, 2024)
	cache_file = tmp_path / "so_monthly_counts.csv"

	with patch("so_challenge.data_fetcher.requests.get") as mocked_get:
		mocked_get.return_value = _mock_response(expected_items)

		df = data_fetcher.fetch_monthly_question_counts(
			start_year=2008,
			end_year=2024,
			cache_path=cache_file,
		)

	assert isinstance(df, pd.DataFrame)
	assert list(df.columns) == ["year_month", "question_count"]
	assert df.shape == (len(expected_items), 2)
	assert cache_file.exists()


def test_cached_data_is_returned_without_network_call(tmp_path):
	cache_file = tmp_path / "so_monthly_counts.csv"
	cached_df = pd.DataFrame(
		{
			"year_month": ["2024-01", "2024-02"],
			"question_count": [123, 234],
		}
	)
	cached_df.to_csv(cache_file, index=False)

	with patch("so_challenge.data_fetcher.requests.get", create=True) as mocked_get:
		result = data_fetcher.fetch_monthly_question_counts(cache_path=cache_file)

	mocked_get.assert_not_called()
	assert result.shape == cached_df.shape
	assert list(result.columns) == ["year_month", "question_count"]
	assert result.to_dict("records") == cached_df.to_dict("records")


def test_network_error_triggers_retry_logic(tmp_path):
	cache_file = tmp_path / "so_monthly_counts.csv"
	successful_response = _mock_response(
		[
			{
				"year_month": "2024-01",
				"question_count": 999,
			}
		]
	)

	with patch("so_challenge.data_fetcher.requests.get") as mocked_get, patch(
		"so_challenge.data_fetcher.time.sleep", create=True
	) as mocked_sleep:
		mocked_get.side_effect = [
			requests.exceptions.RequestException("temporary outage"),
			requests.exceptions.RequestException("temporary outage"),
			successful_response,
		]

		result = data_fetcher.fetch_monthly_question_counts(
			cache_path=cache_file,
			max_retries=3,
		)

	assert mocked_get.call_count == 3
	assert mocked_sleep.call_count == 2
	assert list(result.columns) == ["year_month", "question_count"]
	assert result.shape == (1, 2)
