from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from checkBooking import check_multi_day_availability
from test import navigate_to_booking


driver = webdriver.Chrome(service=Service("/opt/homebrew/bin/chromedriver"))
driver.get("https://www.eid.org/recreation/spra-campsite-photos-and-reservations")

time.sleep(5)

button = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "flybook-book-now-button"))
)

# Scroll into view
driver.execute_script("arguments[0].scrollIntoView(true);", button)

# Wait a moment to avoid overlap glitches
WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "flybook-book-now-button")))

# Click using JavaScript to avoid intercepts
driver.execute_script("arguments[0].click();", button)


# 2. Wait for the iframe to appear
iframe = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.ID, "FlybookWidgetIframe"))
)

# 3. Switch to the iframe
driver.switch_to.frame(iframe)

# 4. Now inside the iframe, find campsite items
campsite_items = WebDriverWait(driver, 15).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, "list-view-item"))
)
print(f"Found {len(campsite_items)} campsite items")

# for campsite in campsite_items:
navigate_to_booking(driver,campsite_items[0])

# time.sleep(3)

print(driver.title)
# driver.quit()
