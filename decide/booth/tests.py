import time
from django.test import TestCase
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from base.tests import BaseTestCase
from base import mods
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from .views import BoothView

# Create your tests here.

class SimpleTest(TestCase):

    def test_basic_add(self):
        # test fixture
        a = 1
        b = 2

        # test case
        self.assertEqual(a+b, 3, msg='Add fuction is not correct')

class VotingDataTest(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def create_voting(self):
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    # def test_get_context_data_200(self):
    #     self.login()
    #     self.voting = self.create_voting()
    #     response = mods.get('booth/{}'.format(self.voting.pk), response=True)
    #     self.assertEqual(response.status_code, 200)

    # def test_get_context_data_not_found(self):
    #     response = self.client.get('/booth/2/')
    #     self.assertEqual(response.status_code, 404)

class AdminTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()
        self.base.tearDown()

    def test_simpleCorrectLogin(self):
        self.driver.get(f'{self.live_server_url}/admin/')
        time.sleep(5)
        self.driver.find_element(By.XPATH, "//input[@id=\'id_username\']").send_keys("admin")
        self.driver.find_element(By.XPATH, "//input[@id=\'id_password\']").send_keys("qwerty",Keys.ENTER)

        print(self.driver.current_url)

        self.assertTrue(len(self.driver.find_elements(By.XPATH, "//div[@id=\'header\']"))==1)

    def test_simpleIncorrectLogin(self):
        self.driver.get(f'{self.live_server_url}/admin/')
        time.sleep(5)
        self.driver.find_element(By.XPATH, "//input[@id=\'id_username\']").send_keys("noadmin")
        self.driver.find_element(By.XPATH, "//input[@id=\'id_password\']").send_keys("qwerty",Keys.ENTER)

        print(self.driver.current_url)

        self.assertTrue(len(self.driver.find_elements(By.XPATH, "//div[@id=\'header\']"))==0)
