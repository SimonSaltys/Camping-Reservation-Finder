from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta

def check_multi_day_availability(driver, campsite_or_url, min_days=3):
    """
    Check if there are at least min_days consecutive days available for booking.
    Returns a list of available date ranges if found, otherwise an empty list.
    """
    try:
        # Navigate to the booking page
        if isinstance(campsite_or_url, str):
            driver.get(campsite_or_url)
        else:
            # Assuming campsite is an element with a book-now button
            title = campsite_or_url.find_element(By.TAG_NAME, "h4").text.strip()
            description = campsite_or_url.find_element(By.TAG_NAME, "span").text.strip()
            book_button = campsite_or_url.find_element(By.CLASS_NAME, "book-now")
            
            print(f"Title: {title}")
            print(f"Description: {description}")
            
            # Click the book button
            book_button.click()
        
        # Check if we need to switch to an iframe
        try:
            iframe = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='go.theflybook.com']"))
            )
            driver.switch_to.frame(iframe)
        except:
            print("No iframe found or not needed, continuing with main content")
        
        # Handle initial form if present
        try:
            # Wait for the confirmation input field
            confirmation_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[pattern='/YES/i']"))
            )
            
            # Input "YES" into the confirmation field
            confirmation_input.clear()
            confirmation_input.send_keys("YES")
            print("INPUTTING YES")
            
            # Input phone number if needed
            phone_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "single-question-answerer input[type='text']"))
            )
            phone_input.clear()
            phone_input.send_keys("801-456-3345")
            print("INPUTTING NUMBER")

            # # Click continue button once it's enabled
            # continue_button = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.btn-block"))
            # )
            # continue_button.click()
            
            # Wait for calendar to appear
            time.sleep(2)
        except:
            print("Form submission not needed or failed, attempting to check calendar directly")
        
        # Now check the calendar for availability
        available_stays = []
        
        # Find the current month and year displayed
        month_year = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".calendar-month-title"))
        ).text.strip()
        print(f"Checking availability for: {month_year}")
        
        # Analyze the calendar grid to find consecutive available days
        calendar_cells = driver.find_elements(By.CSS_SELECTOR, ".calendar-cell-inner")
        
        # Extract dates and their status
        date_statuses = []
        current_month = datetime.strptime(month_year, "%B, %Y")
        
        for cell in calendar_cells:
            try:
                day_number = int(cell.find_element(By.CSS_SELECTOR, ".cell-date-number").text.strip())
                
                # Skip days from previous/next month (usually shown in gray)
                if "non-selectable" in cell.get_attribute("class"):
                    continue
                
                # Check if the date is available for check-in
                is_available = "valid" in cell.get_attribute("class")
                
                # Create a date object and record availability
                cell_date = current_month.replace(day=day_number)
                date_statuses.append((cell_date, is_available))
            except:
                continue
        
        # Find consecutive available days
        consecutive_days = []
        for i, (date, available) in enumerate(date_statuses):
            if available:
                consecutive_days.append(date)
                
                # Check if we have a sequence that ends here
                if i == len(date_statuses) - 1 or not date_statuses[i+1][1]:
                    if len(consecutive_days) >= min_days:
                        start_date = consecutive_days[0]
                        end_date = consecutive_days[-1]
                        available_stays.append((start_date, end_date, len(consecutive_days)))
                    consecutive_days = []
            else:
                if len(consecutive_days) >= min_days:
                    start_date = consecutive_days[0]
                    end_date = consecutive_days[-1]
                    available_stays.append((start_date, end_date, len(consecutive_days)))
                consecutive_days = []
        
        # Check next month if needed by clicking the next month button
        # This can be extended to check multiple months if needed
        
        # Switch back to the main page
        driver.switch_to.default_content()
        
        # Report findings
        if available_stays:
            print(f"Found {len(available_stays)} availability periods of {min_days}+ days:")
            for start, end, days in available_stays:
                print(f"  {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')} ({days} days)")
        else:
            print(f"No availability of {min_days}+ consecutive days found")
        
        return available_stays
        
    except Exception as e:
        print(f"❌ Error checking availability: {e}")
        driver.switch_to.default_content()
        return []

# Example usage:
# driver = webdriver.Chrome()
# available_periods = check_multi_day_availability(driver, "https://booking-url.com", min_days=3)