from django import test
from django.test.utils import override_settings
from django.contrib.auth.models import User
from example.models import Cat, Food
from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time


# TODO(and3rson): Add test case for foreign key (one-to-many).
class GenericTest(test.LiveServerTestCase):
    """
    Tests ability to use SearchableSelect widget
    in admin site to update many-to-many field.
    """
    def setUp(self):
        self.selenium = webdriver.PhantomJS()
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

            wait.until(lambda driver: driver.find_elements_by_class_name('tt-suggestion'))

            import time; time.sleep(1)

            self.selenium.save_screenshot('/tmp/1.png')

            suggestions = self.selenium.find_elements_by_class_name('tt-suggestion')
            print suggestions
            suggestions[0].click()

            time.sleep(1)

            for entry in self.selenium.get_log('browser'):
                print 'LOG:', entry['message']

            self.selenium.save_screenshot('/tmp/2.png')

            wait.until(lambda driver: driver.find_elements_by_class_name('chip'))
            # Wait for suggestion animation to finish
            time.sleep(0.5)

        select_food('M')
        select_food('W')

        cat_name_input.submit()

        wait.until(lambda driver: driver.find_elements_by_class_name('success'))

        marusia = Cat.objects.filter(name='Marusia').prefetch_related('favorite_foods').first()
        self.assertIsNotNone(marusia)
        favorite_foods = marusia.favorite_foods.all()
        self.assertEqual(favorite_foods.count(), 2)
        self.assertIn(favorite_foods[0].name, ('Milk', 'Meat'))
        self.assertEqual(favorite_foods[1].name, 'Whiskas')
