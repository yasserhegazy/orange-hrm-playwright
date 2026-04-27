"""Candidate API operations for OrangeHRM."""

from typing import Any

from playwright.sync_api import Page

from data.models import CandidateData, CreatedCandidate
from tests.plugins.api_helpers import _extract_data, _extract_id, _extract_list, _parse_json, _response_text

CANDIDATES_ENDPOINT = "/web/index.php/api/v2/recruitment/candidates"


def create_candidate_using_api(page: Page, candidate_data: CandidateData, vacancy_id: str) -> CreatedCandidate:
    response = page.request.post(
        url=CANDIDATES_ENDPOINT,
        data={
            "firstName": candidate_data.first_name,
            "middleName": "",
            "lastName": candidate_data.last_name,
            "email": candidate_data.email,
            "vacancyId": vacancy_id,
            "consentToKeepData": False,
        },
    )

    payload = _parse_json(response, "create candidate via API")
    data = _extract_data(payload)
    if not isinstance(data, dict):
        raise AssertionError("Unexpected candidate create response shape")

    candidate_id = _extract_id(data, ("id", "candidateId"), "candidate")
    return CreatedCandidate(
        candidate_id=candidate_id,
        first_name=candidate_data.first_name,
        last_name=candidate_data.last_name,
        email=candidate_data.email,
        vacancy_name=candidate_data.vacancy_name,
    )


def list_candidates_using_api(page: Page) -> list[dict[str, Any]]:
    response = page.request.get(url=CANDIDATES_ENDPOINT, params={"limit": 200, "offset": 0})
    payload = _parse_json(response, "list candidates via API")
    return _extract_list(payload, "list candidates via API")


def _record_vacancy_name(record: dict[str, Any]) -> str | None:
    vacancy = record.get("vacancy")
    if isinstance(vacancy, dict):
        name = vacancy.get("name")
        if isinstance(name, str):
            return name

    value = record.get("vacancyName")
    if isinstance(value, str):
        return value

    return None


def find_candidate_id(page: Page, candidate_data: CandidateData) -> str | None:
    for record in list_candidates_using_api(page):
        record_email = record.get("email")
        if isinstance(record_email, str) and record_email == candidate_data.email:
            return _extract_id(record, ("id", "candidateId"), "candidate")

        first_name = record.get("firstName")
        last_name = record.get("lastName")
        vacancy_name = _record_vacancy_name(record)
        if (
            first_name == candidate_data.first_name
            and last_name == candidate_data.last_name
            and vacancy_name == candidate_data.vacancy_name
        ):
            return _extract_id(record, ("id", "candidateId"), "candidate")

    return None


def delete_candidate_using_api(page: Page, candidate_id: str) -> None:
    response = page.request.delete(
        url=CANDIDATES_ENDPOINT,
        data={"ids": [candidate_id]},
        headers={"Content-Type": "application/json"},
    )
    assert response.ok, f"Failed to delete candidate via API: {_response_text(response)}"
