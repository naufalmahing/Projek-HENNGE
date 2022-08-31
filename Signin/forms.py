from django import forms

class ResetPassword(forms.Form):
    password = forms.CharField(label="Password", max_length=200)