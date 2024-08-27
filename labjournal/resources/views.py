from django.shortcuts import render, redirect, get_object_or_404
from .models import Resource, Suggestion
from .forms import ResourceForm, SuggestionForm, SearchForm
from django.contrib.auth.decorators import login_required


def resource_list(request):
    search_form = SearchForm(request.GET or None)
    resources = Resource.objects.all()

    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        if query:
            resources = resources.filter(description__icontains=query)  # Пошук по опису ресурсу

    application_area = request.GET.get('application_area', '')
    if application_area:
        resources = resources.filter(application_area__icontains=application_area)

    return render(request, 'resource_list.html', {
        'resources': resources,
        'search_form': search_form
    })


@login_required
def add_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('resource_list')
    else:
        form = ResourceForm()
    return render(request, 'add_resource.html', {'form': form})


@login_required
def edit_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        form = ResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('resource_list')
    else:
        form = ResourceForm(instance=resource)
    return render(request, 'edit_resource.html', {'form': form, 'resource': resource})


@login_required
def delete_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        resource.delete()
        return redirect('resource_list')
    return render(request, 'confirm_delete.html', {'resource': resource})


@login_required
def suggestion_list(request):
    suggestions = Suggestion.objects.filter(reviewed=False)
    return render(request, 'suggestion_list.html', {'suggestions': suggestions})


@login_required
def add_suggestion(request):
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('suggestion_list')
    else:
        form = SuggestionForm()
    return render(request, 'add_suggestion.html', {'form': form})


@login_required
def review_suggestion(request, pk):
    suggestion = get_object_or_404(Suggestion, pk=pk)
    if request.method == 'POST':
        suggestion.reviewed = True
        suggestion.save()
        return redirect('suggestion_list')
    return render(request, 'review_suggestion.html', {'suggestion': suggestion})
