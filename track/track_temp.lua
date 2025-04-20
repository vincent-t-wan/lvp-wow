local addonName, addon = ...
addon.data = addon.data or {}
MythicPlusStatsDB = MythicPlusStatsDB or {}
MythicPlusStatsDB.Events = MythicPlusStatsDB.Events or {}
addon.data = MythicPlusStatsDB.Events

local f = CreateFrame("Frame")

-- Event Registration
f:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")
f:RegisterEvent("ENCOUNTER_START")
f:RegisterEvent("ENCOUNTER_END")

f:SetScript("OnEvent", function(self, event, ...)
    if event == "COMBAT_LOG_EVENT_UNFILTERED" then
        local timestamp, subEvent, _, sourceGUID, sourceName, _, _, destGUID, destName, _, _, spellID, spellName = CombatLogGetCurrentEventInfo()

    elseif event == "ENCOUNTER_START" then
        local encounterID, encounterName, difficultyID, groupSize = ...
        table.insert(addon.data, {
            type = "boss_start",
            boss = encounterName,
            id = encounterID,
            time = date("%Y-%m-%d %H:%M:%S")
        })
        print("Boss started: " .. encounterName)

    elseif event == "ENCOUNTER_END" then
        local encounterID, encounterName, difficultyID, groupSize, success = ...
        table.insert(addon.data, {
            type = "boss_end",
            boss = encounterName,
            id = encounterID,
            success = success == 1,
            time = date("%Y-%m-%d %H:%M:%S")
        })
        print("Boss ended: " .. encounterName .. (success == 1 and " (Victory)" or " (Wipe)"))
    end
end)
