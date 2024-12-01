from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.utils import timezone
from datetime import timedelta
from .models import UserProfile, Questionnaire, Playlist
from .forms import UserProfileForm, QuestionnaireForm, UserRegistrationForm, PlaylistForm
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie

def home(request):
    return render(request, 'home.html')

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')

@ensure_csrf_cookie
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Registration successful!')
                return redirect('questionnaire')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
                return render(request, 'auth/register.html', {'form': form})
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})

@login_required
def questionnaire(request):
    # Check if user has completed a questionnaire in the last 24 hours
    last_questionnaire = Questionnaire.objects.filter(
        user=request.user,
        date__gte=timezone.now() - timedelta(days=1)
    ).first()
    
    if last_questionnaire:
        messages.info(request, 'Já completou um questionário nas últimas 24 horas!')
        return redirect('results')
    
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            questionnaire = form.save(commit=False)
            questionnaire.user = request.user
            questionnaire.date = timezone.now()
            
            # Calculate mood and energy levels based on form data
            questionnaire.mood = (
                int(form.cleaned_data['anxiety_level']) +
                int(form.cleaned_data['stress_level']) +
                int(form.cleaned_data['happiness_level'])
            ) / 3
            
            questionnaire.energy_level = (
                int(form.cleaned_data['physical_energy']) +
                int(form.cleaned_data['mental_energy'])
            ) / 2
            
            questionnaire.save()
            
            # Create a playlist based on questionnaire results
            playlist = create_playlist(questionnaire)
            
            messages.success(request, 'Questionário completado com sucesso!')
            return redirect('results')
    else:
        form = QuestionnaireForm()
    
    return render(request, 'questionnaire/questionnaire.html', {
        'form': form,
        'title': 'Questionário de Humor Musical'
    })

@login_required
def profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    user_playlists = Playlist.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'form': form,
        'profile': user_profile,
        'recent_playlists': user_playlists
    }
    
    return render(request, 'user/profile.html', context)


@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'user/edit_profile.html', {'form': form})

@login_required
def playlists(request):
    user_playlists = Playlist.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user/playlists.html', {'playlists': user_playlists})

@login_required
def playlist_detail(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk, user=request.user)
    return render(request, 'user/playlist_detail.html', {'playlist': playlist})

@login_required
def edit_playlist(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PlaylistForm(request.POST, instance=playlist)
        if form.is_valid():
            form.save()
            messages.success(request, 'Playlist atualizada com sucesso!')
            return redirect('playlist_detail', pk=playlist.pk)
    else:
        form = PlaylistForm(instance=playlist)
    return render(request, 'user/edit_playlist.html', {'form': form, 'playlist': playlist})

@login_required
def results(request):
    latest_questionnaire = Questionnaire.objects.filter(user=request.user).latest('date')
    latest_playlist = Playlist.objects.filter(questionnaire=latest_questionnaire).first()
    return render(request, 'questionnaire/results.html', {
        'questionnaire': latest_questionnaire,
        'playlist': latest_playlist
    })

def get_mood_recommendations(mood_score):
    recommendations = {
        'motivacional': {
            'songs': ['Firework - Katy Perry', 'Eye of the Tiger - Survivor', 'Stronger - Kelly Clarkson'],
            'description': 'Músicas motivacionais para elevar seu astral'
        },
        'calmo': {
            'songs': ['Weightless - Marconi Union', 'River Flows in You - Yiruma', 'Claire de Lune - Debussy'],
            'description': 'Melodias suaves para relaxamento'
        },
        'alegre': {
            'songs': ['Happy - Pharrell Williams', "Can't Stop the Feeling - Justin Timberlake", 'Uptown Funk - Mark Ronson'],
            'description': 'Músicas animadas para manter o alto astral'
        },
        'energético': {
            'songs': ['Titanium - David Guetta', 'Levels - Avicii', 'Don\'t Stop Believin\' - Journey'],
            'description': 'Hits energéticos para manter o ritmo'
        }
    }
    
    if mood_score <= 1.5:
        return 'motivacional', recommendations['motivacional']
    elif mood_score <= 2.5:
        return 'calmo', recommendations['calmo']
    elif mood_score <= 3.5:
        return 'alegre', recommendations['alegre']
    else:
        return 'energético', recommendations['energético']

def create_playlist(questionnaire):
    mood_score = (
        questionnaire.mood +
        questionnaire.anxiety_level +
        questionnaire.social_level +
        questionnaire.energy_level
    ) / 4

    mood_category, recommendations = get_mood_recommendations(mood_score)

    return Playlist.objects.create(
        user=questionnaire.user,
        questionnaire=questionnaire,
        title=f"Playlist {mood_category.title()} - {timezone.now().strftime('%d/%m/%Y')}",
        description=recommendations['description'],
        songs=recommendations['songs'],
        mood_category=mood_category
    )
