from django import forms
from .models import LunchBox
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TypeUserForm(forms.Form):
    id_user = forms.IntegerField()
    level = forms.IntegerField()


class TypeForm(forms.Form):
    level = forms.IntegerField()


class LunchBoxForm(forms.ModelForm):

    class Meta:
        model = LunchBox
        fields = ('title', 'img', 'description', 'price', 'addition')


class NumberOfLunchBoxForm(forms.Form):
    id_lunchbox = forms.IntegerField()
    number = forms.IntegerField()


class DelLunchBoxForm(forms.Form):
    del_lunchbox = forms.IntegerField()


class DelUserForm(forms.Form):
    id_user = forms.IntegerField()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class DelOrderForm(forms.Form):
    id_del = forms.IntegerField()


class ReadyOrderForm(forms.Form):
    id_ready = forms.IntegerField()


class SearchOrderForm(forms.Form):
    id_search = forms.IntegerField()


class StatusBusy(forms.Form):
    id_status= forms.IntegerField()