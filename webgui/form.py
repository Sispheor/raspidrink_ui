# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import ModelForm, HiddenInput, widgets
from django import forms
from webgui.models import Cocktail, Bottle, Cocktailinfo
from django.forms.models import modelformset_factory
from django.core.validators import MinValueValidator, MaxValueValidator


class CoktailForm(forms.Form):

    name = forms.CharField(label="Nom du cocktail",
                           min_length=2,
                           max_length=100,
                           required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control input-sm'}))


class BottleItemForm(forms.Form):
    bottle = forms.ModelChoiceField(label="Bouteille",
                                    queryset=Bottle.objects.all(),
                                    required=True,
                                    widget=forms.Select(attrs={'class': 'form-control'}))

    volume = forms.IntegerField(label="Volume en cl",
                                validators=[MinValueValidator(1), MaxValueValidator(20)],
                                widget=forms.NumberInput(attrs={'class': 'form-control input-sm'}))


class LoginForm(forms.Form):
    username = forms.CharField(label="Login",
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control login-field',
                                                             'placeholder': 'Login'}))

    password = forms.CharField(label="Mot de passe",
                               required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control login-field',
                                                                 'placeholder': 'Password'}))


class BottleForm(ModelForm):
    name = forms.CharField(label="Nom",
                           required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Exemple: Vodka'}))
    slot = forms.IntegerField(label="Slot",
                              widget=forms.NumberInput(attrs={'class': 'form-control input-sm'}))

    class Meta:
        model = Bottle
        fields = ['name', 'slot']


class ConfirmCoffin(forms.Form):
    confirm_checkbox = forms.BooleanField(initial=False,
                                          required=True,
                                          label="Confirmation",
                                          widget=forms.CheckboxInput(attrs={'class': 'form-control'}))


