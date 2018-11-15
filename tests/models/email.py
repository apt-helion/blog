# Imports {{{1
from unittest import TestCase

from common.models.email import *
from datetime import date


class EmailTest(TestCase):
    """Email tests and stuff like that"""


    def setUp(self):
        self.email = 'test@email.com'
        self.email_verification = None


    def tearDown(self):
        if isinstance(self.email_verification, EmailVerifications): self.email_verification.delete_instance()


    def test_create_verification(self):
        self.email_verification = EmailVerifications.create_verification(self.email)
        self.assertEqual(self.email_verification.email, self.email, "Incorrect email")
        self.assertEqual(len(self.email_verification.code), 32, "Incorrect uuid value")
