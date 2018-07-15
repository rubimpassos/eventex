from django.test import TestCase
from django.shortcuts import resolve_url as r

from eventex.subscriptions.models import Subscription


class ThankYouPageGet(TestCase):
    def setUp(self):
        self.obj = Subscription.objects.create(
            name='Nome Fictício',
            cpf='12345678901',
            email='nome@email.com.br',
            phone='21-987654321'
        )
        session = self.client.session
        session['subscription_pk'] = self.obj.pk
        session.save()
        self.response = self.client.get(r('subscriptions:thank-you'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_detail.html')

    def test_context(self):
        expected = self.response.context['subscription']
        self.assertIsInstance(expected, Subscription)

    def test_context_data(self):
        contents = [self.obj.name, self.obj.cpf, self.obj.email, self.obj.phone]
        for expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected)

    def test_session_destroyed(self):
        """Must destroy subscription_pk session var after get"""
        self.assertNotIn('subscription_pk', self.client.session)


class ThankYouPageSessionNotFound(TestCase):
    def setUp(self):
        self.response = self.client.get(r('subscriptions:thank-you'))

    def test_session_not_found_redirect(self):
        self.assertRedirects(self.response, r('subscriptions:new'))


class ThankYouPageSubscriptionNotFound(TestCase):
    def setUp(self):
        session = self.client.session
        session['subscription_pk'] = 0
        session.save()
        self.response = self.client.get(r('subscriptions:thank-you'))

    def test_subscription_not_found(self):
        self.assertEqual(404, self.response.status_code)
