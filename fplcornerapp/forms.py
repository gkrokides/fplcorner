from django import forms
from captcha.fields import CaptchaField

# from .models import *
# from django.utils import timezone


class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    captcha = CaptchaField()
