import os
import json
import requests
import pywhatkit as kit
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ------------------------------
# Configuration and Constants
# ------------------------------

# Google Classroom OAuth credentials and scopes
CREDENTIALS_FILE = 'client_secret_198973298286-bgs6dkuduhnvu3ve0h562qg38bcui9u9.apps.googleusercontent.com.json'  # OAuth client credentials file (in same directory)
SCOPES = [
    'https://www.googleapis.com/auth/classroom.announcements.readonly',
    'https://www.googleapis.com/auth/classroom.courses.readonly'
]

# File to track processed announcements (to avoid duplication)
PROCESSED_FILE = 'processed_posts.json'

# Gemini API configuration (Module 3)
GEMINI_MODEL_NAME = "models/gemini-2.0-flash"  # Gemini model per your quick start guide
GEMINI_API_KEY = "AIzaSyD7GrViM-0qPxCQ2W1uvkGik1zmLZ5Txw4"  # Replace with your actual Gemini API key
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com"

# Custom prompt for formatting announcements (adjust as needed)
FORMAT_PROMPT = (
    '''
    Format the following announcement text into a concise, professional WhatsApp group message. 
    Output only the final formatted message without any additional commentary, explanations, or multiple options. 
    Use appropriate emojis and text formatting (like bold or italics) to enhance clarity, 
    but include only the final text that is ready to be posted.
    And Incude emojis to help clarify the info 
    make sure to include date-time or deadlines if exist

    '''
)

# Recipient's phone number for WhatsApp via PyWhatKit
# The phone number should include the country code and a '+' prefix (e.g., "+15551234567").
RECIPIENT_PHONE = "+20 128 542 2943"  # Replace with the recipient's phone number


# ------------------------------
# Module 1: Google Classroom API Integration
# ------------------------------

def authenticate_classroom_api():
    """
    Authenticates with the Google Classroom API using OAuth 2.0.
    Returns an authorized Classroom API service object.
    """
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    service = build('classroom', 'v1', credentials=credentials)
    return service


def list_courses(service):
    """
    Retrieves a list of courses from Google Classroom.
    Returns:
        List of course dictionaries.
    """
    results = service.courses().list().execute()
    return results.get('courses', [])


# ------------------------------
# Module 2: Duplication Prevention Functions
# ------------------------------

def load_processed_posts():
    """
    Loads processed post IDs from a JSON file.
    Returns a dictionary of processed post IDs.
    """
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}


def save_processed_post(post_id):
    """
    Saves a processed post ID to the JSON file.
    """
    processed = load_processed_posts()
    processed[post_id] = True
    with open(PROCESSED_FILE, 'w') as file:
        json.dump(processed, file, indent=4)


# ------------------------------
# Module 3: Gemini API Formatting Function
# ------------------------------

def format_text_with_gemini(raw_text, prompt, gemini_api_key, model_name=GEMINI_MODEL_NAME):
    """
    Uses the Gemini API to generate formatted content by combining a prompt with raw text.
    Adjusted to extract text from the 'content' field in the API response.

    Parameters:
        raw_text (str): The raw announcement text.
        prompt (str): Formatting instructions.
        gemini_api_key (str): Your Gemini API key.
        model_name (str): The Gemini model to use.

    Returns:
        The formatted text as returned by the API, or None if an error occurs.
    """
    endpoint = f"{GEMINI_BASE_URL}/v1beta/{model_name}:generateContent"
    url = f"{endpoint}?key={gemini_api_key}"

    full_text = f"{prompt}\n\n{raw_text}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": full_text}
                ]
            }
        ]
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            candidates = data.get("candidates", [])
            if candidates:
                candidate = candidates[0]
                # Updated extraction: check within candidate["content"] first.
                content = candidate.get("content", {})
                parts = content.get("parts", [])
                if parts and parts[0].get("text"):
                    return parts[0].get("text")
                else:
                    # Fallback: check if candidate has an 'output' field directly.
                    if candidate.get("output"):
                        return candidate.get("output")
                    else:
                        print("DEBUG: Full Gemini API response for debugging:")
                        print(json.dumps(data, indent=2))
                        print("No text found in candidate content.")
                        return None
            else:
                print("No candidates returned.")
                return None
        else:
            print(f"Error: Received status code {response.status_code} from Gemini API")
            print("Response content:", response.text)
            return None
    except Exception as e:
        print("Exception occurred while calling Gemini API:", str(e))
        return None


# ------------------------------
# Module 4: WhatsApp Messaging with PyWhatKit
# ------------------------------

def send_whatsapp_message_pywhatkit(formatted_text, recipient_phone):
    """
    Uses pywhatkit to send a WhatsApp message.
    This function schedules the message to be sent one minute in the future.

    Parameters:
        formatted_text (str): The message content to send.
        recipient_phone (str): The recipient's phone number in international format (e.g., "+15551234567").
    """
    # Calculate the time one minute from now
    now = datetime.datetime.now()
    send_hour = now.hour
    send_minute = now.minute + 1
    if send_minute >= 60:
        send_minute = send_minute - 60
        send_hour = (send_hour + 1) % 24

    print(f"Scheduling WhatsApp message to {recipient_phone} at {send_hour}:{send_minute:02d}...")
    kit.sendwhatmsg(recipient_phone, formatted_text, send_hour, send_minute, wait_time=15, tab_close=True)


# ------------------------------
# Integration: Process Announcements, Format, and Send via WhatsApp
# ------------------------------

def process_announcements(service, course_id):
    """
    Fetches announcements for a given course, formats new ones using the Gemini API,
    sends the formatted message via WhatsApp using pywhatkit, and marks the announcement as processed.

    Parameters:
        service: Authorized Classroom API service object.
        course_id (str): ID of the course to process announcements.
    """
    print(f"\nFetching announcements for course ID: {course_id}")
    announcements = service.courses().announcements().list(courseId=course_id).execute().get('announcements', [])

    processed_posts = load_processed_posts()

    for announcement in announcements:
        post_id = announcement.get('id')
        if post_id in processed_posts:
            print(f"Post {post_id} already processed. Skipping.")
        else:
            raw_text = announcement.get('text', "No text provided.")
            update_time = announcement.get('updateTime', "Unknown update time")
            print(f"Processing post {post_id}: {raw_text}\nUpdated at: {update_time}")

            formatted = format_text_with_gemini(raw_text, FORMAT_PROMPT, GEMINI_API_KEY)
            if formatted:
                print("Formatted Output:")
                print(formatted)
                # Send via WhatsApp using PyWhatKit
                send_whatsapp_message_pywhatkit(formatted, RECIPIENT_PHONE)
            else:
                print("Formatting failed or returned no output.")

            save_processed_post(post_id)


# ------------------------------
# Main Execution Function
# ------------------------------

def main():
    """
    Main function to authenticate with Google Classroom, list courses, process announcements,
    format them via the Gemini API, and send the formatted messages via WhatsApp using pywhatkit.
    """
    service = authenticate_classroom_api()

    courses = list_courses(service)
    if not courses:
        print("No courses found.")
        return

    print("Found courses:")
    for course in courses:
        print(f"- {course['name']} (ID: {course['id']})")

    for course in courses:
        process_announcements(service, course['id'])


if __name__ == "__main__":
    main()
