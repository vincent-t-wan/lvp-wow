MythicPlusStatsDB = MythicPlusStatsDB or {}
MythicPlusStatsDB.Stats = MythicPlusStatsDB.Stats or {}

local totalDamage = 0
local totalHealing = 0
local totalDamageTaken = 0
local totalDeaths = 0
local inMythicDungeon = false

local frame = CreateFrame("Frame")
frame:RegisterEvent("PLAYER_LOGIN")
frame:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")
frame:RegisterEvent("CHALLENGE_MODE_START")
frame:RegisterEvent("CHALLENGE_MODE_COMPLETED")

frame:SetScript("OnEvent", function(self, event, ...)
    if event == "PLAYER_LOGIN" then
        print("LVP version 1.0: Hello, world!")
    elseif event == "CHALLENGE_MODE_START" then
        totalDamage = 0
        totalHealing = 0
        totalDamageTaken = 0
        totalDeaths = 0
        inMythicDungeon = true

        local className = select(2, UnitClass("player"))
        local specIndex = GetSpecialization()
        local specName = specIndex and select(2, GetSpecializationInfo(specIndex)) or "Unknown"
        local specRole = GetSpecializationRole(specIndex)

        table.insert(MythicPlusStatsDB.Stats, {
            type = "dungeon_start",
            time = date("%Y-%m-%d %H:%M:%S"),
            class = className,
            spec = specName,
            role = specRole
        })
        print("Mythic+ started. Tracking active.")
        print("Class:", className, "| Spec:", specName, "| Role:", specRole)

    elseif event == "CHALLENGE_MODE_COMPLETED" then
        inMythicDungeon = false
        table.insert(MythicPlusStatsDB.Stats, {
            type = "dungeon_end",
            time = date("%Y-%m-%d %H:%M:%S"),
            totalDamage = totalDamage,
            totalHealing = totalHealing,
            totalDamageTaken = totalDamageTaken,
            totalDeaths = totalDeaths
        })
        print("Mythic+ completed.")
        print("Total damage dealt:", totalDamage)
        print("Total healing done:", totalHealing)
        print("Damage taken:", totalDamageTaken)
        print("Deaths:", totalDeaths)

    elseif event == "COMBAT_LOG_EVENT_UNFILTERED" and inMythicDungeon then
        local _, subEvent, _, sourceGUID, _, _, _, destGUID, _, _, _, _, _, amount = CombatLogGetCurrentEventInfo()
        local playerGUID = UnitGUID("player")

        -- damage
        if sourceGUID == playerGUID and type(amount) == "number" and (
            subEvent == "SPELL_DAMAGE" or
            subEvent == "SWING_DAMAGE" or
            subEvent == "RANGE_DAMAGE" or
            subEvent == "SPELL_PERIODIC_DAMAGE"
        ) then
            totalDamage = totalDamage + amount
        end

        -- healing
        if sourceGUID == playerGUID and type(amount) == "number" and (
            subEvent == "SPELL_HEAL" or
            subEvent == "SPELL_PERIODIC_HEAL"
        ) then
            totalHealing = totalHealing + amount
        end

        -- damage taken
        if destGUID == playerGUID and type(amount) == "number" and (
            subEvent == "SPELL_DAMAGE" or
            subEvent == "SWING_DAMAGE" or
            subEvent == "RANGE_DAMAGE" or
            subEvent == "SPELL_PERIODIC_DAMAGE"
        ) then
            totalDamageTaken = totalDamageTaken + amount
        end

        -- deaths
        if subEvent == "UNIT_DIED" and destGUID == playerGUID then
            totalDeaths = totalDeaths + 1
        end
    end
end)
