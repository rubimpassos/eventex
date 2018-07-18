from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):
    def test_form_has_field(self):
        """Form must have 4 fields"""
        expected = ['name', 'cpf', 'email', 'phone']
        form = SubscriptionForm()
        self.assertSequenceEqual(expected, list(form.fields))

    def test_is_digit(self):
        """CPF must only accept digit"""
        form = self.make_validated_form(cpf='ABCD5678901')
        self.assertFormErrorCode(form, 'cpf', 'digits')

    def test_cpf_has_11_digits(self):
        """CPF must have 11 digits"""
        form = self.make_validated_form(cpf='1234')
        self.assertFormErrorCode(form, 'cpf', 'length')

    def test_name_must_be_capitalized(self):
        """Name must be capitalized"""
        form = self.make_validated_form(name='RUBI mendes')
        self.assertEqual('Rubi Mendes', form.cleaned_data['name'])

    def test_email_is_optional(self):
        """Email is optional"""
        form = self.make_validated_form(email='')
        self.assertFalse(form.errors)

    def test_phone_is_optional(self):
        """Phone is optional"""
        form = self.make_validated_form(phone='')
        self.assertFalse(form.errors)

    def test_must_informe_email_or_phone(self):
        """Email and phone are optionals, must one must be informed"""
        form = self.make_validated_form(email='', phone='')
        self.assertFormErrorCode(form, '__all__', 'email_or_phone')

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

    def assertFormErrorMessage(self, form, field, msg):
        erros = form.errors
        erros_list = erros[field]
        self.assertListEqual([msg], erros_list)

    def make_validated_form(self, **kwargs):
        valid = dict(name='Nome Fictício', cpf='12345678901', email='nome@email.com.br', phone='21-987654321')
        data = dict(valid, **kwargs)
        form = SubscriptionForm(data)
        form.is_valid()
        return form
