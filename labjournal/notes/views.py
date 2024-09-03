from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotFound
from .models import Notes, NoteAccess
from .forms import NotesForm, SearchForm, NoteAccessForm
from django.contrib import messages
from projects.models import Project
from protocols.models import Protocol
from reagents.models import Reagents
from reagents.models import Consumables



@login_required
def notes_list(request):
    search_form = SearchForm(request.GET or None)
    notes = Notes.objects.all()

    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        if query:
            notes = notes.filter(name__icontains=query)


    return render(request, 'notes_list.html', {
        'notes': notes,
        'search_form': search_form
    })

@login_required
def create_note(request):
    if request.method == 'POST':
        form = NotesForm(request.POST, request.FILES)
        if form.is_valid():
            # Create note instance but do not save to the database yet
            note = form.save(commit=False)
            note.owner = request.user  # Assign current user as the owner
            note.save()  # Save the note to the database

            # Create an entry for note access, giving the user edit permissions
            NoteAccess.objects.create(note=note, user=request.user, access_level=NoteAccess.WRITE)

            # Redirect to notes list page
            return redirect('notes_list')
        else:
            # Log form errors for debugging purposes
            print(form.errors)
    else:
        # Initialize an empty form for GET request
        form = NotesForm()

    # Render the form on the create_note.html template
    return render(request, 'create_note.html', {'form': form})
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

    # Перевірка прав доступу для перегляду
    if note.owner != request.user and not NoteAccess.objects.filter(note = note, user=request.user,
                                                                          access_level__in=[NoteAccess.READ,
                                                                                            NoteAccess.WRITE]).exists():
        return HttpResponseForbidden("You are not allowed to view this project.")

    notes = note.protocols.all()
    notes = note.projects.all()
    notes = note.reagents.all()
    notes = note.consumables.all()

    return render(request, 'view_note.html', {'note': note, 'project': project, 'protocols': protocols, 'reagent':reagent, 'consumable':consumable})

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

