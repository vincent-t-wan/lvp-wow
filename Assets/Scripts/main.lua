MythicPlusStatsDB = MythicPlusStatsDB or {}
MythicPlusStatsDB.Stats = MythicPlusStatsDB.Stats or {}

local customPrint(msg)
    local prefix = "|cffFFD700LVP>|r "  -- Gold color
        print(prefix .. msg)

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
        customPrint("LVP version 1.0: Hello, world!")
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

        local dungeonId = C_ChallengeMode.GetActiveChallengeMapID()
        local dungeonLevel = C_ChallengeMode.GetActiveKeystoneLevel()
        local dungeonName = C_ChallengeMode.GetMapUIInfo(dungeonId)
        local dungeonSeed = C_ChallengeMode.GetSlottedKeystoneInfo()

        table.insert(MythicPlusStatsDB.Stats, {
            type = "dungeon_start",
            dungeonId = dungeonId,
            dungeonName = dungeonName,
            dungeonLevel = dungeonLevel,
            dungeonSeed = dungeonSeed,
            time = date("%Y-%m-%d %H:%M:%S"),
            class = className,
            spec = specName,
            role = specRole
        })
        customPrint("Mythic+ started. Tracking active.")
        customPrint("Class:", className, "| Spec:", specName, "| Role:", specRole)
        customPrint("id:", dungeonId, "| name:", dungeonName, "| level:", dungeonLevel, "| seed:", dungeonSeed)

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
        customPrint("Mythic+ completed.")
        customPrint("Total damage dealt:", totalDamage)
        customPrint("Total healing done:", totalHealing)
        customPrint("Damage taken:", totalDamageTaken)
        customPrint("Deaths:", totalDeaths)

    elseif event == "COMBAT_LOG_EVENT_UNFILTERED" and inMythicDungeon then
        local eventInfo = {CombatLogGetCurrentEventInfo()}
        local timestamp, subEvent, hideCaster, sourceGUID, sourceName, sourceFlags, sourceRaidFlags, destGUID, destName, destFlags, destRaidFlags = unpack(eventInfo, 1, 11)
        local spellID, spellName, spellSchool, amount, overhealing, absorbed, critical

        local playerGUID = UnitGUID("player")

        -- damage
        if sourceGUID == playerGUID then
            -- https://wowpedia.fandom.com/wiki/COMBAT_LOG_EVENT
            if subEvent == "SPELL_DAMAGE" then
                amount = unpack(eventInfo, 15, 15)
                totalDamage = totalDamage + amount
            elseif subEvent == "SWING_DAMAGE" then
                amount = unpack(eventInfo, 12, 12)
                totalDamage = totalDamage + amount
            elseif subEvent == "RANGE_DAMAGE" then
                amount = unpack(eventInfo, 12, 12)
                totalDamage = totalDamage + amount
            elseif subEvent == "SPELL_PERIODIC_DAMAGE" then
                amount = unpack(eventInfo, 15, 15)
                totalDamage = totalDamage + amount
            elseif subEvent == "SPELL_HEAL" then
                amount = unpack(eventInfo, 15, 15)
                totalHealing = totalHealing + amount
            elseif subEvent == "SPELL_PERIODIC_HEAL" then
                amount = unpack(eventInfo, 15, 15)
                totalHealing = totalHealing + amount
            end 
        end

        -- damage taken
        if destGUID == playerGUID then
            if subEvent == "SPELL_DAMAGE" then
                amount = unpack(eventInfo, 15, 15)
                totalDamageTaken = totalDamageTaken + amount
            elseif subEvent == "SWING_DAMAGE" then
                amount = unpack(eventInfo, 12, 12)
                totalDamageTaken = totalDamageTaken + amount
            elseif subEvent == "RANGE_DAMAGE" then
                amount = unpack(eventInfo, 12, 12)
                totalDamageTaken = totalDamageTaken + amount
            elseif subEvent == "SPELL_PERIODIC_DAMAGE" then
                amount = unpack(eventInfo, 15, 15)
                totalDamageTaken = totalDamageTaken + amount
            end
        end

        -- deaths
        if subEvent == "UNIT_DIED" and destGUID == playerGUID then
            totalDeaths = totalDeaths + 1
        end
    end
end)
