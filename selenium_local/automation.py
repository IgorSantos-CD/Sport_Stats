from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def iniciar_driver():
    driver = webdriver.Edge()
    return driver