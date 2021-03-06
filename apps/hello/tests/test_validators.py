# -*- coding: utf-8 -*-
from django.test import TestCase
from hello.models import UserData
from django.core.exceptions import ValidationError


class TestValidators(TestCase):

    def setUp(self):
        UserData.objects.create(
            first_name="Andrei11",
            last_name="Herasko22",
            date_of_birth='2017-05-23',
            bio="bio",
            email="andrey.herasmail.com",
            jabber="hectorcc.co",
            skype="%%244",
            other_contacts="other"
        )
        self.data = UserData.objects.first()

    def test_validate_name(self):
        """check that we can only pass alphabetic
        characters in first_name/last_name field"""
        with self.assertRaisesMessage(
                ValidationError,
                'Enter a valid name.'):
            self.data.clean_fields()

    def test_validate_email(self):
        """check that we can't pass with the wrong email"""
        with self.assertRaisesMessage(
                ValidationError,
                'Enter a valid email address.'):
            self.data.clean_fields()

    def test_validate_jabber(self):
        """check that we can't pass with the wrong jabber"""
        with self.assertRaisesMessage(
                ValidationError,
                'Enter a valid jabber.'):
            self.data.clean_fields()

    def test_validate_skype(self):
        """check that we can't pass with the wrong skype"""
        with self.assertRaisesMessage(
                ValidationError,
                'Enter a valid skype.'):
            self.data.clean_fields()

    def test_validate_date_of_birth(self):
        """check date validation"""
        with self.assertRaisesMessage(
                ValidationError,
                'Enter your real date of birth!'):
            self.data.clean_fields()
