from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from assessments.models import RiskAssessment
from .forms import RegisterForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("accounts:dashboard")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        },
    )


@login_required
def dashboard_view(request):
    assessments = RiskAssessment.objects.filter(
        user=request.user
    ).order_by("-created_at")

    latest_assessment = assessments.first()

    return render(
        request,
        "accounts/dashboard.html",
        {
            "assessments": assessments,
            "latest_assessment": latest_assessment,
        },
    )