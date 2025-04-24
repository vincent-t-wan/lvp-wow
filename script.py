#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import json
import time
import pyrebase
import threading
import re

def fix_trailing_commas(raw_data: str) -> str:
    # Remove trailing commas before a closing brace } (inside objects)
    cleaned = re.sub(r',\s*(\})', r'\1', raw_data)
    # Remove trailing commas before a closing bracket ] (inside arrays)
    cleaned = re.sub(r',\s*(\])', r'\1', cleaned)
    return cleaned

load_dotenv()

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

stop_event = threading.Event()
    
def run(path):
    print(config)

    SAVE_FILE_PATH = os.path.expanduser(path)
    COLLECTION_NAME = "mythic_plus_runs"
    CHECK_INTERVAL_SECONDS = 60

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    # --- PARSE LUA SAVEDVARIABLES FILE ---
    def extract_lua_table(lua_path):
        try:
            with open(lua_path, 'r', encoding='utf-8') as f:
                content = f.read()

            print(content)
            start = content.find("{")
            end = content.rfind("}")
            json_like_list = list(content)
            json_like_list[start] = "#"
            json_like_list[end] = "$"
            json_like = "".join(json_like_list)
            print(json_like)
            json_like = json_like[start:end+1].replace("=", ":")
            json_like = json_like.replace("nil", "null")
            json_like = json_like.replace("[", "")
            json_like = json_like.replace("]", "")
            json_like = json_like.replace("#", "[")
            json_like = json_like.replace("$", "]")
            json_like = fix_trailing_commas(json_like)

            print(json_like)
            data = json.loads(json_like)
            return data
        except Exception as e:
            print("Failed to parse Lua file:", e)
            return []

    # --- BACKGROUND WORKER ---
    while not stop_event.is_set():
        runs = extract_lua_table(SAVE_FILE_PATH)
        print(runs)
        for entry in runs:
            key = f"{entry['name']}_{entry['realm']}_{entry['timeStart'].replace(' ', '_').replace(':', '-')}"
            existing = db.child(COLLECTION_NAME).child(key).get()
            if existing.val() is None:
                db.child("mythic_plus_runs").child(key).set(entry)
                print(f"Uploaded {key}")
            else:
                print(f"Already exists: {key}")
        # if entry not in last_uploaded:
        #     db.collection(COLLECTION_NAME).add(entry)
        #     last_uploaded.add(entry)
        #     print("Uploaded new run:", entry)
        time.sleep(CHECK_INTERVAL_SECONDS)

def start_thread(path):
    stop_event.clear()
    t = threading.Thread(target=run, args=[path], daemon=True)
    t.start()
    print("script executing...")
    return t

def stop_thread():
    stop_event.set()
    print("script stopped.")