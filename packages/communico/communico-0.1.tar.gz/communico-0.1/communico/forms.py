from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label='Your name', required=True)
    email = forms.EmailField(
            label='Your e-Mail',
            help_text='Please, enter a valid email address.')
    subject = forms.CharField(required=True)
    message = forms.CharField(
            label='Your message',
            required=True,
            widget=forms.Textarea)
