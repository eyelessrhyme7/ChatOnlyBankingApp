from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import undetected_chromedriver as ue
import selenium.webdriver as webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import os
import streamlit as st
from streamlit import session_state as state
import requests
import openai
import pandas as pd
from bs4 import BeautifulSoup
import datetime
from numpy import nan
from io import BytesIO
import re

# THIS FILE CONTAINS DEBUGGING CODE, NOT USED IN THE CURRENT PROJECT IMPLEMENTATION

username = ''
passwrd = ''

#Chrome is tested and works as of now. Using undetected-chromedriver. Not using installable webdriver software. Using portable undetected-chromedriver. Only requirement is browser installation, not driver.
driver_c = ue.Chrome()
driver_c.maximize_window()
driver_c.get("https://internet-banking.dbs.com.sg/IB/Welcome")

username_input = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="UID"]"""))).send_keys(username)
password_input = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="PIN"]"""))).send_keys(passwrd)
login_button = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """/html/body/form[1]/div/div[7]/button[1]"""))).click()

print(0)

time.sleep(5)

print(6)
aut_button = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="AuthenticatBtnId"]"""))).click()

print(1)
#Pay
# pay_button = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="topnav2"]/div[1]/h4"""))).click()
# javascript_code = "javascript:goToState('000000000000226','d1e4acbf0a5b19b60166afb390f9f6d4','RetrievemWalletDetails');"
# driver_c.execute_script(javascript_code)

# print(1.4)
# #Paylah
# paylah_button = WebDriverWait(driver_c, 100).until(EC.presence_of_element_located((By.XPATH, """/html/body/section[5]/div/div[1]/div[1]/div[1]/div/ul/li/a"""))).click()
# print(2)
# #Paylah input
# paylah_input = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """/html/body/form[1]/section[2]/div/div/div[1]/div[7]/div[2]/input"""))).send_keys("5")
# print(3)
# #Paylah button
# paylah_submit = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="fetchDetailsButton"]"""))).click()
# print(4)
# #Confirm
# paylah_confirm = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="fetchDetailsButton"]"""))).click()
# print(5)
# #success-text
# # driver_c.find_element_by_xpath("""/html/body/section[2]/div/div/div[1]/div[1]/div/p/span[2]""")
# success_text = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """/html/body/section[2]/div/div/div[1]/div[1]/div/p/span[2]"""))).text
# print(success_text)