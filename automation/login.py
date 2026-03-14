from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
import time 
class Login:
    def start_login(self):
        """Abre Firefox y navega al portal CiDi. Devuelve el objeto webdriver.Firefox para que el llamador pueda interactuar con la sesión si lo desea. """
        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.get("https://cidi.cba.gov.ar/portal-publico/")
        return driver

