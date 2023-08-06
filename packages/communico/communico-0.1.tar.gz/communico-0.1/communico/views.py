from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import forms


def contact_form_view(request):
    form = forms.ContactForm()
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['message'],
                '{name} <{email}>'.format(**form.cleaned_data),
                [settings.EMAIL_HOST_USER]
            )
            return HttpResponseRedirect(reverse('communico:contact'))
    return render(request, 'communico/contact_form.html', {'form': form})
