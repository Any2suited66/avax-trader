from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from chromedriver_py import binary_path
from selenium_stealth import stealth
from re import sub
from decimal import Decimal
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
svc = webdriver.ChromeService(executable_path=binary_path)
browser = webdriver.Chrome(service=svc, options=options)

stealth(browser,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
browser.implicitly_wait(30)
browser.get('https://www.core.app/')
sleep(5)
browser.find_element(By.XPATH, "//*[contains(text(), 'Connect Wallet')]").click()
browser.find_element(By.CSS_SELECTOR, "[data-testid='connect-core-mobile-button']").click()
browser.find_element(By.CSS_SELECTOR, "[data-testid='connect-terms-checkbox']").click()
sleep(2)
browser.find_element(By.CSS_SELECTOR, "[data-testid='connect-terms-continue-btn']").click()
while True:
    with open('buy_or_sell.txt', 'r') as buy_or_sell:
        try:
            avax_balance = browser.find_element(By.XPATH, "//a[@data-testid='portfolio-token-list-row-symbol' and text()='AVAX']/following::p[@data-testid='portfolio-token-list-row-value']")
            usdc_balance = browser.find_element(By.XPATH, "//a[@data-testid='portfolio-token-list-row-symbol' and text()='USDC']/following::p[@data-testid='portfolio-token-list-row-value']").text
        except NoSuchElementException:
            usdc_balance = '$0'
        usdc_balance_dec = Decimal(sub(r'[^\d.]', '', usdc_balance))
        should_buy = False
        should_sell = True
        if usdc_balance_dec > 1:
            should_buy = True
            should_sell = False

        buy_sell_line = buy_or_sell.readline()
        if buy_sell_line == 'buy' and should_buy:
            print('Buying AVAX!')
            browser.find_element(By.CSS_SELECTOR, "[data-testid='swap-btn']").click()
            browser.find_element(By.CSS_SELECTOR, "[data-testid='from-select-token-btn']").click()
            browser.find_element(By.CSS_SELECTOR, "[data-testid='select-usdc-btn']").click()
            browser.find_element(By.CSS_SELECTOR, "[data-testid='token-max-btn']").click()
            browser.find_element(By.CSS_SELECTOR, "[data-testid='to-select-token-btn']").click()
            browser.find_element(By.CSS_SELECTOR, "[data-testid='select-avax-btn']").click()
            sleep(1)
            browser.find_element(By.XPATH, "(//button[@data-testid='swap-btn'])[1]").click()
            WebDriverWait(browser, 300).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='swap-success-toast']")))
            browser.refresh()
        if buy_sell_line == 'sell' and should_sell:
            print('Selling AVAX!')
            browser.find_element(By.CSS_SELECTOR, "[data-testid='swap-btn']").click()
            sleep(2)
            browser.find_element(By.CSS_SELECTOR, "[data-testid='from-select-token-btn']").click()
            browser.find_element(By.CSS_SELECTOR, "[data-testid='select-avax-btn']").click()
            browser.find_element(By.CSS_SELECTOR, "[data-testid='to-select-token-btn']").click()
            browser.find_element(By.CSS_SELECTOR, "[placeholder='Search Name, Symbol or Paste Address…']").send_keys('USDC')
            browser.find_element(By.CSS_SELECTOR, "[data-testid='select-usdc-btn']").click()
            browser.find_element(By.CSS_SELECTOR, "[data-testid='token-max-btn']").click()
            browser.find_element(By.XPATH, "(//button[@data-testid='swap-btn'])[2]").click()
            sleep(2)
            WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='swap-success-toast']")))
            browser.refresh()
        buy_or_sell.close()
        sleep(5)

