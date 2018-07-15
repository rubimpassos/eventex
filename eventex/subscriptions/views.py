from django.conf import settings
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)


def create(request):
    form = SubscriptionForm(request.POST)
    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html', {'form': form})

    subscription = Subscription.objects.create(**form.cleaned_data)

    request.session['subscription_pk'] = subscription.pk

    # Send email
    _send_mail('Confirmação de inscrição',
               settings.DEFAULT_FROM_EMAIL,
               subscription.email,
               'subscriptions/subscription_email.txt',
               {'subscription': subscription})

    return HttpResponseRedirect('/inscricao/obrigado/')


def new(request):
    return render(request, 'subscriptions/subscription_form.html', {'form': SubscriptionForm()})


def detail(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)
    return render(request, 'subscriptions/subscription_detail.html', {'subscription': subscription})


def thank_you(request):
    if 'subscription_pk' not in request.session:
        return HttpResponseRedirect('/inscricao/')

    subscription = get_object_or_404(Subscription, pk=request.session['subscription_pk'])
    del request.session['subscription_pk']
    return render(request, 'subscriptions/subscription_detail.html', {'subscription': subscription})


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])
