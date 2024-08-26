from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Dosage, SideEffect, Note, Theme, Drug



class CustomUserCreationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput)


class NoteForm(forms.ModelForm):
    new_drug_name = forms.CharField(max_length=255, required=True, label="Drug Name")
    new_theme_name = forms.CharField(max_length=255, required=True, label="Theme Name")  # Made this required

    class Meta:
        model = Note
        fields = ['new_drug_name', 'content', 'new_theme_name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get the user from the kwargs
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        new_drug_name = self.cleaned_data.get('new_drug_name')
        drug, created = Drug.objects.get_or_create(name=new_drug_name)
        new_theme_name = self.cleaned_data.get('new_theme_name')
        theme, created = Theme.objects.get_or_create(name=new_theme_name, user=self.user)

        note = super().save(commit=False)
        note.drug = drug
        note.theme = theme
        note.user = self.user  # Assign the user here

        if commit:
            note.save()
        return note


class DosageForm(forms.ModelForm):
    new_drug_name = forms.CharField(max_length=255, required=True, label="Drug Name")

    class Meta:
        model = Dosage
        fields = ['new_drug_name', 'starting_dose', 'min_dose', 'max_dose', 'elderly_dose', 'other_adjustments']

    def save(self, commit=True):
        new_drug_name = self.cleaned_data.get('new_drug_name')
        drug, created = Drug.objects.get_or_create(name=new_drug_name)

        dosage = super().save(commit=False)
        dosage.drug = drug

        if commit:
            dosage.save()
        return dosage

class SideEffectForm(forms.ModelForm):
    PROBABILITY_CHOICES = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('very_high', 'Very High'),
    ]
    new_drug_name = forms.CharField(max_length=255, required=True, label="Drug Name")
    probability = forms.ChoiceField(choices=PROBABILITY_CHOICES)

    class Meta:
        model = SideEffect
        fields = ['new_drug_name', 'effect_description', 'probability']

    def save(self, commit=True):
        new_drug_name = self.cleaned_data.get('new_drug_name')
        drug, created = Drug.objects.get_or_create(name=new_drug_name)

        side_effect = super().save(commit=False)
        side_effect.drug = drug

        if commit:
            side_effect.save()
        return side_effect

class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = ['name']

class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['name']
