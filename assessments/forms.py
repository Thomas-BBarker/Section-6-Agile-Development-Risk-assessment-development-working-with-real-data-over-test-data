from django import forms

from .models import RiskAssessment


class RiskAssessmentForm(forms.ModelForm):
    class Meta:
        model = RiskAssessment
        fields = [
            "identifier_type",
            "identifier",
        ]

        widgets = {
            "identifier_type": forms.Select(),
            "identifier": forms.EmailInput(
                attrs={
                    "placeholder": "Enter your email address",
                    "autocomplete": "email",
                }
            ),
        }

        labels = {
            "identifier_type": "Identifier type",
            "identifier": "Email address",
        }

    def clean_identifier(self):
        identifier = self.cleaned_data["identifier"].strip().lower()

        try:
            forms.EmailField().clean(identifier)
        except forms.ValidationError:
            raise forms.ValidationError(
                "Enter a valid email address."
            )

        return identifier