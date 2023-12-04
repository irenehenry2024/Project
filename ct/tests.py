from datetime import datetime
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Hosttest(TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/'

    def tearDown(self):
        self.driver.quit()
        
    def test_01_login_page(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(1)
        
        login=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/signin/']")
        login.click()
        time.sleep(2)
        Username=driver.find_element(By.ID,"username")
        Username.send_keys("Reena")
        password=driver.find_element(By.CSS_SELECTOR,"input#password.form-control.form-control-lg[type='password']")
        password.send_keys("$Dr1234")
        # presubmit=driver.find_element(By.CSS_SELECTOR,"img.img-fluid")
        # presubmit.click()
        submit=driver.find_element(By.ID,"LoginBtn")
        submit.click()
        time.sleep(2)
        profile=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/user_profile/']")
        profile.click()
        time.sleep(2)

        phone=driver.find_element(By.CSS_SELECTOR,"input#num.form-control.form-control-lg[type='text'][value='8547528289']")
        phone.clear()
        phone.send_keys("6282935321")
        state=driver.find_element(By.ID,"state")
        state.click()
        time.sleep(1)
        state=driver.find_element(By.CSS_SELECTOR,"option[value='Tamil Nadu']")
        state.click()
        time.sleep(1)
        
        district=driver.find_element(By.ID,"district")
        district.click()
        time.sleep(1)
        district=driver.find_element(By.CSS_SELECTOR,"option[value='Coimbatore']")
        district.click()
        time.sleep(1)
        
        gender=driver.find_element(By.ID,"gender")
        gender.click()
        time.sleep(1)
        gender=driver.find_element(By.CSS_SELECTOR,"option[value='female']")
        gender.click()
        time.sleep(1)

        age=driver.find_element(By.ID,"age")
        age.clear()
        age.send_keys("28")

        height=driver.find_element(By.ID,"height")
        height.clear()
        height.send_keys("164.00")

        weight=driver.find_element(By.ID,"weight")
        weight.clear()
        weight.send_keys("62.00")
       
        activity=driver.find_element(By.ID,"activity_level")
        activity.click()
        time.sleep(1)
        activity=driver.find_element(By.CSS_SELECTOR,"option[value='Moderately Active']")
        activity.click()
        time.sleep(1)
        save=driver.find_element(By.ID,"savebtn")
        save.click()
        time.sleep(2)
        home=driver.find_element(By.CSS_SELECTOR,"a[href='/']")
        home.click()
        time.sleep(2)
       

if __name__ == '__main__':
       import unittest
       unittest.main()