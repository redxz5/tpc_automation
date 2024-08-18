import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup logging
logging.basicConfig(filename='log.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(message)s')

# Headless browser setup with user data stored in 'data' folder
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # Run in headless mode
chrome_options.add_argument("--user-data-dir=./data")  # Store user data
chrome_options.add_argument("--window-size=1920,1080")  # Set a specific window size
chrome_options.add_argument("--disable-gpu")  # Disable GPU (sometimes helps with rendering issues)
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model (useful in headless mode)
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_argument("--dns-prefetch-disable")  # Disable DNS prefetching
chrome_options.add_argument("--dns-over-https")  # Use DNS over HTTPS
# chrome_options.add_argument("--host-resolver-rules=MAP * 1.1.1.1")  # Redirect DNS to Cloudflare


num_of_pass=1

try:
    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Set timeout
    driver.set_page_load_timeout(60)  # Increase page load timeout
    
    # Function to scrape data from a page
    def scrape_data():        
        driver.get('https://www.placement.iitbhu.ac.in/company/opportunities')  # Replace with the actual URL
        print("Waiting for tpc site.......")
        time.sleep(30)
        content = driver.page_source
        return content

    # Variable to check in the scraped data
    text = ["Unify","unify"]
    whatsapp_group_name = "Script Alert"
    # whatsapp_group_name = "Mine"

    while True:
        print(f"\t\tPass : {num_of_pass}")
        num_of_pass+=1
        print("Searching............")
        # Scrape the page
        scraped_content = scrape_data()

        found = 0
        for word in text:
            if word in scraped_content:
                found=1
                break

        # Check if the text is present in the scraped content
        if (found==1):
            # Open WhatsApp Web
            print("ENTRY FOUND!!")
            print("Opening Whatsapp.........")
            driver.get('https://web.whatsapp.com')
            time.sleep(30)  # Wait for WhatsApp Web to load

            # Find and click the group chat
            
            try:
                print(f"Searching Group {whatsapp_group_name}")
                search_box = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @role='textbox']"))
                )
                search_box.click()
                search_box.send_keys(f"{whatsapp_group_name}")
                search_box.send_keys(Keys.RETURN)
            except Exception as e:
                logging.error("Failed to locate or interact with the search box.", exc_info=True)

            # Send the message to the group
            try:
                print("Sending The message")
                message_box = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Type a message' and @contenteditable='true']"))
                )
                message_box.click()
                message_box.send_keys(f"Alert: {text} was found on the website!")
                message_box.send_keys(Keys.RETURN)
                time.sleep(30)
                print("Message sent!")
            except Exception as e:
                logging.error("Failed to locate or interact with the message box.", exc_info=True)
        else:
            print("Not Found")
            print("Standby on the site.......")
            # Wait for 10 minutes
            time.sleep(600)
        
        print()
        time.sleep(10)

except Exception as e:
    # Log any errors that occur
    logging.error("An error occurred", exc_info=True)

finally:
    # Clean up and close the driver
    driver.quit()