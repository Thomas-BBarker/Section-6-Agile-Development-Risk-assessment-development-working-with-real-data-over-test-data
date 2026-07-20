from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

import requests
from django.conf import settings


class BreachServiceError(Exception):
    """Raised when the breach API request cannot be completed."""


@dataclass(frozen=True)
class NormalisedBreach:
    provider_breach_id: str
    name: str
    title: str
    domain: str = ""
    breach_date: date | None = None
    added_date: date | None = None
    exposed_data: tuple[str, ...] = ()
    is_verified: bool = False
    is_sensitive: bool = False
    is_retired: bool = False


def _parse_date(value: Any) -> date | None:
    if not value:
        return None

    try:
        return date.fromisoformat(str(value)[:10])
    except (TypeError, ValueError):
        return None


def _normalise_name(name: Any) -> str:
    value = str(name or "").strip()
    return value or "Unknown breach"


def lookup_email_breaches(email: str) -> list[NormalisedBreach]:
    email = email.strip().lower()

    if not email:
        raise BreachServiceError("An email address is required.")

    endpoint = getattr(
        settings,
        "BREACH_API_ENDPOINT",
        "https://api.xposedornot.com/v1/check-email",
    )

    timeout = getattr(settings, "BREACH_API_TIMEOUT", 10)

    try:
        response = requests.get(
            f"{endpoint}/{email}",
            headers={
                "Accept": "application/json",
                "User-Agent": "DigitalFootprintRiskAssessment/1.0",
            },
            timeout=timeout,
        )
    except requests.RequestException as exc:
        raise BreachServiceError(
            "The breach service could not be reached."
        ) from exc

    if response.status_code == 404:
        return []

    if response.status_code == 429:
        raise BreachServiceError(
            "The breach service rate limit has been reached. Try again later."
        )

    if response.status_code >= 500:
        raise BreachServiceError(
            "The breach service is temporarily unavailable."
        )

    if response.status_code != 200:
        raise BreachServiceError(
            f"The breach service returned HTTP {response.status_code}."
        )

    try:
        payload = response.json()
    except ValueError as exc:
        raise BreachServiceError(
            "The breach service returned invalid JSON."
        ) from exc

    return _normalise_response(payload)


def _normalise_response(payload: Any) -> list[NormalisedBreach]:
    if not isinstance(payload, dict):
        return []

    breaches_data = payload.get("breaches")

    if not breaches_data:
        return []

    if isinstance(breaches_data, list) and breaches_data:
        if (
            len(breaches_data) == 1
            and isinstance(breaches_data[0], list)
        ):
            breaches_data = breaches_data[0]

    results: list[NormalisedBreach] = []
    seen: set[str] = set()

    for index, item in enumerate(breaches_data):
        if isinstance(item, str):
            name = _normalise_name(item)

            unique_id = f"xon-{index}-{name.lower().replace(' ', '-')}"
            domain = ""
            breach_date = None
            exposed_data: tuple[str, ...] = ()

        elif isinstance(item, dict):
            name = _normalise_name(
                item.get("breach")
                or item.get("name")
                or item.get("title")
            )

            unique_id = str(
                item.get("id")
                or item.get("breach_id")
                or f"xon-{index}-{name.lower().replace(' ', '-')}"
            )

            domain = str(item.get("domain") or "")
            breach_date = _parse_date(
                item.get("breach_date") or item.get("breached_date")
            )

            raw_exposed_data = (
                item.get("exposed_data")
                or item.get("data_classes")
                or []
            )

            if isinstance(raw_exposed_data, str):
                exposed_data = tuple(
                    part.strip()
                    for part in raw_exposed_data.split(",")
                    if part.strip()
                )
            else:
                exposed_data = tuple(
                    str(value) for value in raw_exposed_data
                )

        else:
            continue

        deduplication_key = unique_id.lower()

        if deduplication_key in seen:
            continue

        seen.add(deduplication_key)

        results.append(
            NormalisedBreach(
                provider_breach_id=unique_id,
                name=name,
                title=name,
                domain=domain,
                breach_date=breach_date,
                exposed_data=exposed_data,
            )
        )

    return results