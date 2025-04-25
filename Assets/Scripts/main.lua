MythicPlusStatsDB = MythicPlusStatsDB or {}

function customPrint(...)
    local prefix = "|cffFFD700LVP|r: "  -- Gold color
    local args = {...}
    local message = table.concat(args, " ")
    print(prefix .. message)
end

-- dungeon ends
local totalDamage = 0
local totalHealing = 0
local totalDamageTaken = 0
local totalDeaths = 0
local inMythicDungeon = false
local totalInterrupts = 0

-- dungeon starts
local characterName = nil
local characterRealm = nil
local timeStart = nil
local className = nil
local specIndex = nil
local specName = nil
local specRole = nil

local dungeonId = nil
local dungeonLevel = nil
local dungeonName = nil
local dungeonSeed = nil

local hitLog = {}

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
        totalInterrupts = 0
        hitLog = {}

        characterName = UnitName("player")
        characterRealm = GetRealmName()
        timeStart = date("%Y-%m-%d %H:%M:%S")
        className = select(2, UnitClass("player"))
        specIndex = GetSpecialization()
        specName = specIndex and select(2, GetSpecializationInfo(specIndex)) or "Unknown"
        specRole = GetSpecializationRole(specIndex)

        dungeonId = C_ChallengeMode.GetActiveChallengeMapID()
        dungeonLevel, _, _ = C_ChallengeMode.GetActiveKeystoneInfo()
        dungeonName = C_ChallengeMode.GetMapUIInfo(dungeonId)
        dungeonSeed = C_ChallengeMode.GetSlottedKeystoneInfo()

        customPrint("Mythic+ started. Tracking active.")
        customPrint("Class:", className, "| Spec:", specName, "| Role:", specRole)
        customPrint("id:", dungeonId, "| name:", dungeonName, "| level:", dungeonLevel, "| seed:", dungeonSeed)

    elseif event == "CHALLENGE_MODE_COMPLETED" then
        inMythicDungeon = false
        table.insert(MythicPlusStatsDB, {
            timeStart = timeStart,
            name = characterName,
            realm = characterRealm,
            dungeonName = dungeonName,
            dungeonId = dungeonId,
            dungeonLevel = dungeonLevel,
            dungeonSeed = dungeonSeed,
            class = className,
            spec = specName,
            role = specRole,
            timeEnd = date("%Y-%m-%d %H:%M:%S"),
            totalDamage = totalDamage,
            totalHealing = totalHealing,
            totalDamageTaken = totalDamageTaken,
            totalDeaths = totalDeaths,
            totalInterrupts = totalInterrupts,
            hitLog = hitLog
        })
        customPrint("Mythic+ completed.")
        customPrint("Total damage dealt:", totalDamage)
        customPrint("Total healing done:", totalHealing)
        customPrint("Damage taken:", totalDamageTaken)
        customPrint("Deaths:", totalDeaths)

    elseif event == "COMBAT_LOG_EVENT_UNFILTERED" and inMythicDungeon then
        local eventInfo = {CombatLogGetCurrentEventInfo()}
        local timestamp, subEvent, hideCaster, sourceGUID, sourceName, sourceFlags, sourceRaidFlags, destGUID, destName, destFlags, destRaidFlags = unpack(eventInfo, 1, 11)
        local spellID, spellName, spellSchool, amount, overhealing, absorbed, critical = unpack(eventInfo, 12, 18)

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

        -- interrupts
        if subEvent == "SPELL_INTERRUPT" and sourceGUID == playerGUID then
            totalInterrupts = totalInterrupts + 1
        end

        -- -- track what players got hit by
        -- local abilityDamageEvents = {
        --     SPELL_DAMAGE = true,
        --     SPELL_PERIODIC_DAMAGE = true,
        -- }

        -- if abilityDamageEvents[subEvent] and destGUID == playerGUID then
        --     local logEntry = {
        --         spell = spellName,
        --         source = sourceName,
        --         time = date("%Y-%m-%d %H:%M:%S"),
        --         amount = amount
        --     }
        --     table.insert(hitLog, logEntry)
        -- end
    end
end)
