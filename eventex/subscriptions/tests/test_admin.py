from unittest.mock import Mock

from django.test import TestCase
from eventex.subscriptions.admin import Subscription, SubscriptionAdmin, admin


class SubscriptionAdminTest(TestCase):
    def setUp(self):
        Subscription.objects.create(
            name='Nome Fictício',
            cpf='12345678901',
            email='nome@email.com.br',
            phone='21-987654321'
        )

        self.model_admin = SubscriptionAdmin(Subscription, admin.site)

    def test_has_action(self):
        """Action mark_as_paid should be installed"""
        self.assertIn('mark_has_paid', self.model_admin.actions)

    def test_mark_all(self):
        """It should mark all selected subscription has paid"""
        self.call_action()
        self.assertEqual(1, Subscription.objects.filter(paid=True).count())

    def test_message(self):
        """It should send a message to the user"""
        mock = self.call_action()
        mock.assert_called_once_with(None, '1 inscrição foi marcada como paga.')

    def call_action(self):
        queryset = Subscription.objects.all()

        mock = Mock()
        old_message_user = SubscriptionAdmin.message_user
        SubscriptionAdmin.message_user = mock
        self.model_admin.mark_has_paid(None, queryset)
        SubscriptionAdmin.message_user = old_message_user

        return mock
