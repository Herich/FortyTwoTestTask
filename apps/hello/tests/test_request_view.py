# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from hello.models import Request
from django.core.urlresolvers import reverse
from django.core import serializers
import json


class TestRequestView(TestCase):
    def setUp(self):
        self.client = Client()

    def create_requests(self):
        for i in range(12):
            Request.objects.create(path='/' + str(i) + '/',
                                   method='GET',
                                   priority=i
                                   )

    def test_rendering(self):
        """check the presence of requests on page"""
        for i in range(5):
            Request.objects.create(path='/' + str(i) + '/', method='GET')
        response = self.client.get(reverse('requests'))
        self.assertIn('Requests', response.content)
        for request in Request.objects.all():
            self.assertIn(request.path, response.content)
            self.assertIn(request.method, response.content)
            self.assertIn(str(request.time)[:12], response.content)
            self.assertIn(str(request.priority), response.content)

    def test_ajax_temp(self):
        """ajax request, must to get the required requests"""
        for i in range(7):
            Request.objects.create(path='/' + str(i) + '/', method='GET')
        response = self.client.get(
            path=reverse('requests'),
            data=dict(frontend_requests='6'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        response_requests = json.loads(response.content)
        requests = serializers.serialize("json", Request.objects.all()[6:])
        self.assertEqual(response_requests, requests)

    def test_more_ten_objects(self):
        """more than 10 objects, must be present 10 objects in context"""
        for i in range(15):
            Request.objects.create(path='/' + str(i) + '/', method='GET')
        response = self.client.get(reverse('requests'))
        requests = Request.objects.all()[6:]
        self.assertEqual(response.context['requests'], list(requests))
        self.assertEqual(len(response.context['requests']), 10)

    def test_less_ten_objects(self):
        """less than 10 objects, must be present all in context"""
        for i in range(5):
            Request.objects.create(path='/' + str(i) + '/', method='GET')
        response = self.client.get(reverse('requests'))
        requests = Request.objects.all()
        self.assertEqual(response.context['requests'], list(requests))
        self.assertEqual(len(response.context['requests']), len(requests))

    def test_sort_decrease(self):
        """test in case objects are sorted in ascending"""
        self.create_requests()
        response = self.client.get('%s?order=1' % reverse('requests'))
        requests = Request.objects.all().order_by('-id')[:10]
        requests = sorted(requests, key=lambda k: k.priority)
        requests.reverse()
        self.assertEqual(list(response.context['requests']), list(requests))

    def test_sort_increase(self):
        """test in case objects are sorted in descending"""
        self.create_requests()
        response = self.client.get('%s?order=0' % reverse('requests'))
        requests = Request.objects.all().order_by('-id')[:10]
        requests = sorted(requests, key=lambda k: k.priority)
        self.assertEqual(list(response.context['requests']), list(requests))

    def test_save_priority(self):
        """check save priority"""
        self.create_requests()
        self.client.post(
            path=reverse('requests'),
            data={
                'priority': 5,
                'req_id': 1
                },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
        request = Request.objects.get(id=1)
        self.assertEqual(request.priority, 5)

    def test_validation_priority(self):
        """check priority validation"""
        self.create_requests()
        self.client.post(
            path=reverse('requests'),
            data={
                'priority': 'lol',
                'req_id': 1
                },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
        request = Request.objects.get(id=1)
        self.assertNotEqual(request.priority, 'lol')
        self.client.post(
            path=reverse('requests'),
            data={
                'priority': -5,
                'req_id': 1
                },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
        request = Request.objects.get(id=1)
        self.assertNotEqual(request.priority, -5)

    def test_json_response_save(self):
        """check json response in case valid priority"""
        self.create_requests()
        response = self.client.post(
            path=reverse('requests'),
            data={
                'priority': 5,
                'req_id': 1
                },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
        response = json.loads(response.content)
        self.assertEqual(1, response)

    def test_json_response_invalid(self):
        """check json response in case invadid priority"""
        self.create_requests()
        response = self.client.post(
            path=reverse('requests'),
            data={
                'priority': -5,
                'req_id': 1
                },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
        response = json.loads(response.content)
        self.assertEqual(0, response)

    def test_view_template(self):
        """check the use of the correct template"""
        response = self.client.get(reverse('requests'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'requests.html')
