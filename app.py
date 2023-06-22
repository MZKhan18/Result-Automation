import streamlit as st
import pickle
import pandas as pd
import time
import matplotlib.pyplot as plt
from PIL import Image

from selenium import webdriver
from selenium.webdriver import  chrome
from selenium.webdriver.common.by import By
from  selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import  ChromeDriverManager
import os


st.title("RESULT AUTOMATION")

#fetching enroll number and student id
def fetch_data(number,student_data):
    finalDf = student_data[student_data['mobile'] == number]
    if finalDf.shape[0]==0:
        student_present = False
    else:
        student_present = True
    student_id_value = ""
    for i in finalDf['id']:
        student_id_value = i
    student_enroll_value = ""
    for i in finalDf['enroll']:
        student_enroll_value = i
    return student_id_value,student_enroll_value, student_present

#importing dataset
student_dict = pickle.load(open('student_data.pkl','rb'))
student_data= pd.DataFrame(student_dict)


#getting phone number
# student_present = True
number = st.number_input("Enter Phone number : ")

student_id_value , student_enroll_value, student_present = fetch_data(number,student_data)

# selenium automation code starts:
if st.button("Show Result"):
    if student_present:
        with st.spinner("loading result....."):
            # os.environ['PATH'] += r"C:\Advance Programming\Selenium Drivers"
            # service = Service(ChromeDriverManager().install()

            options = webdriver.ChromeOptions()
            # options.add_argument("--headless")
            options.add_experimental_option("detach", True)
            options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            # chrome_driver_binary = r"C:\Advance Programming\Selenium Drivers\chromedriver.exe"
            service = Service(executable_path=r"C:\Advance Programming\Selenium Drivers\chromedriver.exe")
            driver = webdriver.Chrome(service = service ,options=options)

            driver.get("https://sstcerp.conicworks.com/examform.php?slug=bef46a916b627ca922729d235571228e")
            driver.implicitly_wait(3)
            student_id = driver.find_element(By.ID, "student_id")

            student_id.send_keys(student_id_value)
            enroll_no = driver.find_element(By.ID, "enroll_no_id")
            enroll_no.send_keys(student_enroll_value)
            button = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div/div[2]/div[1]/div[3]/button')
            button.click()

            driver.implicitly_wait(3)
            regular_button = driver.find_element(By.CLASS_NAME, "mr-3")
            regular_button.click()

            driver.implicitly_wait(3)
            result_button = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div/div[5]/a/button')
            result_button.click()

            driver.implicitly_wait(3)
            time.sleep(10)
            driver.save_screenshot("my-result-1.png")
            img = Image.open('my-result-1.png')
            box = (400, 50, 1230, 900)
            img2 = img.crop(box)
            img2.save('myimage_cropped.png')
            # img2.show()
            st.image(img2)
            driver.close()

    else:
        st.error('Student Not Found!', icon="🚨")






