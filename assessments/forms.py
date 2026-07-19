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
            "identifier": forms.TextInput(
                attrs={
                    "placeholder": "Enter your email address or username",
                    "autocomplete": "off",
                }
            ),
        }

    def clean_identifier(self):
        identifier = self.cleaned_data["identifier"].strip()

        if len(identifier) < 3:
            raise forms.ValidationError(
                "The identifier must contain at least three characters."
            )

        return identifier

    def clean(self):
        cleaned_data = super().clean()

        identifier_type = cleaned_data.get("identifier_type")
        identifier = cleaned_data.get("identifier")

        if (
            identifier_type == "email"
            and identifier
            and "@" not in identifier
        ):
            self.add_error(
                "identifier",
                "Enter a valid email address.",
            )

        return cleaned_data