from django import forms
from django.core.exceptions import ValidationError
from datetime import date


def validate_future_or_today(value):
    if value < date.today():
        raise ValidationError("Choose a valid date")


def validate_positive(value):
    if value is not None and value <= -1:
        raise ValidationError("Enter a positive value")


def validate_pity(value):
    if value >= 90 or value < 0:
        raise ValidationError("Enter the pity rate correctly.")


class MyForm(forms.Form):
    date_input = forms.DateField(
        label="Choose a date",
        widget=forms.DateInput(
            attrs={"style": "text-align: center; padding: 0px", "type": "date"}
        ),
        input_formats=["%Y-%m-%d"],
        validators=[validate_future_or_today],
        required=True,
    )
    primogems_input = forms.IntegerField(
        label="Enter actual primogems",
        widget=forms.NumberInput(
            attrs={
                "style": "text-align: center; padding: 0px",
                "placeholder": "Enter a positive value",
            }
        ),
        validators=[validate_positive],
        required=True,
    )
    starglitter_input = forms.IntegerField(
        label="Starglitter",
        widget=forms.NumberInput(
            attrs={
                "style": "text-align: center; padding: 0px; width: 100%;",
            }
        ),
        validators=[validate_positive],
        required=True,
    )
    pity_input = forms.IntegerField(
        label="Pity",
        widget=forms.NumberInput(
            attrs={
                "style": "text-align: center; padding: 0px; width: 100%;",
            }
        ),
        validators=[validate_pity],
        required=True,
    )
    welkin_input = forms.BooleanField(
        label="Welkin",
        widget=forms.CheckboxInput(),
    )
    events_input = forms.IntegerField(
        label="Events",
        widget=forms.NumberInput(
            attrs={"style": "text-align: center; padding: 0px; width: 100%;"}
        ),
        validators=[validate_positive],
        required=True,
    )
    quests_input = forms.IntegerField(
        label="Quests",
        widget=forms.NumberInput(
            attrs={"style": "text-align: center; padding: 0px; width: 100%;"}
        ),
        validators=[validate_positive],
        required=True,
    )
    others_input = forms.IntegerField(
        label="Others",
        widget=forms.NumberInput(
            attrs={"style": "text-align: center; padding: 0px; width: 100%;"}
        ),
        validators=[validate_positive],
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initial values of fields
        self.fields["date_input"].initial = date.today()
        self.fields["primogems_input"].initial = 10830
        self.fields["starglitter_input"].initial = 28
        self.fields["pity_input"].initial = 0
        self.fields["welkin_input"].initial = True
        self.fields["events_input"].initial = 1600
        self.fields["quests_input"].initial = 0
        self.fields["others_input"].initial = 1900
