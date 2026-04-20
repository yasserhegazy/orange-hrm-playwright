"""Shared HTTP/API helper utilities for OrangeHRM API interactions."""

from typing import Any

from playwright.sync_api import APIResponse
from playwright.sync_api import Error as PlaywrightError


def _response_text(response: APIResponse) -> str:
    try:
        return response.text()
    except PlaywrightError, ValueError:  # pragma: no cover - defensive fallback
        return "<response body unavailable>"


def _extract_invalid_param_keys(response: APIResponse) -> list[str]:
    try:
        payload = response.json()
    except PlaywrightError, ValueError:  # pragma: no cover - defensive fallback
        return []

    if not isinstance(payload, dict):
        return []

    error = payload.get("error")
    if not isinstance(error, dict):
        return []

    data = error.get("data")
    if not isinstance(data, dict):
        return []

    keys = data.get("invalidParamKeys")
    if not isinstance(keys, list):
        return []

    return [str(key) for key in keys]


def _parse_json(response: APIResponse, action: str) -> dict[str, Any]:
    invalid_keys = _extract_invalid_param_keys(response)
    invalid_keys_message = f" invalidParamKeys={invalid_keys}" if invalid_keys else ""
    assert response.ok, (
        f"Failed to {action}. Status {response.status}: {_response_text(response)}{invalid_keys_message}"
    )
    try:
        payload = response.json()
    except (PlaywrightError, ValueError) as exc:  # pragma: no cover - defensive fallback
        raise AssertionError(f"Failed to decode JSON while trying to {action}: {exc}") from exc

    if not isinstance(payload, dict):
        raise AssertionError(f"Unexpected JSON shape while trying to {action}: {type(payload).__name__}")

    return payload


def _extract_data(payload: dict[str, Any]) -> Any:
    return payload.get("data", payload)


def _extract_id(entity: dict[str, Any], keys: tuple[str, ...], entity_name: str) -> str:
    for key in keys:
        value = entity.get(key)
        if value is not None and value != "":
            return str(value)

    raise AssertionError(f"Could not extract {entity_name} id from response entity keys: {sorted(entity.keys())}")


def _extract_list(payload: dict[str, Any], action: str) -> list[dict[str, Any]]:
    data = _extract_data(payload)
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]

    raise AssertionError(f"Expected list response while trying to {action}, got: {type(data).__name__}")
