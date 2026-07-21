from django.db import transaction

from assessments.models import BreachFinding

from .breach_service import lookup_email_breaches
from .recommendations import generate_recommendations
from .scoring import (
    calculate_risk_score,
    determine_risk_level,
)


@transaction.atomic
def perform_risk_assessment(assessment):

    breaches = lookup_email_breaches(assessment.identifier)

    assessment.breach_findings.all().delete()

    exposed_data_types = set()
    sensitive_data_exposed = False

    for breach in breaches:
        exposed_data = list(breach.exposed_data)

        BreachFinding.objects.create(
            assessment=assessment,
            provider_breach_id=breach.provider_breach_id,
            name=breach.name,
            title=breach.title,
            domain=breach.domain,
            breach_date=breach.breach_date,
            exposed_data=exposed_data,
            is_verified=breach.is_verified,
            is_sensitive=breach.is_sensitive,
            is_retired=breach.is_retired,
        )

        exposed_data_types.update(
            str(item).strip().lower()
            for item in exposed_data
            if str(item).strip()
        )

        if breach.is_sensitive:
            sensitive_data_exposed = True

    breach_count = len(breaches)
    exposed_data_count = len(exposed_data_types)

    score = calculate_risk_score(breach_count)
    level = determine_risk_level(score)

    assessment.breach_count = breach_count
    assessment.exposed_data_count = exposed_data_count
    assessment.sensitive_data_exposed = sensitive_data_exposed
    assessment.risk_score = score
    assessment.risk_level = level
    assessment.recommendations = generate_recommendations(
        risk_level=level,
        breach_count=breach_count,
    )

    assessment.save(
        update_fields=[
            "breach_count",
            "exposed_data_count",
            "sensitive_data_exposed",
            "risk_score",
            "risk_level",
            "recommendations",
        ]
    )

    return assessment