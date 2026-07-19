from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RiskAssessmentForm
from .models import RiskAssessment
from .services import assess_identifier


@login_required
def create_assessment_view(request):
    if request.method == "POST":
        form = RiskAssessmentForm(request.POST)

        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.user = request.user

            result = assess_identifier(assessment.identifier)

            assessment.breach_count = result.breach_count
            assessment.exposed_data_count = result.exposed_data_count
            assessment.sensitive_data_exposed = (
                result.sensitive_data_exposed
            )
            assessment.risk_score = result.risk_score
            assessment.risk_level = result.risk_level
            assessment.recommendations = result.recommendations

            assessment.save()

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
        "assessments/result.html",
        {"assessment": assessment},
    )