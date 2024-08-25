from django import forms
from .models import Dosage, SideEffect, Note, Theme, Drug
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = ['name']

class DosageForm(forms.ModelForm):
    drug = forms.ModelChoiceField(queryset=Drug.objects.all(), empty_label="Select a drug")

    class Meta:
        model = Dosage
        fields = ['drug', 'starting_dose', 'min_dose', 'max_dose', 'elderly_dose', 'other_adjustments']

class SideEffectForm(forms.ModelForm):
    drug = forms.ModelChoiceField(queryset=Drug.objects.all(), empty_label="Select a drug")

    class Meta:
        model = SideEffect
        fields = ['drug', 'effect_description', 'probability']

class NoteForm(forms.ModelForm):
    drug = forms.ModelChoiceField(queryset=Drug.objects.all(), empty_label="Select a drug")

    class Meta:
        model = Note
        fields = ['drug', 'content', 'theme']

class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['name']
