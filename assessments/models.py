from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class RiskAssessment(models.Model):
    IDENTIFIER_TYPES = [
        ("email", "Email address"),
        ("username", "Username"),
    ]

    RISK_LEVELS = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="risk_assessments",
        null=True,
        blank=True,
    )

    identifier_type = models.CharField(
        max_length=20,
        choices=IDENTIFIER_TYPES,
    )

    identifier = models.CharField(
        max_length=255,
    )

    breach_count = models.PositiveIntegerField(
        default=0,
    )

    exposed_data_count = models.PositiveIntegerField(
        default=0,
    )

    sensitive_data_exposed = models.BooleanField(
        default=False,
    )

    risk_score = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
    )

    risk_level = models.CharField(
        max_length=20,
        choices=RISK_LEVELS,
        default="low",
    )

    recommendations = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"{self.user.username}: "
            f"{self.identifier_type} assessment "
            f"({self.risk_score}/10)"
        )
# Create your models here.
