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

def lookup_identifier(identifier: str) -> dict:
    normalised_identifier = identifier.strip().lower()

    return DEMO_RESULTS.get(
        normalised_identifier,
        {
            "breach_count": 0,
            "exposed_data_count": 0,
            "sensitive_data_exposed": False,
        },
    )

@dataclass
class AssessmentResult:
    breach_count: int
    exposed_data_count: int
    sensitive_data_exposed: bool
    risk_score: int
    risk_level: str
    recommendations: str


def calculate_risk_score(
    breach_count: int,
    exposed_data_count: int,
    sensitive_data_exposed: bool,
) -> tuple[int, str]:
    """
    Calculate a transparent risk score between 1 and 10.

    This is an initial project scoring model and should be validated
    during testing and evaluation.
    """

    score = 1

    # Breach frequency: maximum contribution of four points.
    score += min(breach_count, 4)

    # Number of different exposed data categories.
    if exposed_data_count >= 2:
        score += 1

    if exposed_data_count >= 5:
        score += 1

    # Passwords, financial information, or similar sensitive data.
    if sensitive_data_exposed:
        score += 3

    score = min(score, 10)

    if score <= 3:
        risk_level = "low"
    elif score <= 6:
        risk_level = "medium"
    elif score <= 8:
        risk_level = "high"
    else:
        risk_level = "critical"

    return score, risk_level


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
            "Review the affected accounts for unfamiliar logins, "
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

    return "\n".join(
        f"• {recommendation}"
        for recommendation in recommendations
    )

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


def lookup_identifier(identifier: str) -> dict:
    """
    Temporary local lookup used while developing the application.

    Replace this function with an external breach API after the local
    workflow has been tested.
    """

    normalised_identifier = identifier.strip().lower()

    return DEMO_RESULTS.get(
        normalised_identifier,
        {
            "breach_count": 0,
            "exposed_data_count": 0,
            "sensitive_data_exposed": False,
        },
    )


def assess_identifier(identifier: str) -> AssessmentResult:
    lookup_result = lookup_identifier(identifier)

    breach_count = lookup_result["breach_count"]
    exposed_data_count = lookup_result["exposed_data_count"]
    sensitive_data_exposed = lookup_result[
        "sensitive_data_exposed"
    ]

    risk_score, risk_level = calculate_risk_score(
        breach_count=breach_count,
        exposed_data_count=exposed_data_count,
        sensitive_data_exposed=sensitive_data_exposed,
    )

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