from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Nome Fictício', cpf='12345678901', email='nome@email.com.br', phone='21-987654321')
        self.response = self.client.post(r('subscriptions:new'), data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'nome@email.com.br']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = ['Nome Fictício', '12345678901', 'nome@email.com.br', '21-987654321']
        for expected in contents:
            with self.subTest():
                self.assertIn(expected, self.email.body)
