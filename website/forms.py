from django import forms

from .models import IncomingMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = IncomingMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Nama harus terdiri dari minimal 2 karakter.")
        return name

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError("Pesan harus terdiri dari minimal 10 karakter.")
        return message
