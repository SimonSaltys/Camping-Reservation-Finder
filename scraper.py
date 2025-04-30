from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from scraper_utils import navigate_to_booking
from discord_utils import send_discord_message
from dotenv import load_dotenv



# Global variables to persist across function calls
checked_campsites = []
best_options = []
max_campsites_to_check = 29  # Safety limit change to 28

def process_next_unchecked_campsite(driver):
    """
    Process the next unchecked campsite from the list.
    Returns True if a campsite was processed, False if all are checked or error.
    """
    global checked_campsites, best_options
    
    try:
        # Start fresh - go to the main page
        driver.get("https://www.eid.org/recreation/spra-campsite-photos-and-reservations")
        time.sleep(3)
        
        # Click the book now button
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "flybook-book-now-button"))
        )
        driver.execute_script("arguments[0].click();", button)
        
        # Wait for and switch to the iframe
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "FlybookWidgetIframe"))
        )
        driver.switch_to.frame(iframe)
        
        # Get all campsite items
        campsite_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "list-view-item"))
        )
        print(f"Found {len(campsite_items)} campsite items")
        
        # Find the first unchecked campsite
        for i, campsite in enumerate(campsite_items):
            try:
                campsite_name = campsite.find_element(By.TAG_NAME, "h4").text.strip()
                
                # Skip empty campsite names
                if not campsite_name:
                    print(f"Skipping campsite with empty name at position {i+1}")
                    continue
                
                print(f"Found campsite: {campsite_name}")
                
                # Skip if already checked
                if campsite_name in checked_campsites:
                    print(f"Skipping already checked campsite: {campsite_name}")
                    continue
                
                # Found an unchecked campsite - process it
                print(f"Checking campsite {i+1}/{len(campsite_items)}: {campsite_name}")
                
                # Process this campsite
                booking_result = navigate_to_booking(driver, campsite)
                
                if booking_result:
                    best_options.append(booking_result)
                
                # Mark as checked and return success
                checked_campsites.append(campsite_name)
                print(f"Added {campsite_name} to checked list. Total checked: {len(checked_campsites)}")
                return True
                
            except Exception as e:
                print(f"Error processing campsite {i+1}: {str(e)}")
                continue
        
        # If we get here, all campsites have been checked
        print("All campsites have been checked!")
        return False
        
    except Exception as e:
        print(f"Error in process_next_unchecked_campsite: {str(e)}")
        return False

def main():
    """Main function that starts the process and loops through campsites"""
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    load_dotenv()

    try:
        # Keep processing campsites until we're done or hit the safety limit
        campsite_count = 0
        while campsite_count < max_campsites_to_check:
            # Process the next unchecked campsite
            success = process_next_unchecked_campsite(driver)
            
            if success:
                campsite_count += 1
                print(f"Successfully processed campsite {campsite_count}")
            else:
                print("No more campsites to process or error occurred. Exiting loop.")
                break
                
            # Small delay between iterations
            time.sleep(2)
            
    except Exception as e:
        print(f"An error occurred in main: {e}")
    finally:
        # Print results    
        print(f"\nTotal campsites checked: {len(checked_campsites)}")
        print("Checked campsites:")
        for i, name in enumerate(checked_campsites):
            print(f"{i+1}. {name}")

            # Create the "Best Campsite Options Found" message
        message = "**🏕️Best Campsite Options Found:**\n"
        for i, c in enumerate(best_options[:10], 1):
            # Check if the campsite is one of the specified ones
            star = "⭐" if any(num in c['campsite'] for num in ["014", "015", "016"]) else ""
            message += f"**{i}. {c['campsite']} {star}**\n"
            message += f"📅 {c['check_in_str']} to {c['check_out_str']} ({c['nights']} nights)\n\n"

    # Truncate if message exceeds 2000 characters
        if len(message) > 2000:
            message = message[:1970] + '...'

        # Create the more concise "Other Options Found" message
        #todo off by 1
        more_message = "\n"
        for i, c in enumerate(best_options[10:28], 11):
            more_message += f"**{i}. {c['campsite']}**{star} ({c['nights']} nights)\n"


        # Truncate if more_message exceeds 2000 characters
        if len(more_message) > 2000:
            more_message = more_message[:1970] + '...'

        # Send the messages
        send_discord_message(message)
        send_discord_message(more_message)

        # Allow time to see results before closing
        time.sleep(5)
        print(driver.title)
        driver.quit()


if __name__ == "__main__":
    main()