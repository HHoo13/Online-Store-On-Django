from django import forms
from django.contrib.auth.forms import UsernameField, UserCreationForm
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _

from api.models import Buyer
from api.fields_validators import PhoneField


class TheCreateForm(UserCreationForm):
    phone_number = PhoneField(
        label=_("Phone number"),
        widget=forms.TextInput(attrs={"autocomplete": "phone_number"}),
        help_text=_("Enter your phone number."),
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        field_classes = {"username": UsernameField}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            Buyer.objects.create(phone_number=f'+{self.cleaned_data['phone_number']}', User=user)
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return user
