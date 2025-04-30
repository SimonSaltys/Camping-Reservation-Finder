from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime, timedelta
from testMessage import sort_campsites
from copy import deepcopy




def navigate_to_booking(driver, campsite):
    try:
        # Re-locate the elements before interacting with them
        title = campsite.find_element(By.TAG_NAME, "h4").text.strip()
        description = campsite.find_element(By.TAG_NAME, "span").text.strip()

        if(title == ''):
            print("No Title")
            return False

        print(f"Title: {title}")
        print(f"Description: {description}")
        # Re-locate the book button before clicking it
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
        # return True

    if find_possible_booking(driver):
        print("Successfully Looked for some bookings")
        return find_best_booking(driver,title)

    
    return True

    

def handle_booking_form(driver):
    try:
        # Wait for the form to fully load
        WebDriverWait(driver, 5).until(
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
        phone_field = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "single-question-answerer input.form-control"))
        )
        phone_field.clear()
        phone_field.send_keys("555-123-4567")  # Replace with actual phone number
        print("Entered phone number")
    except Exception as e:
        print(f"Could not find or interact with phone field: {str(e)}")

    
    time.sleep(2)

    try:
        print("Searching for continue button")

        # Try to find and click the continue button
        button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'to')]"))
        )
        
        # Click the button
        button.click()
        print("Clicked continue button")
    except Exception as e:
        print(f"Could not find or interact with the button: {str(e)}")

    time.sleep(5)



def find_possible_booking(driver):
    try:
        print("Starting date selection process...")
        months_to_check = 3
        all_check_in_dates = []
        all_check_out_dates = []

        for month_index in range(months_to_check):
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "calendar-select-component"))
            )

            # Get all calendar cells
            dates = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".calendar-cell-inner"))
            )

            month_dropdown = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "month-dropdown"))
            )

            select = Select(month_dropdown)
            selected_month = select.first_selected_option.text


            print(f"Selected month: {selected_month}")

            for date_cell in dates:
                class_attr = date_cell.get_attribute("class")
                date_number = date_cell.find_element(By.CLASS_NAME, "cell-date-number").text
                full_date = f"{selected_month} {date_number}, 2025"

                if "valid" in class_attr:
                    all_check_in_dates.append(full_date)
                elif "check-out-day-only" in class_attr:
                    all_check_out_dates.append(full_date)

            # Print out the lists
            print("Check-in dates found:", all_check_in_dates)
            print("Check-out dates found:", all_check_out_dates)

            if month_index < months_to_check - 1:
                try:
                    next_month_button = driver.find_element(By.ID,"ClickNextMonth")
                    next_month_button.click()
                    print("Clicked next month button")
                    time.sleep(1.5)
                except Exception as e:
                    print(f"Error navigating to next month: {str(e)}")
                    break
        
        print(f"Total check-in dates found across {months_to_check} months: {len(all_check_in_dates)}")
        print(f"Total check-out dates found across {months_to_check} months: {len(all_check_out_dates)}")

        return {
            "check_in_dates": all_check_in_dates,
            "check_out_dates": all_check_out_dates
        }

    except Exception as e:
        print(f"Error finding possible bookings: {str(e)}")
        return {"check_in_dates": [], "check_out_dates": []}


def find_best_booking(driver, title ,min_stay=1, max_stay=7):
    try:
        available_dates = find_possible_booking(driver)

        if not available_dates["check_in_dates"]:
            print("No check-in dates available")
            return None
        
        parsed_checkin_dates = []
        for date_str in available_dates["check_in_dates"]:
            try:
                date_obj = datetime.strptime(date_str,"%B %d, %Y")
                parsed_checkin_dates.append(date_obj)
            except ValueError:
                print(f"Could not parse check-in date: {date_str}")

        parsed_checkout_dates = []
        for date_str in available_dates["check_out_dates"]:
            try:
                date_obj = datetime.strptime(date_str, "%B %d, %Y")
                parsed_checkout_dates.append(date_obj)
            except ValueError:
                print(f"Could not parse check-out date: {date_str}")

        parsed_checkin_dates.sort()
        parsed_checkout_dates.sort()

        options = []

        for check_in in parsed_checkin_dates:

            for check_out in parsed_checkout_dates:
                stay_nights = (check_out - check_in).days

                if min_stay <= stay_nights <= max_stay and check_out > check_in:
                     options.append({
                        "campsite": title,
                        "check_in": check_in,
                        "check_out": check_out,
                        "nights": stay_nights,
                        "check_in_str": check_in.strftime("%B %d, %Y"),
                        "check_out_str": check_out.strftime("%B %d, %Y")
                    })
        
        best_options = sort_campsites(deepcopy(options))

        for opt in best_options:
            print(f"- Campsite {opt['campsite']}, {opt['check_in_str']} to {opt['check_out_str']} ({opt['nights']} nights)")

        print(f"PICKING {best_options[0]}")

        if best_options:
            return best_options[0]
        else:
            return None      
    except Exception as e:
        print(f"Error finding best booking: {str(e)}")
        return None


