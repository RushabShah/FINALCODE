from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("http://localhost:5000")
elem = driver.find_element_by_name("String")
elem.send_keys("Hello.")
elem.submit()
html= driver.find_element_by_xpath(".//html")
print html.text
assert "100.0% Unique" in html.text
#assert "sdsdsd" in html.text
driver.close()

