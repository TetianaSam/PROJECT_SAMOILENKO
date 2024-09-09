from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotFound
from .models import Project, ProjectAccess
from protocols.models import Protocol
from .forms import ProjectForm, SearchForm, ProjectAccessForm
from django.contrib import messages


@login_required
def project_list(request):
    search_form = SearchForm(request.GET or None)
    projects = Project.objects.all()

    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        if query:
            projects = projects.filter(name__icontains=query)


    return render(request, 'project_list.html', {
        'projects': projects,
        'search_form': search_form
    })

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # Зберігаємо проект, але не виконуємо збереження власника
            project = form.save(commit=False)
            project.owner = request.user
            project.save()

            # Додаємо власника проекту з правами редагування
            ProjectAccess.objects.create(project=project, user=request.user, access_level=ProjectAccess.WRITE)

            return redirect('project_list')  # Перенаправлення на список проектів
        else:
            print(form.errors)  # Друк помилок форми для налагодження
    else:
        form = ProjectForm()

    return render(request, 'create_project.html', {'form': form})


@login_required
def manage_project_access(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if project.owner != request.user:
        return HttpResponseForbidden("You are not allowed to manage access for this project.")

    if request.method == 'POST':
        form = ProjectAccessForm(request.POST, project=project)
        if form.is_valid():
            access = form.save(commit=False)
            access.project = project
            access.save()
            messages.success(request, f'Access for user {access.user.username} has been added.')
            return redirect('manage_project_access', pk=pk)
    else:
        form = ProjectAccessForm(project=project)

    existing_access = project.access_permissions.all()

    return render(request, 'manage_access.html', {
        'project': project,
        'form': form,
        'existing_access': existing_access
    })


@login_required
def remove_project_access(request, project_id, user_id):
    project = get_object_or_404(Project, id=project_id)
    if project.owner != request.user:
        return HttpResponseForbidden("You are not allowed to remove access for this project.")

    access = get_object_or_404(ProjectAccess, project=project, user__id=user_id)

    if request.method == 'POST':
        access.delete()
        messages.success(request, f'Access for user {access.user.username} has been removed.')
        return redirect('manage_project_access', pk=project_id)

    return render(request, 'confirm_remove_access.html', {'access': access, 'project': project})
@login_required
def view_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # Перевірка прав доступу для перегляду
    if project.owner != request.user and not ProjectAccess.objects.filter(project=project, user=request.user,
                                                                          access_level__in=[ProjectAccess.READ,
                                                                                            ProjectAccess.WRITE]).exists():
        return HttpResponseForbidden("You are not allowed to view this project.")

    protocols = project.protocols.all()  # Використовуємо related_name='protocols' з ManyToManyField
#notes = note.notes.all()TO DO?????
    return render(request, 'view_project.html', {'project': project, 'protocols': protocols})

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if project.owner != request.user and not ProjectAccess.objects.filter(project=project, user=request.user,
                                                                          access_level=ProjectAccess.WRITE).exists():
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
    return render(request, 'confirm_delete_project.html', {'project': project})

@login_required
def project_notes(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Check permissions
    if project.owner != request.user and not ProjectAccess.objects.filter(
        project=project, user=request.user, access_level__in=[ProjectAccess.READ, ProjectAccess.WRITE]
    ).exists():
        return HttpResponseForbidden("You are not allowed to view this project.")

    notes = project.notes.all()

    return render(request, 'project_notes.html', {
        'project': project,
        'notes': notes
    })