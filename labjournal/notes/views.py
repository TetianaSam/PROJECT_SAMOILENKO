from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponse
from .models import Notes, NoteAccess,NoteFile
from .forms import NotesForm, SearchForm, NoteAccessForm,NoteFileFormSet
from django.contrib import messages
from django.db.models import Q


@login_required
def notes_list(request):
    search_form = SearchForm(request.GET or None)
    notes = Notes.objects.all()

    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        date_from = search_form.cleaned_data.get('date_from')
        date_to = search_form.cleaned_data.get('date_to')
        note_topic = search_form.cleaned_data.get('note_topic')
        sort_by = search_form.cleaned_data.get('sort_by')

        filters = Q()

        if date_from:
            filters &= Q(created_at__gte=date_from)  # Use &= to ensure all conditions are met

        if date_to:
            filters &= Q(created_at__lte=date_to)

        if note_topic:
            filters &= Q(note_topic__icontains=note_topic)

        notes = notes.filter(filters).distinct()

        # Validate and restrict sort_by values to prevent potential security issues
        allowed_sort_fields = ['created_at', 'note_topic']  # Example fields
        if sort_by in allowed_sort_fields:
            notes = notes.order_by(sort_by)

    return render(request, 'notes_list.html', {
        'notes': notes,
        'search_form': search_form
    })
@login_required
def create_note(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        file_formset = NoteFileFormSet(request.POST, request.FILES, queryset=NoteFile.objects.none())

        if form.is_valid() and file_formset.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
            note.save()

            for file_form in file_formset:
                if file_form.cleaned_data.get('file'):
                    file_instance = file_form.save(commit=False)
                    file_instance.note = note
                    file_instance.save()

            # Create an entry for note access, giving the user edit permissions
            NoteAccess.objects.create(note=note, user=request.user, access_level=NoteAccess.WRITE)

            # Redirect to notes list page
            return redirect('notes_list')

    else:
        form = NotesForm()
        file_formset = NoteFileFormSet(queryset=NoteFile.objects.none())

    return render(request, 'create_note.html', {
        'form': form,
        'file_formset': file_formset
    })
@login_required
def manage_note_access(request, pk):
    note = get_object_or_404(Notes, pk=pk)

    if note.owner != request.user:
        return HttpResponseForbidden("You are not allowed to manage access to this note.")

    if request.method == 'POST':
        form = NoteAccessForm(request.POST, note=note)
        if form.is_valid():
            access = form.save(commit=False)
            access.note = note
            access.save()
            messages.success(request, f'Access for user {access.user.username} has been added.')
            return redirect('manage_note_access', pk=pk)
    else:
        form = NoteAccessForm(note=note)

    existing_access = note.access_permissions.all()

    return render(request, 'manage_access_note.html', {
        'note': note,
        'form': form,
        'existing_access': existing_access
    })


@login_required
def remove_note_access(request, note_id, user_id):
    note = get_object_or_404(Notes, id=note_id)
    if note.owner != request.user:
        return HttpResponseForbidden("You are not allowed to remove access to this note.")

    access = get_object_or_404(NoteAccess, note=note, user__id=user_id)

    if request.method == 'POST':
        access.delete()
        messages.success(request, f'Access for user {access.user.username} has been removed.')
        return redirect('manage_note_access', pk=note_id)

    return render(request, 'confirm_remove_access_note.html', {'access': access, 'note': note})
@login_required
def view_note(request, pk):
    note = get_object_or_404(Notes, pk=pk)

    if note.owner != request.user and not NoteAccess.objects.filter(
            note=note,
            user=request.user,
            access_level__in=[NoteAccess.READ, NoteAccess.WRITE]
    ).exists():
        return HttpResponseForbidden("You are not allowed to view this note.")

    # Отримання всіх проектів, протоколів, реагентів і витратних матеріалів
    projects = note.projects.all()
    protocols = note.protocols.all()
    reagents = note.reagents.all()
    consumables = note.consumables.all()

    return render(request, 'view_note.html', {
        'note': note,
        'projects': projects,
        'protocols': protocols,
        'reagents': reagents,
        'consumables': consumables,
    })
@login_required
def edit_note(request, pk):
    note = get_object_or_404(Notes, pk=pk)

    if note.owner != request.user and not NoteAccess.objects.filter(note=note, user=request.user,
                                                                          access_level=NoteAccess.WRITE).exists():
        return HttpResponseForbidden("You are not allowed to edit this note.")

    if request.method == 'POST':
        form = NotesForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes_list')
    else:
        form = NotesForm(instance=note)

    return render(request, 'edit_note.html', {'form': form, 'note': note})
@login_required
def delete_note(request, pk):
    note = get_object_or_404(Notes, pk=pk)

    if note.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this note.")

    if request.method == 'POST':
        note.delete()
        return redirect('notes_list')
    return render(request, 'confirm_delete_note.html', {'note': note})

def search_notes(request):
    form = SearchForm(request.GET or None)
    notes = Notes.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        projects = form.cleaned_data.get('projects')
        note_topic = form.cleaned_data.get('note_topic')

        filters = Q()

        if query:
            filters |= Q(note_text__icontains=query)  # Пошук за текстом нотатки

        if date_from:
            filters |= Q(created_at__gte=date_from)

        if date_to:
            filters |= Q(created_at__lte=date_to)

        if projects:
            filters |= Q(projects__in=projects)

        if note_topic:
            filters |= Q(note_topic__icontains=note_topic)

        notes = notes.filter(filters).distinct()

    return render(request, 'your_template.html', {'form': form, 'notes': notes})