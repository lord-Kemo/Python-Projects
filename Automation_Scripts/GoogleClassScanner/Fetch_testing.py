from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time

# Replace with your WhatsApp group name exactly as it appears in WhatsApp
WHATSAPP_GROUP_NAME = "IBCU S'27 Admins"

# Path to your ChromeDriver. If it's in your PATH, you can just write "chromedriver"
CHROME_DRIVER_PATH = "C:\WebDrivers\chromedriver.exe"


def send_test_message():
    """
    This function opens WhatsApp Web, waits for you to scan the QR code (if needed),
    finds the specified WhatsApp group, and sends a test message.
    """
    # Set up Chrome options. Uncomment the next line to use a separate profile.
    chrome_options = Options()
    # chrome_options.add_argument("user-data-dir=./User_Data")

    # Create a Service object with the path to ChromeDriver
    service_obj = Service(CHROME_DRIVER_PATH)

    # Initialize the WebDriver with the Service object and options
    driver = webdriver.Chrome(service=service_obj, options=chrome_options)
    driver.get("https://web.whatsapp.com")
    print("Please scan the QR code if not already logged in.")

    # Wait until WhatsApp Web loads by waiting for the search box element
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
    except Exception as e:
        print("Error loading WhatsApp Web:", e)
        driver.quit()
        return

    # Find the group chat by its title and click it
    try:
        group = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, f'//span[@title="{WHATSAPP_GROUP_NAME}"]'))
        )
        group.click()
        print("Group chat found and clicked.")
    except Exception as e:
        print(f"Could not find group named '{WHATSAPP_GROUP_NAME}':", e)
        driver.quit()
        return

    # Wait for the message input box to load, type the test message, and send it
    try:
        msg_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
        test_message = ("Trying fetch : Checking Groups Validation and Accessing Keys to Numbers.")


        msg_box.send_keys(test_message + Keys.ENTER)
        print("Test message sent.")
    except Exception as e:
        print("Error sending message:", e)

    # Wait a few seconds to ensure the message is sent, then close the browser
    time.sleep(10)
    driver.quit()


if __name__ == "__main__":
    send_test_message()
