from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service

def iniciar_driver(log_level = 3):
    options = Options()
    options.add_argument(f"--log-level={log_level}")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--headless")

    service = Service(executable_path="./webdrivers/msedgedriver.exe")
    driver = webdriver.Edge(options=options, service=service)
    return driver