# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.forms.formsets import formset_factory, BaseFormSet
from django.core.context_processors import csrf
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from webgui.form import *
from utils.random_cocktail import *
from utils.check_form import *
from utils.rpi_api_call import *


def homepage(request):
    """
    Homepage of the Bar Pi app. Show all availlable coktail
    :param request: metadata about the request
    :return: Homepage
    """
    cocktails = Cocktail.objects.all()
    return render(request, 'homepage.html', {'coktails': cocktails})


def create_cocktail(request):
    # This class is used to make empty formset forms required
    # See http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/4951032#4951032
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    BottleItemFormSet = formset_factory(BottleItemForm, max_num=10, formset=RequiredFormSet)

    if request.method == 'POST':  # If the form has been submitted...
        bottle_list_form = CoktailForm(request.POST)  # A form bound to the POST data
        # Create a formset from the submitted data
        cocktail_item_formset = BottleItemFormSet(request.POST, request.FILES)
        # check form is ok
        if bottle_list_form.is_valid() and cocktail_item_formset.is_valid():
            # check total volume does not exceed 20 cl
            if is_total_volume_exceed_20cl(cocktail_item_formset):
                messages.add_message(request, messages.ERROR,
                                     "Le volume total doit etre inférieur ou égal à 20 cl",
                                     extra_tags='warning')
            else:
                # check not multiple same bottle
                if is_same_bootle_in_list(cocktail_item_formset):
                    messages.add_message(request, messages.ERROR,
                                         "Ne pas utiliser une bouteille plus d'une fois dans le même cocktail",
                                         extra_tags='warning')
                else:
                    # Everything ok, create the cocktail
                    cocktail = Cocktail()
                    cocktail.lock = False
                    cocktail.name = bottle_list_form.cleaned_data['name']
                    cocktail.save()

                    for form in cocktail_item_formset.forms:
                        volume = form.cleaned_data['volume']
                        bottle = Bottle.objects.get(id=form.cleaned_data['bottle'].id)
                        info_cocktail = Cocktailinfo(bottle=bottle, cocktail=cocktail, volume=volume)
                        info_cocktail.save()
                    messages.add_message(request, messages.SUCCESS, "Cocktail créé avec succès")
                    return redirect('webgui.views.homepage')
    else:
        bottle_list_form = CoktailForm()
        cocktail_item_formset = BottleItemFormSet()

    c = {'bottle_list_form': bottle_list_form,
         'cocktail_item_formset': cocktail_item_formset,
        }
    c.update(csrf(request))
    return render(request, 'create_cocktail.html', c)


def delete_cocktail(request, id):
    cocktail = Cocktail.objects.get(id=id)
    cocktail.delete()
    messages.add_message(request, messages.SUCCESS, "Cocktail supprimé", extra_tags='info')
    return redirect('webgui.views.homepage')


def login_page(request):
    if request.POST:
        form = LoginForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password, request=request)
            print "authenticate user :"+str(user)
            if user is not None:
                login(request, user)
                return redirect('webgui.views.admin_homepage')
            else:
                messages.add_message(request, messages.ERROR, "Login ou mot de passe invalide", extra_tags='danger')
                form = LoginForm()  # An unbound form
                return render(request, 'login_form.html', {'form': form})
        else:
            messages.add_message(request, messages.ERROR, "Login ou mot de passe invalide", extra_tags='danger')
            return render(request, 'login_form.html', {'form': form})

    else:
        form = LoginForm()  # An unbound form
        return render(request, 'login_form.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('webgui.views.homepage')


@login_required(login_url='/login/')
def admin_homepage(request):
    bottles = Bottle.objects.all().order_by('slot')
    return render(request, 'admin_homepage.html', {'bottles': bottles})


@login_required(login_url='/login/')
def delete_bottle(request, id):
    bottle = Bottle.objects.get(id=id)
    cocktails = Cocktail.objects.filter(bottles=id)
    if request.POST:
        # remove cocktail
        for cocktail in cocktails:
            cocktail.delete()
        # remove bottle
        bottle = Bottle.objects.get(id=id)
        bottle.delete()
        messages.add_message(request, messages.SUCCESS,
                             "Bouteille supprimée",
                             extra_tags='info')
        return redirect('webgui.views.admin_homepage')
    else:
        return render(request, 'delete_bottle.html', {'bottle': bottle, 'cocktails': cocktails})


@login_required(login_url='/login/')
def create_bottle(request):
    if request.POST:
        form = BottleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Bouteille ajoutée")
            return redirect('webgui.views.admin_homepage')
    else:
        form = BottleForm()
    return render(request, 'create_bottle.html', {'form': form})


@login_required(login_url='/login/')
def update_bottle(request, id):
    bottle = get_object_or_404(Bottle, id=id)
    form = BottleForm(request.POST or None, instance=bottle)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS,
                             "Bouteille mise à jour",
                             extra_tags='info')
        return redirect('webgui.views.admin_homepage')
    return render(request, "update_bottle.html", {'form': form,
                                                  'bottle': bottle})


def run_cocktail(request, id):
    # get cocktail by id
    cocktail = Cocktail.objects.get(id=id)
    # create JSON payload from cocktail object
    payload = get_playload_from_cocktail(cocktail)

    # call rasp lib
    response = call_api('/make_cocktail', payload)

    if response["status"] == "ok":
        # Get the max time from the bigger volume. * 100 to get it in seconde
        max_time = get_highter_volume(cocktail) * 1000
        return render(request, "run_cocktail.html", {'max_time': max_time,
                                                     'cocktail': cocktail})
    else:
        messages.add_message(request, messages.ERROR,
                             "Raspidrink est occupé",
                             extra_tags='warning')
        return redirect('webgui.views.homepage')


def run_random(request):
    # get all cocktail
    cocktails = Cocktail.objects.all()
    if len(cocktails) < 1:
        messages.add_message(request, messages.ERROR,
                             "Aucun cocktail dans le système",
                             extra_tags='warning')
        return redirect('webgui.views.homepage')
    else:
        # take a cocktail randomly
        cocktail = random.choice(cocktails)
        # create JSON payload from cocktail object
        payload = get_playload_from_cocktail(cocktail)

        # call rasp lib
        response = call_api('/make_cocktail', payload)

        if response["status"] == "ok":
            # Get the max time from the bigger volume. * 1000 to get it in seconde
            max_time = get_highter_volume(cocktail) * 1000
            return render(request, "run_cocktail.html", {'max_time': max_time,
                                                         'cocktail': cocktail})
        else:
            messages.add_message(request, messages.ERROR,
                                 "Raspidrink est occupé",
                                 extra_tags='warning')
            return redirect('webgui.views.homepage')


def run_coffin(request):
    # get all bottle
    bottles = Bottle.objects.all()

    # get the number of total bottle to take random
    number_of_bottle = len(bottles)

    if number_of_bottle < 1:
        messages.add_message(request, messages.ERROR,
                             "Aucune bouteille dans le système",
                             extra_tags='warning')
        return redirect('webgui.views.homepage')
    else:
        # get a randomly created cocktail
        bottles = get_random_cocktail(bottles, number_of_bottle)
        # prepare json payload
        payload = {'data': []}
        payload.update({'data': bottles})
        # call rasp lib
        response = call_api('/make_cocktail', payload)

        if response["status"] == "ok":
            # TODO: get max time from the bigger volume
            max_time = get_highter_volume(bottles) * 1000
            return render(request, "run_coffin.html", {'max_time': max_time,
                                                       'bottles': bottles})

        else:
            messages.add_message(request, messages.ERROR,
                                 "Raspidrink est occupé",
                                 extra_tags='warning')
            return redirect('webgui.views.homepage')

