# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestPlacePages():
  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_placePages(self):
    self.driver.get("http://localhost:8000/restaurants/home/")
    self.driver.maximize_window()
    wait = WebDriverWait(self.driver, 50)

    # Select categories
    time.sleep(2)
    self.driver.find_element(By.CSS_SELECTOR, ".categories-card:nth-child(2) > h3").click()
    time.sleep(2)
    self.driver.find_element(By.LINK_TEXT, "Grocery-Bakery").click()
    time.sleep(2)
    self.driver.find_element(By.LINK_TEXT, "Restaurant").click()
    time.sleep(2)

    # Select a restaurant
    view_detail = self.driver.find_element(By.XPATH,
                                           "//a[contains(text(), 'View Detail') and contains(@href, '/restaurants/5/')]")
    self.driver.execute_script("arguments[0].click();", view_detail)
    time.sleep(3)

    # Back to all restaurants
    back_to_all_restaurants = self.driver.find_element(By.XPATH,
                                                  "//a[contains(text(), 'Back to All Restaurants') and @href='/restaurants/all/?category=']")
    self.driver.execute_script("arguments[0].click();", back_to_all_restaurants)
    time.sleep(4)
    self.driver.close()
  
