#!/usr/bin/env python3

import script
import os
import tkinter as tk
from tkinter import ttk, messagebox
import threading

def find_character_directory(selected_realm, character_name):
    """
    Helper function that searches for the directory path starting from:
    ...\World of Warcraft\_retail_\WTF\Account\selected_realm\character_name

    Returns:
        str or None: Full path to the character directory if found, else None.
    """
    # Locate this script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(script_dir)

    # Navigate up to the WoW root folder and then into WTF\Account
    wow_root = os.path.abspath(os.path.join(script_dir, "..", "..", "..", "WTF"))
    print(wow_root)
    target_path = os.path.join(selected_realm, character_name)
    print(target_path)

    for root, dirs, files in os.walk(wow_root):
        for dir_name in dirs:
            full_path = os.path.join(root, dir_name)
            if full_path.endswith(target_path):
                return full_path

    return None

realms = [
    "Aegwynn", "Aerie Peak", "Agamaggan", "Aggramar", "Akama", "Alexstrasza", "Alleria", "Altar of Storms",
    "Alterac Mountains", "Aman'Thul", "Andorhal", "Anetheron", "Antonidas", "Anub'arak", "Anvilmar", "Arathor",
    "Archimonde", "Area 52", "Argent Dawn", "Arthas", "Arygos", "Auchindoun", "Azgalor", "Azjol-Nerub", "Azralon",
    "Azshara", "Azuremyst", "Baelgun", "Balnazzar", "Barthilas", "Black Dragonflight", "Blackhand", "Blackrock",
    "Blackwater Raiders", "Blackwing Lair", "Blade's Edge", "Bladefist", "Bleeding Hollow", "Blood Furnace",
    "Bloodhoof", "Bloodscalp", "Bonechewer", "Borean Tundra", "Boulderfist", "Bronzebeard", "Burning Blade",
    "Burning Legion", "Caelestrasz", "Cairne", "Cenarion Circle", "Cenarius", "Cho'gall", "Chromaggus", "Coilfang",
    "Crushridge", "Daggerspine", "Dalaran", "Dalvengyr", "Dark Iron", "Darkspear", "Darrowmere", "Dath'Remar",
    "Dawnbringer", "Deathwing", "Demon Soul", "Dentarg", "Destromath", "Dethecus", "Detheroc", "Doomhammer",
    "Draenor", "Dragonblight", "Dragonmaw", "Drak'Tharon", "Drak'thul", "Draka", "Drakkari", "Dreadmaul",
    "Drenden", "Dunemaul", "Durotan", "Duskwood", "Earthen Ring", "Echo Isles", "Eitrigg", "Eldre'Thalas", "Elune",
    "Emerald Dream", "Eonar", "Eredar", "Executus", "Exodar", "Farstriders", "Feathermoon", "Fenris", "Firetree",
    "Fizzcrank", "Frostmane", "Frostmourne", "Frostwolf", "Galakrond", "Gallywix", "Garithos", "Garona", "Garrosh",
    "Ghostlands", "Gilneas", "Gnomeregan", "Goldrinn", "Gorefiend", "Gorgonnash", "Greymane", "Grizzly Hills",
    "Gul'dan", "Gundrak", "Gurubashi", "Hakkar", "Haomarush", "Hellscream", "Hydraxis", "Hyjal", "Icecrown",
    "Illidan", "Jaedenar", "Jubei'Thos", "Kael'thas", "Kalecgos", "Kargath", "Kel'Thuzad", "Khadgar", "Khaz Modan",
    "Khaz'goroth", "Kil'jaeden", "Kilrogg", "Kirin Tor", "Korgath", "Korialstrasz", "Kul Tiras", "Laughing Skull",
    "Lethon", "Lightbringer", "Lightning's Blade", "Lightninghoof", "Llane", "Lothar", "Madoran", "Maelstrom",
    "Magtheridon", "Maiev", "Mal'Ganis", "Malfurion", "Malorne", "Malygos", "Mannoroth", "Medivh", "Misha",
    "Mok'Nathal", "Moon Guard", "Moonrunner", "Mug'thol", "Muradin", "Nagrand", "Nathrezim", "Nazgrel", "Nazjatar",
    "Nemesis", "Ner'zhul", "Nesingwary", "Nordrassil", "Norgannon", "Onyxia", "Perenolde", "Proudmoore",
    "Quel'Thalas", "Quel'dorei", "Ragnaros", "Ravencrest", "Ravenholdt", "Rexxar", "Rivendare", "Runetotem",
    "Sargeras", "Saurfang", "Scarlet Crusade", "Scilla", "Sen'jin", "Sentinels", "Shadow Council", "Shadowmoon",
    "Shadowsong", "Shandris", "Shattered Halls", "Shattered Hand", "Shu'halo", "Silver Hand", "Silvermoon",
    "Sisters of Elune", "Skullcrusher", "Skywall", "Smolderthorn", "Spinebreaker", "Spirestone", "Staghelm",
    "Steamwheedle Cartel", "Stonemaul", "Stormrage", "Stormreaver", "Stormscale", "Suramar", "Tanaris", "Terenas",
    "Terokkar", "Thaurissan", "The Forgotten Coast", "The Scryers", "The Underbog", "The Venture Co",
    "Thorium Brotherhood", "Thrall", "Thunderhorn", "Thunderlord", "Tichondrius", "Tol Barad", "Tortheldrin",
    "Trollbane", "Turalyon", "Twisting Nether", "Uldaman", "Uldum", "Undermine", "Ursin", "Uther", "Vashj",
    "Vek'nilash", "Velen", "Warsong", "Whisperwind", "Wildhammer", "Windrunner", "Winterhoof", "Wyrmrest Accord",
    "Ysera", "Ysondre", "Zangarmarsh", "Zul'jin", "Zuluhed"
]

thread_handle = None

def on_submit():
    global thread_handle
    selected_realm = realm_var.get().strip()
    character_name = char_name_var.get().strip()
    if not character_name:
        messagebox.showerror("Error", "Character name is required.")
        return
    if not selected_realm:
        messagebox.showerror("Error", "Please select a realm.")
        return
    dir = find_character_directory(selected_realm, character_name)
    if dir != None:
        print(dir)
        if thread_handle is None or not thread_handle.is_alive():
            thread_handle = script.start_thread(dir + "\SavedVariables\lvp-wow.lua")
        select_frame.pack_forget()
        run_frame.pack(fill=tk.BOTH,expand=True)
    else:
        messagebox.showerror("Error", "Realm/Character path not found.")

def on_back():
    script.stop_thread()
    run_frame.pack_forget()
    select_frame.pack(fill=tk.BOTH,expand=True)

# Create the main window
root = tk.Tk()

select_frame = tk.Frame(root)
select_frame.pack(fill=tk.BOTH,expand=True)

run_frame = tk.Frame(root)
tk.Label(run_frame, text="Running LVP...").pack(pady=(10, 0))
back_btn = tk.Button(run_frame, text="Back", command=on_back).pack(pady=(10, 0))

root.title("LVP")
root.geometry("400x180")

# Realm dropdown (with search)
tk.Label(select_frame, text="Realm (US Only):").pack(pady=(10, 0))
realm_var = tk.StringVar()
realm_combo = ttk.Combobox(select_frame, textvariable=realm_var, values=realms)
realm_combo.pack(pady=(0, 10))

# Character name entry
tk.Label(select_frame, text="Character Name:").pack()
char_name_var = tk.StringVar()
char_entry = tk.Entry(select_frame, textvariable=char_name_var)
char_entry.pack(pady=(0, 10))

# Submit button
submit_btn = tk.Button(select_frame, text="Submit", command=on_submit)
submit_btn.pack()

# Run the GUI loop
root.mainloop()
