from django.db import transaction

from home.models import BreachFinding

from .breach_service import BreachServiceError, lookup_email_breaches
from .recommendations import generate_recommendations
from .scoring import (
    calculate_risk_score,
    determine_risk_level,
    generate_assessment_summary,
)


@transaction.atomic
def perform_risk_assessment(assessment):
    assessment.status = "processing"
    assessment.error_message = ""
    assessment.save(update_fields=["status", "error_message"])

    try:
        breaches = lookup_email_breaches(assessment.email)

        assessment.breach_findings.all().delete()

        for breach in breaches:
            BreachFinding.objects.create(
                assessment=assessment,
                provider_breach_id=breach.provider_breach_id,
                name=breach.name,
                title=breach.title,
                domain=breach.domain,
                breach_date=breach.breach_date,
                exposed_data=list(breach.exposed_data),
                is_verified=breach.is_verified,
                is_sensitive=breach.is_sensitive,
                is_retired=breach.is_retired,
            )

        breach_count = len(breaches)
        score = calculate_risk_score(breach_count)
        level = determine_risk_level(score)

        assessment.unique_breach_count = breach_count
        assessment.risk_score = score
        assessment.risk_level = level
        assessment.summary = generate_assessment_summary(
            breach_count=breach_count,
            score=score,
            risk_level=level,
        )
        assessment.recommendations = generate_recommendations(
            risk_level=level,
            breach_count=breach_count,
        )
        assessment.status = "completed"
        assessment.error_message = ""

    except BreachServiceError as exc:
        assessment.status = "failed"
        assessment.error_message = str(exc)

    assessment.save()

    return assessment