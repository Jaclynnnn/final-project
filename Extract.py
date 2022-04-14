from time import sleep, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

def openWhatsapp():
    driver = webdriver.Chrome(executable_path="C:\\chromedriver.exe")
    driver.get("https://web.whatsapp.com/")
    driver.maximize_window()
    print("please scan QR code and press Enter")
    input()
    print("Logged in!")

