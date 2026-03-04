import os.path
import joblib
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def main():

    print("\n🔍 Loading ML Model...")
    model = joblib.load("signup_model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    print("✅ Model Loaded Successfully!")

    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)

    print("\n📨 Fetching Latest Emails...\n")

    results = service.users().messages().list(
        userId='me',
        maxResults=20
    ).execute()

    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")
        return

    print("===== REAL-TIME SIGNUP DETECTION =====\n")

    for msg in messages:
        msg_data = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='metadata',
            metadataHeaders=['Subject', 'From']
        ).execute()

        headers = msg_data['payload']['headers']

        subject = ""
        sender = ""

        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            if header['name'] == 'From':
                sender = header['value']

        if subject.strip() == "":
            continue

        X = vectorizer.transform([subject])
        prediction = model.predict(X)[0]

        if prediction == 1:
            print("🚨 Signup Email Detected!")
            print("From   :", sender)
            print("Subject:", subject)
            print("-" * 60)

if __name__ == '__main__':
    main()
