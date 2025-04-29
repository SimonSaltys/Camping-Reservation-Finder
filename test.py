from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime, timedelta

# Navigate to the booking page
def navigate_to_booking(driver, campsite):
    try:
        # Extract information from the campsite element
        title = campsite.find_element(By.TAG_NAME, "h4").text.strip()
        description = campsite.find_element(By.TAG_NAME, "span").text.strip()
        print(f"Title: {title}")
        print(f"Description: {description}")
        
        # Find and click the book button
        book_button = campsite.find_element(By.CLASS_NAME, "book-now")
        print("Found book button, clicking...")
        book_button.click()
        print("Book button clicked")
    except Exception as e:
        print(f"Error extracting campsite info: {str(e)}")
        return False

    # Handle the booking form
    if handle_booking_form(driver):
        print("Successfully submitted booking form")

# Placeholder for the missing function `handle_booking_form`
def handle_booking_form(driver):
    try:
        # Wait for the form to fully load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "form-control"))
        )
        
        # Find the confirmation field - it's the first input with pattern attribute
        confirmation_field = driver.find_element(By.CSS_SELECTOR, "input[pattern='/YES/i']")
        confirmation_field.clear()
        confirmation_field.send_keys("YES")  # Enter in uppercase to ensure pattern match
        print("Entered 'YES' in confirmation field")
    except Exception as e:
        print(f"Could not find or interact with confirmation field: {str(e)}")
        
    # Find the phone number field - it's inside the single-question-answerer component
    try:
        phone_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "single-question-answerer input.form-control"))
        )
        phone_field.clear()
        phone_field.send_keys("555-123-4567")  # Replace with actual phone number
        print("Entered phone number")
    except Exception as e:
        print(f"Could not find or interact with phone field: {str(e)}")

    
    time.sleep(10)


    try:
        # Try to find and click the continue button
        button = driver.find_element(By.CLASS_NAME, "btn btn-primary btn-block")
        
        # Check if button is still disabled
        if button.get_attribute("disabled"):
            print("Button is still disabled. Form validation may have failed.")
        
        # Click the button
        button.click()
        print("Clicked continue button")
    except Exception as e:
        print(f"Could not find or interact with the button: {str(e)}")

    time.sleep(10)

# def switch_to_i_frame(driver):
#     try:
#         print("Looking for iframe containing 'go.theflybook.com'...")

#         iframe = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located(
#                 (By.CSS_SELECTOR, "iframe[src*='go.theflybook.com']:not([src*='stripe'])")
#             )
#         )

#         print(f"Found iframe with src: {iframe.get_attribute('src')}")
#         driver.switch_to.frame(iframe)
#         return True
#     except TimeoutException:
#         print("Timed out waiting for iframe.")
#         return False
#     except Exception as e:
#         print(f"Unexpected error while switching to iframe: {e}")
#         return False


# Usage example (commented out)
# from selenium import webdriver
# driver = webdriver.Chrome()
# navigate_to_booking(driver, campsite_element)
