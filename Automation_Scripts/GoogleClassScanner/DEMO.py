import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

# ------------------------------
# CONFIGURATION
# ------------------------------
WHATSAPP_GROUP_NAME = "D3MO"  # Replace with your actual WhatsApp group name
CHROME_DRIVER_PATH = r"C:\WebDrivers\chromedriver.exe"  # Update with your ChromeDriver path
USER_DATA_DIR = r"./User_Data"  # Persistent profile directory
DUMMY_ANNOUNCEMENT = (
    "📢 *Test Announcement*\n\n"
    "This is a dummy announcement sent as a demo.\n\n"
    "Please disregard."
)


# ------------------------------
# HELPER FUNCTION: Remove non-BMP characters
# ------------------------------
def remove_non_bmp(text):
    """Return a string with characters having code points above 0xFFFF removed."""
    return ''.join(c for c in text if ord(c) <= 0xFFFF)


# ------------------------------
# FUNCTION: Send Dummy Announcement via WhatsApp
# ------------------------------
def send_whatsapp_message_selenium(message, group_name):
    """
    Use Selenium to send a message to a WhatsApp group.
    Uses a persistent Chrome profile to maintain login if enabled.
    """
    # Remove non-BMP characters from the message to avoid ChromeDriver issues.
    message = remove_non_bmp(message)

    chrome_options = Options()
    # Uncomment the following line to use a persistent profile:
    # chrome_options.add_argument(f"user-data-dir={USER_DATA_DIR}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")

    service_obj = Service(CHROME_DRIVER_PATH)

    try:
        driver = webdriver.Chrome(service=service_obj, options=chrome_options)
    except Exception as e:
        print("Error initializing ChromeDriver:", e)
        return

    driver.get("https://web.whatsapp.com")
    print("Waiting for WhatsApp Web to load (please scan QR if needed)...")

    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        print("WhatsApp Web loaded successfully!")
    except Exception as e:
        print("Error loading WhatsApp Web:", e)
        driver.quit()
        return

    try:
        group_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, f'//span[@title="{group_name}"]'))
        )
        group_element.click()
        print(f"Group '{group_name}' found and selected!")
    except Exception as e:
        print(f"Could not find group '{group_name}':", e)
        driver.quit()
        return

    # Try multiple selectors for the message box
    msg_box = None
    selectors = [
        ('xpath', '//div[@contenteditable="true"][@data-tab="10"]'),
        ('xpath', '//footer//div[@contenteditable="true"]'),
        ('css', "div.copyable-text.selectable-text")
    ]

    for sel_type, sel_value in selectors:
        try:
            if sel_type == 'xpath':
                msg_box = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, sel_value))
                )
            elif sel_type == 'css':
                msg_box = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, sel_value))
                )
            if msg_box:
                print(f"Message input box found using {sel_type} selector: {sel_value}")
                break
        except Exception as e:
            print(f"Selector '{sel_value}' did not work: {e}")

    if not msg_box:
        print("Error: Could not locate the message input box.")
        driver.quit()
        return

    try:
        msg_box.send_keys(message + Keys.ENTER)
        print("WhatsApp group message sent!")
    except Exception as e:
        print("Error sending message via WhatsApp:", e)

    time.sleep(10)
    driver.quit()


# ------------------------------
# MAIN EXECUTION
# ------------------------------
if __name__ == "__main__":
    send_whatsapp_message_selenium(DUMMY_ANNOUNCEMENT, WHATSAPP_GROUP_NAME)
