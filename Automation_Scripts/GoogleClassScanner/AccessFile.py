import os
import json
import time
import datetime
import schedule
import requests

# Selenium imports for WhatsApp group automation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Google Classroom API imports
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ------------------------------
# CONFIGURATION & CONSTANTS
# ------------------------------

# Google Classroom OAuth settings – update with your credentials file name
CREDENTIALS_FILE = 'client_secret_198973298286-bgs6dkuduhnvu3ve0h562qg38bcui9u9.apps.googleusercontent.com.json'
SCOPES = [
    'https://www.googleapis.com/auth/classroom.announcements.readonly',
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.coursework.me'
]

# File to track processed posts (avoid duplicates)
PROCESSED_FILE = 'processed_posts.json'

# Gemini API settings (for formatting messages) – update with your actual API key
GEMINI_MODEL_NAME = "models/gemini-2.0-flash"
GEMINI_API_KEY = "AIzaSyD7GrViM-0qPxCQ2W1uvkGik1zmLZ5Txw4"  # Replace with your Gemini API key
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com"
# Refined prompt: output only the final formatted WhatsApp message.
FORMAT_PROMPT = (
    "Format the following announcement text into a concise, professional WhatsApp group message. "
    "Output only the final formatted message without any additional commentary or multiple options. "
    "Use appropriate emojis and text formatting for clarity."
)

# WhatsApp group details (for Selenium automation) – update with your group's exact name
WHATSAPP_GROUP_NAME = "FCAI IBCU SWE S'27 | Materials"

# Selenium WebDriver settings – update the path as needed (use a raw string for Windows)
CHROME_DRIVER_PATH = r"C:\WebDrivers\chromedriver.exe"

# Persistent profile directory for Selenium (to keep WhatsApp logged in)
USER_DATA_DIR = r"./User_Data"

# Polling interval in seconds for scanning new uploads (e.g., 300 seconds = 5 minutes)
POLL_INTERVAL = 300

# ------------------------------
# SETUP PERSISTENT PROFILE DIRECTORY
# ------------------------------

if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)
    print(f"Created persistent profile directory: {USER_DATA_DIR}")

# ------------------------------
# HELPER: Safe Execution with Retries for API Calls
# ------------------------------

def safe_execute(request, retries=3, delay=5):
    """Attempt to execute a Google API request with retries on failure."""
    for attempt in range(retries):
        try:
            return request.execute()
        except Exception as e:
            print(f"[Warning] Error executing request (attempt {attempt+1}/{retries}): {e}")
            time.sleep(delay)
    raise Exception("Request failed after multiple retries.")

# ------------------------------
# GOOGLE CLASSROOM FUNCTIONS (Module 1 & 3)
# ------------------------------

def authenticate_classroom_api():
    """Authenticate with Google Classroom API using OAuth2 and return a service object."""
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    service = build('classroom', 'v1', credentials=credentials)
    return service

def list_courses(service):
    """Retrieve list of courses."""
    results = safe_execute(service.courses().list())
    return results.get('courses', [])

def fetch_all_announcements(service, course_id):
    """Fetch all announcements from a course, handling pagination."""
    announcements = []
    request = service.courses().announcements().list(courseId=course_id)
    while request is not None:
        response = safe_execute(request)
        announcements.extend(response.get('announcements', []))
        request = service.courses().announcements().list_next(request, response)
    return announcements

def fetch_all_coursework(service, course_id):
    """Fetch all coursework (assignments, material uploads) from a course, handling pagination."""
    coursework = []
    request = service.courses().courseWork().list(courseId=course_id)
    while request is not None:
        response = safe_execute(request)
        coursework.extend(response.get('courseWork', []))
        request = service.courses().courseWork().list_next(request, response)
    return coursework

# ------------------------------
# DUPLICATION PREVENTION FUNCTIONS (Module 2)
# ------------------------------

def load_processed_posts():
    """Load processed post IDs from file."""
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_processed_post(post_id):
    """Mark a post as processed by saving its ID."""
    processed = load_processed_posts()
    processed[post_id] = True
    with open(PROCESSED_FILE, 'w') as f:
        json.dump(processed, f, indent=4)

# ------------------------------
# GEMINI API FORMATTING FUNCTION (Module 3)
# ------------------------------

def format_text_with_gemini(raw_text):
    """
    Use the Gemini API to format the text.
    Returns only the final formatted message (a string) or None on error.
    """
    endpoint = f"{GEMINI_BASE_URL}/v1beta/{GEMINI_MODEL_NAME}:generateContent"
    url = f"{endpoint}?key={GEMINI_API_KEY}"

    # Combine the refined prompt with the raw text
    full_text = f"{FORMAT_PROMPT}\n\n{raw_text}"

    payload = {
        "contents": [
            {"parts": [{"text": full_text}]}
        ]
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            candidates = data.get("candidates", [])
            if candidates:
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if parts and parts[0].get("text"):
                    return parts[0].get("text")
            print("Formatting returned no output.")
            return None
        else:
            print(f"Gemini API Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print("Exception during Gemini formatting:", str(e))
        return None

# ------------------------------
# WHATSAPP GROUP SENDING VIA SELENIUM (Module 2 workaround)
# ------------------------------

def send_whatsapp_message_selenium(message, group_name):
    """
    Use Selenium to send a message to a WhatsApp group.
    Uses a persistent Chrome profile to maintain login.
    """
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={USER_DATA_DIR}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    from selenium.webdriver.chrome.service import Service
    service_obj = Service(CHROME_DRIVER_PATH)

    try:
        driver = webdriver.Chrome(service=service_obj, options=chrome_options)
    except Exception as e:
        print("Error initializing ChromeDriver:", e)
        return

    driver.get("https://web.whatsapp.com")
    print("Waiting for WhatsApp Web to load...")

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
        group = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, f'//span[@title="{group_name}"]'))
        )
        group.click()
        print(f"Group '{group_name}' found and selected!")
    except Exception as e:
        print(f"Could not find group named '{group_name}':", e)
        driver.quit()
        return

    try:
        msg_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
        msg_box.send_keys(message + Keys.ENTER)
        print("WhatsApp group message sent!")
    except Exception as e:
        print("Error sending message via WhatsApp:", e)

    time.sleep(10)
    driver.quit()

# ------------------------------
# PROCESSING UPDATES FROM GOOGLE CLASSROOM (Module 1 & 3)
# ------------------------------

def process_classroom_updates(service):
    """
    Process announcements and coursework for all courses.
    For each course:
      - Fetch all announcements and coursework (with pagination).
      - For each new update (not in processed_posts), format it via Gemini API.
      - Send the formatted message to the WhatsApp group.
      - Mark the update as processed.
    """
    courses = list_courses(service)
    processed_posts = load_processed_posts()

    for course in courses:
        course_id = course.get('id')
        print(f"\nFetching updates for course: {course.get('name')} (ID: {course_id})")

        # Process Announcements
        announcements = fetch_all_announcements(service, course_id)
        print(f"Found {len(announcements)} announcements.")
        for announcement in announcements:
            post_id = announcement.get('id')
            update_time = announcement.get('updateTime')
            print(f"Announcement ID: {post_id}, Updated: {update_time}")
            if post_id in processed_posts:
                continue
            raw_text = announcement.get('text', "No text provided.")
            formatted = format_text_with_gemini(raw_text)
            if formatted:
                print("Formatted Announcement:")
                print(formatted)
                send_whatsapp_message_selenium(formatted, WHATSAPP_GROUP_NAME)
            else:
                print("No formatted output for announcement", post_id)
            save_processed_post(post_id)

        # Process Coursework updates (assignments, materials)
        coursework = fetch_all_coursework(service, course_id)
        print(f"Found {len(coursework)} coursework items.")
        for work in coursework:
            post_id = work.get('id')
            if post_id in processed_posts:
                continue
            title = work.get('title', "No title")
            description = work.get('description', "")
            raw_text = f"Assignment: {title}\\n{description}"
            formatted = format_text_with_gemini(raw_text)
            if formatted:
                print("Formatted Coursework Update:")
                print(formatted)
                send_whatsapp_message_selenium(formatted, WHATSAPP_GROUP_NAME)
            else:
                print("No formatted output for coursework", post_id)
            save_processed_post(post_id)

# ------------------------------
# DAILY ASSIGNMENT DEADLINE REMINDER (Module 4)
# ------------------------------

def check_assignment_deadlines(service):
    """
    Check assignments in all courses and send a daily reminder for upcoming deadlines.
    """
    courses = list_courses(service)
    now = datetime.datetime.now()

    for course in courses:
        course_id = course.get('id')
        coursework = fetch_all_coursework(service, course_id)
        for work in coursework:
            due = work.get('dueDate')  # Expected as a dict with 'year', 'month', 'day'
            if due:
                try:
                    assignment_due = datetime.datetime(due['year'], due['month'], due['day'])
                except Exception as e:
                    print(f"Error parsing dueDate for assignment {work.get('id')}:", e)
                    continue
                if now < assignment_due and (assignment_due - now).days <= 7:
                    title = work.get('title', "Assignment")
                    reminder = (f"Reminder: '{title}' is due on {assignment_due.strftime('%A, %B %d at %I:%M %p')}. "
                                "Please make sure to submit your work on time.")
                    print("Sending reminder for assignment:", title)
                    send_whatsapp_message_selenium(reminder, WHATSAPP_GROUP_NAME)

# ------------------------------
# POLLING & SCHEDULING SETUP
# ------------------------------

def poll_updates(service):
    """Poll for new uploads and process them."""
    process_classroom_updates(service)

def main():
    # Authenticate once at start
    service = authenticate_classroom_api()

    # Schedule polling every POLL_INTERVAL seconds (e.g., every 5 minutes)
    schedule.every(POLL_INTERVAL).seconds.do(lambda: poll_updates(service))

    # Schedule daily assignment reminders at 08:00 AM
    schedule.every().day.at("08:00").do(lambda: check_assignment_deadlines(service))

    print("Started polling for Classroom updates and scheduled daily reminders...")
    while True:
        schedule.run_pending()
        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    main()
