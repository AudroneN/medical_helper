from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, DosageForm, SideEffectForm, NoteForm, ThemeForm
from .models import Dosage, SideEffect, Note, Theme
from django.core.mail import send_mail

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, DosageForm, SideEffectForm, NoteForm, DrugForm
from .models import Dosage, SideEffect, Note, Drug, Theme

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
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('home')
    else:
        form = NoteForm()
    return render(request, 'medical_helper_app/notes.html', {'form': form})


# Register View
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html', {'form': form})

# Login View
def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'medical_helper_app/login.html', {'form': form})



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
            'from@example.com',
            [request.user.email],
            fail_silently=False,
        )

        return redirect('home')
    return render(request, 'email.html')
