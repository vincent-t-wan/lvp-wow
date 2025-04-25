import os
import pyrebase
from flask import Flask, request

COLLECTION_NAME = "mythic_plus_runs"

config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID")
}

print(config)

firebase = pyrebase.initialize_app(config)
db = firebase.database()

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json
    key = data.key
    entry = data.entry
    existing = db.child(COLLECTION_NAME).child(key).get()
    if existing.val() is None:
        db.child("mythic_plus_runs").child(key).set(entry)
        print(f"Uploaded {key}")
    else:
        print(f"Skipped (already in firebase): {key}")
    return {'status': 'ok'}