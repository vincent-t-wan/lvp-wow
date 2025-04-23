#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import json
import time
import pyrebase

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
    
def run(path):
    print(config)

    SAVE_FILE_PATH = os.path.expanduser(path)
    COLLECTION_NAME = "mythic_plus_runs"
    CHECK_INTERVAL_SECONDS = 60

    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    db = firebase.database()

    # --- PARSE LUA SAVEDVARIABLES FILE ---
    def extract_lua_table(lua_path):
        with open(lua_path, 'r', encoding='utf-8') as f:
            content = f.read()

        print(content)
        start = content.find("{")
        end = content.rfind("}") + 1
        json_like = content[start:end].replace("=", ":")
        json_like = json_like.replace("nil", "null")

        try:
            data = json.loads(json_like)
            return data
        except Exception as e:
            print("Failed to parse Lua file:", e)
            return []

    # --- BACKGROUND WORKER ---
    last_uploaded = set()
    while True:
        runs = extract_lua_table(SAVE_FILE_PATH)
        print(runs)
        new_runs = [json.dumps(run, sort_keys=True) for run in runs if json.dumps(run, sort_keys=True) not in last_uploaded]
        if new_runs:
            for run_str in new_runs:
                run = json.loads(run_str)
                db.collection(COLLECTION_NAME).add(run)
                last_uploaded.add(run_str)
                print("Uploaded new run:", run.get("dungeonName", "Unknown"))
        time.sleep(CHECK_INTERVAL_SECONDS)