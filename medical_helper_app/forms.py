from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Dosage, SideEffect, Note, Theme, Drug
class CustomUserCreationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class DosageForm(forms.ModelForm):
    new_drug_name = forms.CharField(max_length=255, required=False, label="Or enter a new drug name")

    class Meta:
        model = Dosage
        fields = ['drug', 'new_drug_name', 'starting_dose', 'min_dose', 'max_dose', 'elderly_dose', 'other_adjustments']

    def save(self, commit=True):
        drug = self.cleaned_data.get('drug')
        new_drug_name = self.cleaned_data.get('new_drug_name')

        if new_drug_name:
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
    new_drug_name = forms.CharField(max_length=255, required=False, label="Or enter a new drug name")
    probability = forms.ChoiceField(choices=PROBABILITY_CHOICES)

    class Meta:
        model = SideEffect
        fields = ['drug', 'new_drug_name', 'effect_description', 'probability']

    def save(self, commit=True):
        drug = self.cleaned_data.get('drug')
        new_drug_name = self.cleaned_data.get('new_drug_name')

        if new_drug_name:
            drug, created = Drug.objects.get_or_create(name=new_drug_name)

        side_effect = super().save(commit=False)
        side_effect.drug = drug

        if commit:
            side_effect.save()
        return side_effect

class NoteForm(forms.ModelForm):
    new_drug_name = forms.CharField(max_length=255, required=False, label="Or enter a new drug name")
    new_theme_name = forms.CharField(max_length=255, required=False, label="Or enter a new theme name")

    class Meta:
        model = Note
        fields = ['drug', 'new_drug_name', 'content', 'theme', 'new_theme_name']

    def save(self, commit=True):
        drug = self.cleaned_data.get('drug')
        new_drug_name = self.cleaned_data.get('new_drug_name')
        theme = self.cleaned_data.get('theme')
        new_theme_name = self.cleaned_data.get('new_theme_name')

        if new_drug_name:
            drug, created = Drug.objects.get_or_create(name=new_drug_name)
        
        if new_theme_name:
            theme, created = Theme.objects.get_or_create(name=new_theme_name, user=self.instance.user)

        note = super().save(commit=False)
        note.drug = drug
        note.theme = theme

        if commit:
            note.save()
        return note

class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = ['name']

class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['name']
