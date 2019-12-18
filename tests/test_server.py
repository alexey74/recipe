from django.test.testcases import TestCase
from django.urls.base import reverse
import json
import yaml


class OpenAPISchemaTestCase(TestCase):
    def test_schema_has_valid_title(self):
        response = self.client.get(reverse('openapi-schema') + '?format=openapi')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(yaml.load(response.content)['info']['title'], 'Recipe Project')
