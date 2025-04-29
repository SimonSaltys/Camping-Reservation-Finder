from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime, timedelta

# Navigate to the booking page
def navigate_to_booking(driver, campsite_or_url):
    try:
        if isinstance(campsite_or_url, str):
            driver.get(campsite_or_url)
            print(f"Navigated to URL: {campsite_or_url}")
        else:
            # Extract information from the campsite element
            try:
                title = campsite_or_url.find_element(By.TAG_NAME, "h4").text.strip()
                description = campsite_or_url.find_element(By.TAG_NAME, "span").text.strip()
                print(f"Title: {title}")
                print(f"Description: {description}")
                
                # Find and click the book button
                book_button = campsite_or_url.find_element(By.CLASS_NAME, "book-now")
                print("Found book button, clicking...")
                book_button.click()
                print("Book button clicked")
            except Exception as e:
                print(f"Error extracting campsite info: {str(e)}")
                return False
                
        # Handle the booking form
        if switch_to_i_frame(driver) and handle_booking_form(driver):
            print("Successfully submitted booking form")
            
            # After successful form submission, handle calendar selection
            if select_booking_dates(driver):
                print("Successfully selected booking dates")
                return True
            else:
                print("Failed to select booking dates")
                return False
        else:
            print("Failed to submit booking form")
            return False
            
    except Exception as e:
        print(f"Error in navigation: {str(e)}")
        return False

# Handle the initial booking form
def handle_booking_form(driver):
    try:
        print("Starting to interact with campsite booking form...")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        h1 = driver.find_element(By.TAG_NAME, "h1")
        print(f"Found <h1>: {h1.text}")

        
        # Find the confirmation input field (the first input that requires 'Yes')
        try:
            print("Looking for form group")
            switch_to_i_frame(driver)

            # Wait for the form to fully load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "form-group"))
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
        
        # After filling out the form, the button should be enabled - check and click it
        try:
            # Small delay to ensure form validation completes
            time.sleep(1)
            
            # Try to find and click the continue button
            button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.btn-block")
            
            # Check if button is still disabled
            if button.get_attribute("disabled"):
                print("Button is still disabled. Form validation may have failed.")
                
                # Force enable button if needed (as a fallback)
                driver.execute_script("arguments[0].removeAttribute('disabled')", button)
                print("Forcibly enabled button")
            
            # Click the button
            button.click()
            print("Clicked continue button")
            
            # Wait for calendar to appear (which indicates successful form submission)
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.calendar-select-component"))
            )
            print("Calendar appeared - form submitted successfully")
            
            return True
        except Exception as e:
            print(f"Error clicking continue button: {str(e)}")
            return False
    
    except Exception as e:
        print(f"Error handling booking form: {str(e)}")
        return False

# Select dates on the calendar
def select_booking_dates(driver, check_in_date=None, check_out_date=None):
    try:
        print("Starting date selection process...")
        
        # Wait for the calendar to be fully loaded and interactive
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.calendar-cell-inner.valid"))
        )
        
        # If specific dates weren't provided, find the first available date
        if not check_in_date:
            try:
                # Find all valid cells (available for check-in)
                valid_cells = driver.find_elements(By.CSS_SELECTOR, "div.calendar-cell-inner.valid")
                
                if len(valid_cells) > 0:
                    # Get the day number from the first available cell
                    check_in_day = valid_cells[0].find_element(By.CLASS_NAME, "cell-date-number").text
                    print(f"Found available check-in day: {check_in_day}")
                    
                    # Click the first available date for check-in
                    valid_cells[0].click()
                    print(f"Selected day {check_in_day} for check-in")
                    
                    # Wait a moment for the calendar to update
                    time.sleep(1)
                    
                    # Now find check-out date options
                    checkout_cells = driver.find_elements(By.CSS_SELECTOR, "div.calendar-cell-inner.check-out-day-only")
                    
                    if len(checkout_cells) > 0:
                        # Get the day number from the first available checkout cell
                        check_out_day = checkout_cells[0].find_element(By.CLASS_NAME, "cell-date-number").text
                        print(f"Found available check-out day: {check_out_day}")
                        
                        # Click the first available checkout date
                        checkout_cells[0].click()
                        print(f"Selected day {check_out_day} for check-out")
                    else:
                        print("No checkout dates available")
                        return False
                else:
                    print("No valid check-in dates available")
                    
                    # Try to navigate to next month if no dates are available
                    next_month_button = driver.find_element(By.ID, "ClickNextMonth")
                    next_month_button.click()
                    print("Clicked next month button to look for available dates")
                    
                    # Wait for calendar to update
                    time.sleep(1)
                    
                    # Try again with the new month
                    return select_booking_dates(driver)
            except Exception as e:
                print(f"Error selecting available dates: {str(e)}")
                return False
        else:
            # If specific dates were provided
            try:
                # Parse the provided dates
                if isinstance(check_in_date, str):
                    check_in_date = datetime.strptime(check_in_date, "%m/%d/%Y")
                if isinstance(check_out_date, str):
                    check_out_date = datetime.strptime(check_out_date, "%m/%d/%Y")
                
                # Get the current month/year displayed in the calendar
                month_year_text = driver.find_element(By.CLASS_NAME, "calendar-month-title").text
                current_month, current_year = month_year_text.replace(",", "").split()
                
                # Convert month name to number
                month_dict = {
                    "January": 1, "February": 2, "March": 3, "April": 4,
                    "May": 5, "June": 6, "July": 7, "August": 8,
                    "September": 9, "October": 10, "November": 11, "December": 12
                }
                current_month_num = month_dict.get(current_month)
                current_year_num = int(current_year)
                
                # Navigate to the month of check-in date if needed
                while (current_year_num != check_in_date.year or 
                       current_month_num != check_in_date.month):
                    
                    # Determine if we need to go forward or backward
                    target_date = datetime(current_year_num, current_month_num, 1)
                    check_in_month_date = datetime(check_in_date.year, check_in_date.month, 1)
                    
                    if check_in_month_date > target_date:
                        # Click next month
                        next_month_button = driver.find_element(By.ID, "ClickNextMonth")
                        next_month_button.click()
                    else:
                        # Click previous month
                        prev_month_button = driver.find_element(By.CSS_SELECTOR, "a.calendar-month-select-arrow:first-child")
                        prev_month_button.click()
                    
                    # Wait for calendar to update
                    time.sleep(1)
                    
                    # Update current month/year
                    month_year_text = driver.find_element(By.CLASS_NAME, "calendar-month-title").text
                    current_month, current_year = month_year_text.replace(",", "").split()
                    current_month_num = month_dict.get(current_month)
                    current_year_num = int(current_year)
                
                # Now we're on the correct month, find the specific check-in date
                cell_selector = f"div.calendar-cell-inner:not(.non-selectable) div.cell-date-number:contains('{check_in_date.day}')"
                check_in_cells = driver.find_elements(By.CSS_SELECTOR, cell_selector)
                
                # Filter to find the valid cell that contains our date
                for cell in check_in_cells:
                    parent = cell.find_element(By.XPATH, "..")  # Get parent element
                    if "valid" in parent.get_attribute("class"):
                        cell.click()
                        print(f"Selected check-in date: {check_in_date.strftime('%m/%d/%Y')}")
                        break
                
                # Wait for calendar to update after selecting check-in date
                time.sleep(1)
                
                # Select check-out date if provided
                if check_out_date:
                    # Similar logic to navigate to check-out month if needed
                    # Then select the specific date
                    # This would be similar to the check-in date selection above
                    pass
                
            except Exception as e:
                print(f"Error selecting specific dates: {str(e)}")
                return False
        
        # Check if dates were successfully selected
        try:
            # Wait for the dates to be displayed in the summary section
            WebDriverWait(driver, 5).until(
                lambda d: "Not Selected" not in d.find_element(By.CSS_SELECTOR, "div.check-in-choice").text
            )
            WebDriverWait(driver, 5).until(
                lambda d: "Not Selected" not in d.find_element(By.CSS_SELECTOR, "div.check-out-choice").text
            )
            print("Dates successfully selected")
            
            # Look for any next steps (continue buttons, etc.)
            try:
                continue_buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn-primary:not([disabled])")
                if len(continue_buttons) > 0:
                    for button in continue_buttons:
                        if "Continue" in button.text or "Next" in button.text or "Book" in button.text:
                            button.click()
                            print("Clicked continue button after date selection")
                            break
            except:
                print("No continue button found after date selection")
            
            return True
        except Exception as e:
            print(f"Could not confirm date selection: {str(e)}")
            return False
            
    except Exception as e:
        print(f"Error selecting booking dates: {str(e)}")
        return False


def switch_to_i_frame(driver):
    try:
        print("Looking for iframe...")
        iframe = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "FlybookWidgetIframe"))
        )
        print("Found iframe, switching to it")
        driver.switch_to.frame(iframe)
        return True
    except TimeoutException:
        print("No iframe found within timeout period.")
        return False
    except Exception as e:
        print(f"Error finding iframe: {str(e)}")
        return False



# Usage example
# driver = webdriver.Chrome()
# book_campsite(driver, "https://example.com/campsite-booking", phone_number="123-456-7890")


