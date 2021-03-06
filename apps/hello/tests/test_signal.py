# -*- coding: utf-8 -*-
from django.test import TestCase
from hello.models import Request, ActionHistory


class TestSignal(TestCase):

    def test_create(self):
        """check signal in case create object"""
        Request.objects.create(path='/', method='GET')
        self.assertEqual(ActionHistory.objects.last().action, 'created')

    def test_edit(self):
        """check signal in case edit object"""
        req = Request.objects.create(path='/', method='GET')
        req.method = 'post'
        req.save()
        self.assertEqual(ActionHistory.objects.last().action, 'update')

    def test_deleted(self):
        """check signal in case delete object"""
        req = Request.objects.create(path='/', method='GET')
        req.delete()
        self.assertEqual(ActionHistory.objects.last().action, 'deleted')
