from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, DosageForm, SideEffectForm, NoteForm, ThemeForm
from .models import Dosage, SideEffect, Note, Theme
from django.core.mail import send_mail

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, DosageForm, SideEffectForm, NoteForm, DrugForm
from .models import Dosage, SideEffect, Note, Drug, Theme

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'medical_helper_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'medical_helper_app/login.html', {'form': form})

@login_required
def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    dosages = Dosage.objects.filter(user=request.user)
    side_effects = SideEffect.objects.filter(user=request.user)
    notes = Note.objects.filter(user=request.user)
    
    context = {
        'dosages': dosages,
        'side_effects': side_effects,
        'notes': notes,
    }
    return render(request, 'medical_helper_app/index.html', context)
@login_required
def dosage_view(request):
    if request.method == 'POST':
        form = DosageForm(request.POST)
        if form.is_valid():
            dosage = form.save(commit=False)
            dosage.user = request.user
            dosage.save()
            return redirect('home')
    else:
        form = DosageForm()
    return render(request, 'medical_helper_app/dosage.html', {'form': form})

@login_required
def side_effect_view(request):
    if request.method == 'POST':
        form = SideEffectForm(request.POST)
        if form.is_valid():
            side_effect = form.save(commit=False)
            side_effect.user = request.user
            side_effect.save()
            return redirect('home')
    else:
        form = SideEffectForm()
    return render(request, 'medical_helper_app/side_effects.html', {'form': form})

@login_required
def notes_view(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, user=request.user)  # Pass the user to the form
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NoteForm(user=request.user)  # Pass the user to the form
    return render(request, 'medical_helper_app/notes.html', {'form': form})

# Email Content View
@login_required
def send_content_via_email(request):
    if request.method == 'POST':
        dosage_content = Dosage.objects.filter(user=request.user)
        side_effect_content = SideEffect.objects.filter(user=request.user)
        notes_content = Note.objects.filter(user=request.user)

        email_content = "Dosages:\n"
        for dosage in dosage_content:
            email_content += f"{dosage.drug_name}: Start {dosage.starting_dose}, Min {dosage.min_dose}, Max {dosage.max_dose}\n"

        email_content += "\nSide Effects:\n"
        for side_effect in side_effect_content:
            email_content += f"{side_effect.drug_name}: {side_effect.effect_description}, Probability {side_effect.probability}\n"

        email_content += "\nNotes:\n"
        for note in notes_content:
            email_content += f"{note.drug_name}: {note.content} (Theme: {note.theme.name})\n"

        send_mail(
            'Your Medical Helper Information',
            email_content,
            'audra991@yahoo.com',
            [request.user.email],
            fail_silently=False,
        )

        return redirect('home')
    return render(request, 'email.html')
