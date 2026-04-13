from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Task
from .forms import TaskForm

def index(request):
    search_input = request.GET.get('search-area') or ''
    filter_category = request.GET.get('category-filter') or ''
    
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    # 1. On récupère toutes les tâches pour les calculs de stats
    all_taches = Task.objects.all()
    
    # 2. Filtrage pour l'affichage
    taches_display = all_taches.filter(title__icontains=search_input)
    if filter_category:
        taches_display = taches_display.filter(category=filter_category)
    
    # 3. Tri (Non-terminées -> Urgentes -> Date d'échéance)
    taches_display = taches_display.order_by('completed', '-priority', 'due_date')

    # Statistiques pour les badges
    stats = {
        'Travail': all_taches.filter(category='TRAVAIL', completed=False).count(),
        'Loisirs': all_taches.filter(category='LOISIRS', completed=False).count(),
        'Courses': all_taches.filter(category='COURSES', completed=False).count(),
    }

    # Calcul de la progression globale
    progression = 0
    total_count = all_taches.count()
    if total_count > 0:
        progression = int((all_taches.filter(completed=True).count() / total_count) * 100)
    
    context = {
        'taches': taches_display,
        'form': TaskForm(),
        'search_input': search_input,
        'progression': progression,
        'maintenant': timezone.now(),
        'limite_proche': timezone.now() + timedelta(hours=24),
        'stats': stats,
        'filter_category': filter_category
    }
    return render(request, 'macronote/list.html', context)

def delete_task(request, pk):
    get_object_or_404(Task, pk=pk).delete()
    return redirect('home')

def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    return redirect('home')

def delete_all(request):
    Task.objects.all().delete()
    return redirect('home')