from django import test
from django.test.utils import override_settings
from django.contrib.auth.models import User
from example.models import Cat, Food, Person
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.support.ui as ui
import time


# TODO(and3rson): Add test case for foreign key (one-to-many).
class GenericTest(test.LiveServerTestCase):
    """
    Tests ability to use SearchableSelect widget
    in admin site to update many-to-many field.
    """
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.selenium = webdriver.Chrome(options=chrome_options)
        # self.selenium.maximize_window()
        super(GenericTest, self).setUp()

        self.admin = User.objects.create(username='admin', is_superuser=True, is_staff=True)
        self.admin.set_password('admin')
        self.admin.save()

        Food.objects.bulk_create([
            Food(name='Milk'),
            Food(name='Spam'),
            Food(name='Eggs'),
            Food(name='Fish'),
            Food(name='Chips'),
            Food(name='Meat'),
            Food(name='Whiskas')
        ])

        Person.objects.bulk_create([
            Person(name='Andrew'),
            Person(name='David'),
            Person(name='Mary'),
            Person(name='Matthew'),
            Person(name='Mike'),
            Person(name='Victoria')
        ])

    @override_settings(DEBUG=True)
    def test_foo(self):
        self.selenium.get(self.live_server_url + '/admin/')
        login = self.selenium.find_element_by_id('id_username')
        password = self.selenium.find_element_by_id('id_password')
        login.send_keys('admin')
        password.send_keys('admin')
        password.submit()

        wait = ui.WebDriverWait(self.selenium, 10)
        wait.until(lambda driver: driver.find_elements_by_class_name('model-cat'))

        self.selenium.get(self.live_server_url + '/admin/example/cat/add/')

        wait.until(lambda driver: driver.find_elements_by_class_name('tt-menu'))

        cat_name_input = self.selenium.find_element_by_id('id_name')
        cat_name_input.send_keys('Marusia')

        def select_food(text):
            field = self.selenium.find_element_by_id('id_favorite_foods')
            field.send_keys(text)

            wait.until(lambda driver: driver.find_elements_by_css_selector('.field-favorite_foods .tt-suggestion'))

            suggestions = self.selenium.find_elements_by_css_selector('.field-favorite_foods .tt-suggestion')
            suggestions[0].click()

            wait.until(lambda driver: driver.find_elements_by_css_selector('.field-favorite_foods .chip'))

            # Wait for suggestion animation to finish
            time.sleep(0.5)

        select_food('M')
        select_food('W')

        # Select person

        owner_field = self.selenium.find_element_by_id('id_owner')
        owner_field.send_keys('An')

        wait.until(lambda driver: driver.find_elements_by_css_selector('.field-owner .tt-suggestion'))

        owner = self.selenium.find_elements_by_css_selector('.field-owner .tt-suggestion')
        owner[0].click()

        wait.until(lambda driver: driver.find_elements_by_css_selector('.field-owner .chip'))

        # Wait for suggestion animation to finish
        time.sleep(0.5)

        wait.until(lambda driver: driver.find_elements_by_class_name('tt-suggestion'))

        # Save cat record

        self.selenium.find_elements_by_css_selector('[name="_continue"]')[0].click()

        wait.until(lambda driver: driver.find_elements_by_class_name('success'))

        marusia = Cat.objects.filter(name='Marusia').prefetch_related('favorite_foods').first()
        self.assertIsNotNone(marusia)
        favorite_foods = marusia.favorite_foods.all()
        self.assertEqual(favorite_foods.count(), 2)
        self.assertIn(favorite_foods[0].name, ('Milk', 'Meat'))
        self.assertEqual(favorite_foods[1].name, 'Whiskas')
        self.assertEqual(marusia.owner.name, 'Andrew')
