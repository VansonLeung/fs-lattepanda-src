import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import requests

# https://stackoverflow.com/questions/48007699/how-to-allow-or-deny-notification-geo-location-microphone-camera-pop-up
option = Options()
option.add_argument("--disabl-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
option.add_experimental_option("detach", True)
#option.add_argument("headless")

option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1,
    "profile.default_content_setting_values.notifications": 1
  })
#
driver = webdriver.Chrome("/usr/bin/chromedriver", options=option)

count = 0

try:
    myip = requests.get('https://www.wikipedia.org').headers['X-Client-IP']
    print(myip)
    response = requests.post('https://formulasquare.com/api/etc/create_signals.php', data={'ip': myip, 'status': 1, 'msg': 'starting' })
except Exception as e:
    print(e)

while True:
    try:
        driver.get("https://localhost:8080/build/callapp.html?a=asdf&audio=false&video=true")


        try:
            myip = requests.get('https://www.wikipedia.org').headers['X-Client-IP']
            print(myip)
            response = requests.post('https://formulasquare.com/api/etc/create_signals.php', data={'ip': myip, 'status': 1, 'msg': 'webrtc booting' })
        except Exception as e:
            print(e)


        try:
            time.sleep(1)
            button = driver.find_element(By.ID, "details-button")
            button.click()
        except Exception as e:
            print(e)


        time.sleep(3)

        try:
            link = driver.find_element(By.ID, "proceed-link")
            link.click()
        except Exception as e:
            print(e)


        button = driver.find_element(By.ID, "request_permission")
        button.click()

        time.sleep(1)

        driver.refresh()

        button = driver.find_element(By.ID, "select_video_source_refresh")
        button.click()


        dropdown = Select(driver.find_element(By.ID, "select_video_size"))
        # dropdown = driver.find_element(By.ID, "select_video_size")
        dropdown.select_by_index(0)

        time.sleep(3)

        try:
            button = driver.find_element(By.CLASS_NAME, "callapp_button")
            button.click()
            print("ASSA")
        except Exception as e:
            print(e)
            myip = requests.get('https://www.wikipedia.org').headers['X-Client-IP']
            print(myip)
            raise e
            #response = requests.post('https://formulasquare.com/api/etc/create_signals.php', data={'ip': myip, 'status': -1, 'msg': 'camera not ready?' })


        try:
            myip = requests.get('https://www.wikipedia.org').headers['X-Client-IP']
            print(myip)
            #response = requests.post('https://formulasquare.com/api/etc/create_signals.php', data={'ip': myip, 'status': 2, 'msg': 'webrtc ready' })
        except Exception as e:
            print(e)
            raise e


        time.sleep(10)
        break
    except Exception as e:
        print(e)
        count += 1
        if count > 15:
            count = 0

            try:

                myip = requests.get('https://www.wikipedia.org').headers['X-Client-IP']
                print(myip)
                #response = requests.post('https://formulasquare.com/api/etc/create_signals.php', data={'ip': myip, 'status': -1, 'msg': 'failed to connect webrtc browser' })
            except Exception as e:
                print(e)

        time.sleep(2)
        driver.refresh();


