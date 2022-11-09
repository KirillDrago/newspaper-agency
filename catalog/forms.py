from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from catalog.models import Newspaper, Redactor


class RedactorCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields +(
            "first_name",
            "last_name",
            "years_of_experience"
        )


class RedactorExperienceUpdateForm(forms.ModelForm):

    class Meta:
        model = Redactor
        fields = ("years_of_experience",)


class NewspaperForm(forms.ModelForm):

    redactors = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Newspaper
        fields = "__all__"
