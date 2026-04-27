"""Vacancy API operations for OrangeHRM."""

from typing import Any

from playwright.sync_api import Page

from data.models import CreatedVacancy, VacancyData, VacancyStatus
from tests.plugins.api_helpers import _extract_data, _extract_id, _extract_list, _parse_json, _response_text

VACANCIES_ENDPOINT = "/web/index.php/api/v2/recruitment/vacancies"
JOB_TITLES_ENDPOINT = "/web/index.php/api/v2/admin/job-titles"


def _resolve_job_title_id(page: Page, job_title: str) -> str:
    response = page.request.get(url=JOB_TITLES_ENDPOINT, params={"limit": 200, "offset": 0})
    payload = _parse_json(response, f"resolve job title '{job_title}'")
    records = _extract_list(payload, "resolve job title")

    for record in records:
        if record.get("title") != job_title:
            continue
        return _extract_id(record, ("id", "jobTitleId"), "job title")

    available_titles = sorted({str(record.get("title")) for record in records if record.get("title")})
    raise AssertionError(
        f"Job title '{job_title}' was not found in API response. Available titles sample: {available_titles[:10]}"
    )


def create_vacancy_using_api(page: Page, vacancy_data: VacancyData, hiring_manager_employee_id: str) -> CreatedVacancy:
    job_title_id = _resolve_job_title_id(page, vacancy_data.job_title)
    payload = {
        "name": vacancy_data.vacancy_name,
        "jobTitleId": job_title_id,
        "employeeId": hiring_manager_employee_id,
        "description": "",
        "status": vacancy_data.status == VacancyStatus.ACTIVE,
        "isPublished": True,
    }

    response = page.request.post(url=VACANCIES_ENDPOINT, data=payload)
    result = _parse_json(response, "create vacancy via API")
    data = _extract_data(result)
    if not isinstance(data, dict):
        raise AssertionError("Unexpected vacancy create response shape")

    vacancy_id = _extract_id(data, ("id", "vacancyId"), "vacancy")
    return CreatedVacancy(
        vacancy_id=vacancy_id,
        vacancy_name=vacancy_data.vacancy_name,
        job_title=vacancy_data.job_title,
        status=vacancy_data.status,
    )


def list_vacancies_using_api(page: Page) -> list[dict[str, Any]]:
    response = page.request.get(url=VACANCIES_ENDPOINT, params={"limit": 200, "offset": 0})
    payload = _parse_json(response, "list vacancies via API")
    return _extract_list(payload, "list vacancies via API")


def find_vacancy_id_by_name(page: Page, vacancy_name: str) -> str | None:
    for record in list_vacancies_using_api(page):
        if record.get("name") != vacancy_name:
            continue
        return _extract_id(record, ("id", "vacancyId"), "vacancy")

    return None


def delete_vacancy_using_api(page: Page, vacancy_id: str) -> None:
    response = page.request.delete(
        url=VACANCIES_ENDPOINT,
        data={"ids": [vacancy_id]},
        headers={"Content-Type": "application/json"},
    )
    assert response.ok, f"Failed to delete vacancy via API: {_response_text(response)}"
