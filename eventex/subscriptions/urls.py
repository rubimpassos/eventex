from django.conf.urls import url

from eventex.subscriptions.views import new, detail, thank_you


app_name = 'subscriptions'
urlpatterns = [
    url(r'^$', new, name='new'),
    url(r'^(?P<pk>\d+)/$', detail, name='detail'),
    url(r'^obrigado/$', thank_you, name='thank-you'),
]
