__author__ = 'sebastienclaeys'

from django.test.simple import DjangoTestSuiteRunner
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from abc import abstractmethod

# Custom test runner which prevent creation and destruction of a mirror test database
class TestRunner(DjangoTestSuiteRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        self.setup_test_environment()
        suite = self.build_suite(test_labels, extra_tests)
        # old_config = self.setup_databases()
        result = self.run_suite(suite)
        # self.teardown_databases(old_config)
        self.teardown_test_environment()
        return self.suite_result(suite, result)


class LoggedInTestCase(TestCase):
    def setUp(self):
        # Set the user to me - pk=1
        self.user = User.objects.get(pk=1)



# Custom Test Case to simply implement a basic test for a view giving the view function and the arguments
# Example:
# class Ab_exp_statusTestCase(ViewTestCase):
#    def pre_test(self):
#        self.view = views.ab_exp_status
#        self.view_args = (1,)
#
class ViewTestCase(LoggedInTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        super(ViewTestCase, self).setUp()

    # Must be overwrited and setting view and view_args
    @abstractmethod
    def pre_test(self):
        self.view = None
        self.view_args = None


    def test_details(self):
        # Set custom view and args
        self.pre_test()

        # Build the request
        request = self.factory.get(reverse(self.view, args=self.view_args))

        # Assign superuser to act like we are logged in
        request.user = self.user

        # Test the view
        response = self.view(request, *self.view_args)
        self.assertEqual(response.status_code, 200)



