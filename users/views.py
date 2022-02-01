from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import connection
from django.conf import settings
from django.contrib.auth.models import User
from .forms import UserForm

@login_required
def index(request):
    # Ordre :
    order_by = request.GET.get('sort', 'last_name')
    queryset = User.objects.all().order_by(order_by)

    # Pagination :
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'order_by': order_by,
        'conn': connection,
        'debug': settings.DEBUG
    }
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        context['layout'] = 'layouts/ajax.html'
    else:
        context['layout'] = 'layouts/default.html'
        context['tab'] = 'users'

    return render(request, 'Users/index.html', context)

@login_required
def add(request):
    context = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/users')
        else:
            context['error_message'] = 'Utilisateur n’a pas pu être ajouté! Veuillez réessayer.'
    else:
        form = UserForm()
    context['form'] = form

    return render(request, 'Users/add.html', context)

@login_required
def edit(request, id):
    user = get_object_or_404(User, pk=id)
    form = UserForm(request.POST or None, instance=user)
    context = {}

    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(request.POST.get('password'))
            user.is_active = True
            user.save()
            return redirect('/users')
        else:
            context['error_message'] = 'Utilisateur n’a pas pu être modifié! Veuillez réessayer.'
            print(form.errors)

    context['form'] = form

    return render(request, 'Users/edit.html', context)

@login_required
def delete(request, id):
    user = get_object_or_404(User, pk=id)
    user.delete()
    return redirect('/users')