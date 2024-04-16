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
        #Test Case 1
        login=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/signin/']")
        login.click()
        time.sleep(2)
        Username=driver.find_element(By.ID,"username")
        Username.send_keys("lakshmi")
        password=driver.find_element(By.CSS_SELECTOR,"input#password.form-control.form-control-lg[type='password']")
        password.send_keys("$Dr1234")
        submit=driver.find_element(By.ID,"LoginBtn")
        submit.click()
        time.sleep(2)
        dashboard=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/d_dashboard/']")
        dashboard.click()
        time.sleep(2)
        # services=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='#team-section']")
        # services.click()
        # time.sleep(1)
        # tutorial=driver.find_element(By.CSS_SELECTOR,"a.test1-lin[href='/upload_video/']")
        # tutorial.click()
        # time.sleep(2)
        title=driver.find_element(By.ID,"id_title")
        title.send_keys("Video Tutorial")
        time.sleep(1)
        video_input = driver.find_element(By.CSS_SELECTOR, "input#id_video_file[type='file'][name='video_file']")
        video_path = 'C:\\Users\\irene\\Downloads\\tutorial.mp4'
        video_input.send_keys(video_path)
        time.sleep(2)
        desc=driver.find_element(By.ID,"id_description")
        desc.send_keys("Video Tutorial regarding good food")
        time.sleep(1)
        upload=driver.find_element(By.ID,"upload")
        upload.click()
        time.sleep(2)




        # profile = driver.find_element(By.CSS_SELECTOR, 'a.nav-link[href="/user_profile/"]')
        # profile.click()
        # time.sleep(2)

        # phone=driver.find_element(By.ID,"num")
        # phone.clear()
        # phone.send_keys("6282967432")
        # state=driver.find_element(By.CSS_SELECTOR,"select#state.form-control.form-control-lg[name='state'][onchange='populateDistricts()']")
        # state.click()
        # time.sleep(1)
        # kerala=driver.find_element(By.CSS_SELECTOR,"option[value='Tamil Nadu']")
        # kerala.click()
        # time.sleep(1)
        # district=driver.find_element(By.ID,"district")
        # district.click()
        # time.sleep(1)
        # sdistrict=driver.find_element(By.CSS_SELECTOR,"option[value='Coimbatore']")
        # sdistrict.click()
        # time.sleep(1)
        
        # gender=driver.find_element(By.ID,"gender")
        # gender.click()
        # time.sleep(1)
        # female=driver.find_element(By.CSS_SELECTOR,"option[value='female']")
        # female.click()
        # time.sleep(1)

        # age=driver.find_element(By.ID,"age")
        # age.clear()
        # age.send_keys("28")
        # time.sleep(2)

        # height=driver.find_element(By.ID,"height")
        # height.clear()
        # height.send_keys("164.00")
        # time.sleep(2)

        # weight=driver.find_element(By.ID,"weight")
        # weight.clear()
        # weight.send_keys("62.00")
        # time.sleep(2)
       
        # activity=driver.find_element(By.ID,"activity_level")
        # activity.click()
        # time.sleep(1)
        # sedentary=driver.find_element(By.CSS_SELECTOR,"option[value='Moderately Active']")
        # sedentary.click()
        # time.sleep(2)
        # save=driver.find_element(By.ID,"savebtn")
        # save.click()
        # time.sleep(2)

        # home=driver.find_element(By.ID,"home")
        # home.click()
        # time.sleep(2)
        # logout = driver.find_element(By.ID,"logout")
        # logout.click()
        # time.sleep(2)
# Test case 3
        # signin=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/signin/']")
        # signin.click()
        # time.sleep(2)
        # uname=driver.find_element(By.ID,"username")
        # uname.send_keys("Reena")
        # password=driver.find_element(By.CSS_SELECTOR,"input#password.form-control.form-control-lg[type='password']")
        # password.send_keys("$Dr1234")
        # login=driver.find_element(By.ID,"LoginBtn")
        # login.click()
        # time.sleep(2)
        # profile = driver.find_element(By.CSS_SELECTOR, 'a.nav-link[href="/user_profile/"]')
        # profile.click()
        # time.sleep(2)
        # book =  driver.find_element(By.CSS_SELECTOR, "a.nav-link.dropdown-toggle#bookAppointmentsDropdown")
        # book.click()
        # time.sleep(2)
        # dietitian =  driver.find_element(By.CSS_SELECTOR, "a[href='/dietitians_list/']")
        # dietitian.click()
        # time.sleep(2)
        # rate=driver.find_element(By.ID, "rate")
        # rate.click()
        # time.sleep(2)
        # comment=driver.find_element(By.ID,"review")
        # comment.send_keys("good")
        # ratesub = driver.find_element(By.ID,"submit")
        # ratesub.click()
        # time.sleep(2)
        # home = driver.find_element(By.CSS_SELECTOR, "a[href='/']")
        # home.click()
        # time.sleep(2)
        # logg = driver.find_element(By.CSS_SELECTOR, "a#logout.nav-link[href='/loggout/']")
        # logg.click()
        # time.sleep(2)

        # bkdiet=driver.find_element(By.ID, "book")
        # bkdiet.click()
        # time.sleep(2)
        # dtbook = driver.find_element(By.CSS_SELECTOR, "input[type='date'][name='session_date'].form-control[required]")
        # dtbook.sendkeys("14-12-2023")
        # dttime=driver.find_element(By.ID,"date")
        # dttime.click()
        # time.sleep(2)
        # btn = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary[type='submit']")
        # btn.click()
        # time.sleep(2)



        # prof = driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/duser_profile/']")
        # prof.click()
        # time.sleep(1)
        # services = driver.find_element(By.CSS_SELECTOR,"a.nav-link.dropdown-toggle")
        # services.click()
        # time.sleep(1)
        # slots = driver.find_element(By.ID,"addslot")
        # slots.click()
        # time.sleep(1)
        
        # add=driver.find_element(By.ID,"showSlotsFormButton")
        # add.click()
        # time.sleep(2)
        # session=driver.find_element(By.CSS_SELECTOR,"select#session[name='session']")
        # session.click()
        # time.sleep(2)
        # mrng=driver.find_element(By.CSS_SELECTOR,"option[value='Morning']")
        # mrng.click()
        # time.sleep(2)
        # times =driver.find_element(By.CSS_SELECTOR,"input#selectedTime[type='hidden'][name='time']")
        # times.click()
        # time.sleep(2)
        # sub=driver.find_element(By.CSS_SELECTOR,"button.btn-submit[type='submit']")
        # sub.click()
        # time.sleep(2)


# if __name__ == '__main__':
#        import unittest
#        unittest.main()