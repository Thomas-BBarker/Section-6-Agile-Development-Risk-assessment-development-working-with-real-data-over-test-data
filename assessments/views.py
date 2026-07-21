from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RiskAssessmentForm
from .models import RiskAssessment
from .services import perform_risk_assessment


@login_required
def create_assessment_view(request):
    if request.method == "POST":
        form = RiskAssessmentForm(request.POST)

        if form.is_valid():
            identifier = form.cleaned_data["identifier"]
            identifier_type = form.cleaned_data["identifier_type"]

            assessment = RiskAssessment.objects.create(
                user=request.user,
                identifier=identifier,
                identifier_type=identifier_type,
            )

            try:
                perform_risk_assessment(assessment)
                assessment.refresh_from_db()
            except Exception:
                assessment.delete()

                messages.error(
                    request,
                    "The breach lookup could not be completed. Please try again.",
                )

                return render(
                    request,
                    "assessments/create_assessment.html",
                    {"form": form},
                )

            return redirect(
                "assessments:result",
                assessment_id=assessment.id,
            )

    else:
        form = RiskAssessmentForm()

    return render(
        request,
        "assessments/create_assessment.html",
        {"form": form},
    )


@login_required
def assessment_result_view(request, assessment_id):
    assessment = get_object_or_404(
        RiskAssessment,
        id=assessment_id,
        user=request.user,
    )

    return render(
        request,
        "assessments/assessment_result.html",
        {"assessment": assessment},
    )