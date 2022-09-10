from django import forms

class CreateNewList(forms.Form):
    # all available forms: https://docs.djangoproject.com/en/4.1/topics/forms/

    # label (optional) shows up before the field/box
    name = forms.CharField(label='Name', max_length=255)
    # creates a check field/button
    check = forms.BooleanField(required=False)