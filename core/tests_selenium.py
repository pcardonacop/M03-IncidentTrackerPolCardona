import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SecurityRegressionTests(StaticLiveServerTestCase):
    fixtures = ['testdb.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument('--headless')
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_analista_no_pot_accedir_admin(self):
        # Anar a la pàgina de login de l'admin
        self.selenium.get(f'{self.live_server_url}/admin/')
        
        # Fer login
        username_input = self.selenium.find_element(By.NAME, 'username')
        username_input.send_keys('analista1')
        password_input = self.selenium.find_element(By.NAME, 'password')
        password_input.send_keys('1234')
        self.selenium.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Esperar que la URL canviï (que no sigui la de login)
        WebDriverWait(self.selenium, 5).until(
            lambda driver: driver.current_url != f'{self.live_server_url}/admin/login/'
        )

        # Comprovar si hem acabat a l'admin (vulnerabilitat)
        current_url = self.selenium.current_url
        if '/admin/' in current_url and 'login' not in current_url:
            self.fail("L'analista ha pogut accedir a l'admin (hauria d'estar prohibit)")