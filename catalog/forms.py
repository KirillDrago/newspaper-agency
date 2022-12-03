from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.urls import reverse

from catalog.models import Newspaper, Redactor


class RedactorCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "years_of_experience"
        )

        def get_absolute_url(self):  # new
            return reverse("redactor-list", args=[str(self.id)])


class RedactorExperienceUpdateForm(forms.ModelForm):

    class Meta:
        model = Redactor
        fields = ("years_of_experience",)

    def clean_years_of_experience(self):
        years_of_experience = self.cleaned_data["years_of_experience"]

        if 0 > years_of_experience:
            raise ValidationError("Experience must be positive")

        if years_of_experience > 99:
            raise ValidationError("Incorrect data")

        return years_of_experience


class NewspaperForm(forms.ModelForm):

    redactors = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Newspaper
        fields = "__all__"


class NewspaperSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by title"})
    )


class TopicSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"})
    )
