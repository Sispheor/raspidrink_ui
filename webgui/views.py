# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from models import Bottle, Cocktail, Cocktailinfo
from webgui.form import *
from django.forms.formsets import formset_factory, BaseFormSet
from django.core.context_processors import csrf
from django.contrib import messages

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

        if bottle_list_form.is_valid() and cocktail_item_formset.is_valid():
            # create the cocktail
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


