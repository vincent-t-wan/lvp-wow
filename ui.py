#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk

selected_realm = ""
character_name = ""

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

def on_submit():
    selected_realm = realm_var.get()
    character_name = char_name_var.get()
    select_frame.pack_forget()
    run_frame.pack(fill=tk.BOTH,expand=True)

def on_back():
    selected_realm = ""
    character_name = ""
    run_frame.pack_forget()
    select_frame.pack(fill=tk.BOTH,expand=True)

# Create the main window
root = tk.Tk()

select_frame = tk.Frame(root)
select_frame.pack(fill=tk.BOTH,expand=True)

run_frame = tk.Frame(root)
tk.Label(run_frame, text="Running LVP...").pack(pady=(10, 0))
tk.Label(run_frame, text="Character: " + character_name).pack(pady=(10, 0))
tk.Label(run_frame, text="Realm: " + selected_realm).pack(pady=(10, 0))
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
