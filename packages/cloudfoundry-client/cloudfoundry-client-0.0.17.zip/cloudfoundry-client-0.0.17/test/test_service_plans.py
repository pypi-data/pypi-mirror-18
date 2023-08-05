import httplib
import sys
import unittest

import mock

import cloudfoundry_client.main as main
from abstract_test_case import AbstractTestCase
from fake_requests import mock_response


class TestServicePlans(unittest.TestCase, AbstractTestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_client_class()

    def setUp(self):
        self.build_client()

    def test_list(self):
        self.client.get.return_value = mock_response(
            '/v2/service_plans?q=service_guid%20IN%20service_id',
            httplib.OK,
            None,
            'v2', 'service_plans', 'GET_response.json')
        cpt = reduce(lambda increment, _: increment + 1, self.client.service_plans.list(service_guid='service_id'), 0)
        self.client.get.assert_called_with(self.client.get.return_value.url)
        self.assertEqual(cpt, 1)

    def test_get(self):
        self.client.get.return_value = mock_response(
            '/v2/service_plans/plan_id',
            httplib.OK,
            None,
            'v2', 'service_plans', 'GET_{id}_response.json')
        result = self.client.service_plans.get('plan_id')
        self.client.get.assert_called_with(self.client.get.return_value.url)
        self.assertIsNotNone(result)

    def test_list_instances(self):
        self.client.get.return_value = mock_response(
            '/v2/service_plans/plan_id/service_instances?q=space_guid%20IN%20space_id',
            httplib.OK,
            None,
            'v2', 'apps', 'GET_{id}_routes_response.json')
        cpt = reduce(lambda increment, _: increment + 1,
                     self.client.service_plans.list_instances('plan_id', space_guid='space_id'), 0)
        self.client.get.assert_called_with(self.client.get.return_value.url)
        self.assertEqual(cpt, 1)

    def test_entity(self):
        self.client.get.side_effect = [
            mock_response(
                '/v2/service_plans/plan_id',
                httplib.OK,
                None,
                'v2', 'service_plans', 'GET_{id}_response.json'),
            mock_response(
                '/v2/services/6a4abae6-93e0-438b-aaa2-5ae67f3a069d',
                httplib.OK,
                None,
                'v2', 'services', 'GET_{id}_response.json')
            ,
            mock_response(
                '/v2/service_plans/5d8f3b0f-6b5b-487f-8fed-4c2d9b812a72/service_instances',
                httplib.OK,
                None,
                'v2', 'service_instances', 'GET_response.json')
        ]
        service_plan = self.client.service_plans.get('plan_id')

        self.assertIsNotNone(service_plan.service())
        cpt = reduce(lambda increment, _: increment + 1, service_plan.service_instances(), 0)
        self.assertEqual(cpt, 1)
        self.client.get.assert_has_calls([mock.call(side_effect.url) for side_effect in self.client.get.side_effect],
                                         any_order=False)

    @mock.patch.object(sys, 'argv', ['main', 'list_service_plans'])
    def test_main_list_service_plans(self):
        with mock.patch('cloudfoundry_client.main.build_client_from_configuration',
                        new=lambda: self.client):
            self.client.get.return_value = mock_response('/v2/service_plans',
                                                         httplib.OK,
                                                         None,
                                                         'v2', 'service_plans', 'GET_response.json')
            main.main()
            self.client.get.assert_called_with(self.client.get.return_value.url)

    @mock.patch.object(sys, 'argv', ['main', 'get_service_plan', '5d8f3b0f-6b5b-487f-8fed-4c2d9b812a72'])
    def test_main_get_service_plan(self):
        with mock.patch('cloudfoundry_client.main.build_client_from_configuration',
                        new=lambda: self.client):
            self.client.get.return_value = mock_response('/v2/service_plans/5d8f3b0f-6b5b-487f-8fed-4c2d9b812a72',
                                                         httplib.OK,
                                                         None,
                                                         'v2', 'service_plans', 'GET_{id}_response.json')
            main.main()
            self.client.get.assert_called_with(self.client.get.return_value.url)


