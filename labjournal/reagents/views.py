from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Reagents, Consumables, ReagentsAccess, ConsumablesAccess
from .forms import ReagentsForm, ConsumablesForm, ReagentsAccessForm, ConsumablesAccessForm, SearchForm
from django.contrib import messages


@login_required
def reagents_list(request):
    search_form = SearchForm(request.GET or None)
    reagents = Reagents.objects.all()

    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        if query:
            reagents = reagents.filter(name__icontains=query)

    return render(request, 'reagents/reagents_list.html', {
        'reagents': reagents,
        'search_form': search_form
    })


@login_required
def consumables_list(request):
    search_form = SearchForm(request.GET or None)
    consumables = Consumables.objects.all()

    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        if query:
            consumables = consumables.filter(name__icontains=query)

    return render(request, 'consumables/consumables_list.html', {
        'consumables': consumables,
        'search_form': search_form
    })


@login_required
def create_reagent(request):
    if request.method == 'POST':
        form = ReagentsForm(request.POST, request.FILES)
        if form.is_valid():
            reagent = form.save(commit=False)
            reagent.owner = request.user
            reagent.save()

            ReagentsAccess.objects.create(reagent=reagent, user=request.user, access_level=ReagentsAccess.WRITE)

            return redirect('reagents_list')
    else:
        form = ReagentsForm()

    return render(request, 'reagents/create_reagent.html', {'form': form})


@login_required
def create_consumable(request):
    if request.method == 'POST':
        form = ConsumablesForm(request.POST, request.FILES)
        if form.is_valid():
            consumable = form.save(commit=False)
            consumable.owner = request.user
            consumable.save()

            ConsumablesAccess.objects.create(consumable=consumable, user=request.user, access_level=ConsumablesAccess.WRITE)

            return redirect('consumables_list')
    else:
        form = ConsumablesForm()

    return render(request, 'consumables/create_consumable.html', {'form': form})


@login_required
def manage_reagent_access(request, pk):
    reagent = get_object_or_404(Reagents, pk=pk)

    if reagent.owner != request.user:
        return HttpResponseForbidden("You are not allowed to manage access for this reagent.")

    if request.method == 'POST':
        form = ReagentsAccessForm(request.POST, instance=reagent)
        if form.is_valid():
            access = form.save(commit=False)
            access.reagent = reagent
            access.save()
            messages.success(request, f'Access for user {access.user.username} has been added.')
            return redirect('manage_reagent_access', pk=pk)
    else:
        form = ReagentsAccessForm()

    existing_access = reagent.access_permissions.all()

    return render(request, 'reagents/manage_access.html', {
        'reagent': reagent,
        'form': form,
        'existing_access': existing_access
    })


@login_required
def manage_consumable_access(request, pk):
    consumable = get_object_or_404(Consumables, pk=pk)

    if consumable.owner != request.user:
        return HttpResponseForbidden("You are not allowed to manage access for this consumable.")

    if request.method == 'POST':
        form = ConsumablesAccessForm(request.POST, instance=consumable)
        if form.is_valid():
            access = form.save(commit=False)
            access.consumable = consumable
            access.save()
            messages.success(request, f'Access for user {access.user.username} has been added.')
            return redirect('manage_consumable_access', pk=pk)
    else:
        form = ConsumablesAccessForm()

    existing_access = consumable.access_permissions.all()

    return render(request, 'consumables/manage_access.html', {
        'consumable': consumable,
        'form': form,
        'existing_access': existing_access
    })


@login_required
def remove_reagent_access(request, reagent_id, user_id):
    reagent = get_object_or_404(Reagents, id=reagent_id)
    if reagent.owner != request.user:
        return HttpResponseForbidden("You are not allowed to remove access for this reagent.")

    access = get_object_or_404(ReagentsAccess, reagent=reagent, user__id=user_id)

    if request.method == 'POST':
        access.delete()
        messages.success(request, f'Access for user {access.user.username} has been removed.')
        return redirect('manage_reagent_access', pk=reagent_id)

    return render(request, 'reagents/confirm_remove_access.html', {'access': access, 'reagent': reagent})


@login_required
def remove_consumable_access(request, consumable_id, user_id):
    consumable = get_object_or_404(Consumables, id=consumable_id)
    if consumable.owner != request.user:
        return HttpResponseForbidden("You are not allowed to remove access for this consumable.")

    access = get_object_or_404(ConsumablesAccess, consumable=consumable, user__id=user_id)

    if request.method == 'POST':
        access.delete()
        messages.success(request, f'Access for user {access.user.username} has been removed.')
        return redirect('manage_consumable_access', pk=consumable_id)

    return render(request, 'consumables/confirm_remove_access.html', {'access': access, 'consumable': consumable})


@login_required
def view_reagent(request, pk):
    reagent = get_object_or_404(Reagents, pk=pk)

    if reagent.owner != request.user and not ReagentsAccess.objects.filter(reagent=reagent, user=request.user,
                                                                          access_level__in=[ReagentsAccess.READ,
                                                                                            ReagentsAccess.WRITE]).exists():
        return HttpResponseForbidden("You are not allowed to view this reagent.")

    return render(request, 'reagents/view_reagent.html', {'reagent': reagent})


@login_required
def view_consumable(request, pk):
    consumable = get_object_or_404(Consumables, pk=pk)

    if consumable.owner != request.user and not ConsumablesAccess.objects.filter(consumable=consumable, user=request.user,
                                                                          access_level__in=[ConsumablesAccess.READ,
                                                                                            ConsumablesAccess.WRITE]).exists():
        return HttpResponseForbidden("You are not allowed to view this consumable.")

    return render(request, 'consumables/view_consumable.html', {'consumable': consumable})


@login_required
def edit_reagent(request, pk):
    reagent = get_object_or_404(Reagents, pk=pk)

    if reagent.owner != request.user and not ReagentsAccess.objects.filter(reagent=reagent, user=request.user,
                                                                          access_level=ReagentsAccess.WRITE).exists():
        return HttpResponseForbidden("You are not allowed to edit this reagent.")

    if request.method == 'POST':
        form = ReagentsForm(request.POST, request.FILES, instance=reagent)
        if form.is_valid():
            form.save()
            return redirect('reagents_list')
    else:
        form = ReagentsForm(instance=reagent)

    return render(request, 'reagents/edit_reagent.html', {'form': form, 'reagent': reagent})


@login_required
def edit_consumable(request, pk):
    consumable = get_object_or_404(Consumables, pk=pk)

    if consumable.owner != request.user and not ConsumablesAccess.objects.filter(consumable=consumable, user=request.user,
                                                                          access_level=ConsumablesAccess.WRITE).exists():
        return HttpResponseForbidden("You are not allowed to edit this consumable.")

    if request.method == 'POST':
        form = ConsumablesForm(request.POST, request.FILES, instance=consumable)
        if form.is_valid():
            form.save()
            return redirect('consumables_list')
    else:
        form = ConsumablesForm(instance=consumable)

    return render(request, 'consumables/edit_consumable.html', {'form': form, 'consumable': consumable})


@login_required
def delete_reagent(request, pk):
    reagent = get_object_or_404(Reagents, pk=pk)

    if reagent.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this reagent.")

    if request.method == 'POST':
        reagent.delete()
        return redirect('reagents_list')

    return render(request, 'reagents/confirm_delete.html', {'reagent': reagent})


@login_required
def delete_consumable(request, pk):
    consumable = get_object_or_404(Consumables, pk=pk)

    if consumable.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this consumable.")

    if request.method == 'POST':
        consumable.delete()
        return redirect('consumables_list')

    return render(request, 'consumables/confirm_delete.html', {'consumable': consumable})
