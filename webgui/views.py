# -*- coding: utf-8 -*-
from random import randint

from django.shortcuts import render, redirect, get_object_or_404
from django.forms.formsets import formset_factory, BaseFormSet
from django.core.context_processors import csrf
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from webgui.form import *
from utils.random_cocktail import *
from utils.check_form import *
import json
from requests import put, get, post
from django.conf import settings
from utils.get_highter import get_highter_volume


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
    payload = {'data': []}
    table_bottle_slot_dict = []
    for bottle in cocktail.bottles.all():
        info = Cocktailinfo.objects.get(bottle=bottle, cocktail=cocktail)
        bottle_slot_dict = {'slot_id': bottle.slot, 'volume': info.volume}
        table_bottle_slot_dict.append(bottle_slot_dict)
        payload.update({'data': table_bottle_slot_dict})

    # call rasp lib
    url = 'http://'+settings.RPI_IP+':5000'
    headers = {'content-type': 'application/json'}

    # create cocktail payload to send to the RPI API
    r = post(url+'/make_cocktail', data=json.dumps(payload), headers=headers)

    # decode json response. This give a string
    response = json.loads(r.text)

    if response["status"] =="ok":
        # Get the max time from the bigger volume. * 100 to get it in seconde
        max_time = get_highter_volume(table_bottle_slot_dict) * 1000
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
        # TODO: call rasp lib
        max_time = 1000
        return render(request, "run_cocktail.html", {'max_time': max_time,
                                                     'cocktail': cocktail})


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
        # random a number of bottle from 1 to the maximum bottle available
        list_size = randint(1, number_of_bottle)
        # the sum value is tne total volume. In ou case is always 20 cl
        list_sum_value = 20

        # get list of random number
        random_list_with_zero = rand_int_vec(list_size,
                                             list_sum_value,
                                             distribution=rand_floats(list_size))
        # remove zero in this list
        random_list = []
        for el in random_list_with_zero:
            if el != 0:
                random_list.append(el)

        number_of_bottle = len(random_list)
        print "number of bottle used: "+str(len(random_list))
        print "list: "+str(random_list)

        # get randomly item in the list switch the list_size
        bottles = set(bottles)
        bottles_selected = random.sample(bottles, number_of_bottle)
        print bottles_selected

        # we cannot use the Cocktail object without saving it
        bottles = []
        i = 0
        for bottle in bottles_selected:
            list_bottle_volume = {'bottle_name': bottle.name, 'volume': random_list[i]}
            bottles.append(list_bottle_volume)
            i += 1

        # TODO: get max time from the bigger volume
        # TODO: call rasp lib
        max_time = 1000
        print bottles
        return render(request, "run_coffin.html", {'max_time': max_time,
                                                   'bottles': bottles})


