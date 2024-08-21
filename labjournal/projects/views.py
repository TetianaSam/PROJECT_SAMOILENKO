from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotFound
from .models import Project
from .forms import ProjectForm, SearchForm

@login_required
def project_list(request):
    search_form = SearchForm(request.GET or None)
    projects = Project.objects.all()

    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        if query:
            projects = projects.filter(name__icontains=query)  # Пошук по назві проекту

    return render(request, 'project_list.html', {
        'projects': projects,
        'search_form': search_form
    })

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user  # Встановлюємо власника проекту
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()

    return render(request, 'create_project.html', {'form': form})

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if project.owner != request.user:
        return HttpResponseForbidden("You are not allowed to edit this project.")

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'edit_project.html', {'form': form, 'project': project})

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if project.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this project.")

    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'confirm_delete.html', {'project': project})

@login_required
def view_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if not project:
        return HttpResponseNotFound("Project not found")

    # Перевірка прав доступу для перегляду
    if project.owner != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to view this project.")

    return render(request, 'view_project.html', {'project': project})
