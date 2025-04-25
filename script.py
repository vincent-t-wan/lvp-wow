#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import json
import time
import threading
import re
import requests

# def convert_lua_array_of_objects_to_json(text):
#     # Match any block of: { { ... }, { ... }, ... }
#     # Convert only the *outermost* braces to brackets
#     # Handles nesting and spacing
#     def replacer(match):
#         inner = match.group(1)
#         return f'[{inner}]'

#     # This regex finds { { <anything> } } patterns with multiple entries
#     pattern = re.compile(r'\{\s*({\s*.*?\s*})\s*(?:,\s*{\s*.*?\s*})+\s*\}', re.DOTALL)
#     return re.sub(pattern, lambda m: replacer(m), text)

def fix_trailing_commas(raw_data: str) -> str:
    # Remove trailing commas before a closing brace } (inside objects)
    cleaned = re.sub(r',\s*(\})', r'\1', raw_data)
    # Remove trailing commas before a closing bracket ] (inside arrays)
    cleaned = re.sub(r',\s*(\])', r'\1', cleaned)
    return cleaned

load_dotenv()

stop_event = threading.Event()

url = 'http://localhost:5000/upload'

def run(path):

    SAVE_FILE_PATH = os.path.expanduser(path)
    LOCAL_CACHE_FILE = "uploaded_runs.json"
    CHECK_INTERVAL_SECONDS = 60

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
            # json_like = convert_lua_array_of_objects_to_json(json_like)

            print(json_like)
            data = json.loads(json_like)
            return data
        except Exception as e:
            print("Failed to parse Lua file:", e)
            return []
    
    if os.path.exists(LOCAL_CACHE_FILE):
        with open(LOCAL_CACHE_FILE, "r") as f:
            uploaded_cache = set(json.load(f))
    else:
        uploaded_cache = set()

    # --- BACKGROUND WORKER ---
    while not stop_event.is_set():
        runs = extract_lua_table(SAVE_FILE_PATH)
        print(runs)
        updated = False
        for entry in runs:
            key = f"{entry['name']}_{entry['realm']}_{entry['timeStart'].replace(' ', '_').replace(':', '-')}"
            if key not in uploaded_cache:
                uploaded_cache.add(key)
                updated = True
                try:
                    data = {
                        "key": key,
                        "entry": entry
                    }
                    response = requests.post(url, json=data)
                    response.raise_for_status()
                    resp = response.json()
                    if resp.get("status") == "ok":
                        print("Send successful!")
                    else:
                        print("Unexpected response:", resp)
                except requests.exceptions.RequestException as e:
                    print("Send failed:", e)
            else:
                print(f"Skipped (already in local): {key}")
        if updated:
            with open(LOCAL_CACHE_FILE, "w") as f:
                json.dump(list(uploaded_cache), f)
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