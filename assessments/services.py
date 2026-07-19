from dataclasses import dataclass


DEMO_RESULTS = {
    "lowrisk@example.com": {
        "breach_count": 0,
        "exposed_data_count": 0,
        "sensitive_data_exposed": False,
    },
    "mediumrisk@example.com": {
        "breach_count": 2,
        "exposed_data_count": 3,
        "sensitive_data_exposed": False,
    },
    "highrisk@example.com": {
        "breach_count": 4,
        "exposed_data_count": 6,
        "sensitive_data_exposed": True,
    },
}


@dataclass
class AssessmentResult:
    breach_count: int
    exposed_data_count: int
    sensitive_data_exposed: bool
    risk_score: int
    risk_level: str
    recommendations: str


def lookup_demo_identifier(identifier: str) -> dict:

    normalised_identifier = identifier.strip().lower()

    return DEMO_RESULTS.get(
        normalised_identifier,
        {
            "breach_count": 0,
            "exposed_data_count": 0,
            "sensitive_data_exposed": False,
        },
    )


def calculate_risk_score(
    breach_count: int,
    exposed_data_count: int,
    sensitive_data_exposed: bool,
) -> int:
    score = 1

    if breach_count >= 1:
        score += 2

    if breach_count >= 3:
        score += 2

    if breach_count >= 5:
        score += 2

    if exposed_data_count >= 5:
        score += 1

    if exposed_data_count >= 10:
        score += 1

    if sensitive_data_exposed:
        score += 1

    return min(score, 10)


def determine_risk_level(score: int) -> str:
    if score <= 3:
        return "low"

    if score <= 6:
        return "medium"

    return "high"


def create_recommendations(
    breach_count: int,
    sensitive_data_exposed: bool,
) -> str:
    recommendations = [
        "Use a unique password for every online account.",
        "Enable multi-factor authentication where it is available.",
    ]

    if breach_count > 0:
        recommendations.append(
            "Change passwords for affected accounts and any other "
            "accounts where the same password was reused."
        )

        recommendations.append(
            "Review affected accounts for unfamiliar logins, "
            "messages, purchases, or profile changes."
        )

    if sensitive_data_exposed:
        recommendations.append(
            "Closely monitor important accounts because sensitive "
            "information may have been exposed."
        )

        recommendations.append(
            "Be cautious of phishing emails, unexpected password-reset "
            "messages, and requests for personal information."
        )

    if breach_count == 0:
        recommendations.append(
            "No known breaches were identified, but continue following "
            "good password and account-security practices."
        )

    return "\n".join(
        f"• {recommendation}"
        for recommendation in recommendations
    )


def assess_identifier(identifier: str) -> AssessmentResult:
    lookup_result = lookup_demo_identifier(identifier)

    breach_count = lookup_result["breach_count"]
    exposed_data_count = lookup_result["exposed_data_count"]
    sensitive_data_exposed = lookup_result[
        "sensitive_data_exposed"
    ]

    risk_score = calculate_risk_score(
        breach_count=breach_count,
        exposed_data_count=exposed_data_count,
        sensitive_data_exposed=sensitive_data_exposed,
    )

    risk_level = determine_risk_level(risk_score)

    recommendations = create_recommendations(
        breach_count=breach_count,
        sensitive_data_exposed=sensitive_data_exposed,
    )

    return AssessmentResult(
        breach_count=breach_count,
        exposed_data_count=exposed_data_count,
        sensitive_data_exposed=sensitive_data_exposed,
        risk_score=risk_score,
        risk_level=risk_level,
        recommendations=recommendations,
    )