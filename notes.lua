print("Hello World!")

local f = CreateFrame("Frame")
-- other considerations include battle ressurection count, bloodlust count etc. but let's keep things simple for now...
local parameters = {"damage", "healing", "crowdControlCount", "damageTaken", "deathCount", "pullCount", "race", "class", "specialization", "role", "itemLevel"}
local guid = nil

function f:OnEvent(event, ...)
	self[event](self, event, ...) -- call the appropriate event handler
end

function f:ADDON_LOADED(event, addOnName) -- parameters are in order and are dependent on the event (see /etrace in WoW)
	if addOnName == "LVP" then
        -- Our saved variables, if they exist, have been loaded at this point.
        if data == nil then
            -- This is the first time this addon is loaded; set SVs to default values
            data = {}
		else
			local name = UnitName("player")
			print("We meet again, "  .. name .. ". You currently have " .. #data .. " Mythic+ dungeons saved on this account.")
end

function f:PLAYER_ENTERING_WORLD(event, isLogin, isReload)
	print(event, isLogin, isReload)
end

function f:CHAT_MSG_CHANNEL(event, text, playerName, _, channelName)
	print(event, text, playerName, channelName)
end

function f:COMBAT_LOG_EVENT_UNFILTERED()
	if guid == nil then
		local _, subevent, _, sourceGUID, _, _, _, _, destName = CombatLogGetCurrentEventInfo()
		guid = sourceGUID
		local locClass, engClass, locRace, engRace, gender, name, server = GetPlayerInfoByGUID(sourceGUID)

		print("name: ", name, "\n")
		print("gender: ", gender, "\n")
		print("server: ", server, "\n")
		print("race: ", engRace, "\n")
		print("class: ", engClass, "\n")
	end

	local spellId, amount

	if subevent == "SWING_DAMAGE" then
		amount, _, _, _, _, _, critical = select(12, CombatLogGetCurrentEventInfo())
	elseif subevent == "SPELL_DAMAGE" then
		spellId, _, _, amount, _, _, _, _, _, _ = select(12, CombatLogGetCurrentEventInfo())
	end


	-- if critical and sourceGUID == playerGUID then
	-- 	-- get the link of the spell or the MELEE globalstring
	-- 	local action = spellId and GetSpellLink(spellId) or MELEE
	-- 	print(MSG_CRITICAL_HIT:format(action, destName, amount))
	-- end
end

f:RegisterEvent("ADDON_LOADED")
f:RegisterEvent("PLAYER_ENTERING_WORLD")
f:RegisterEvent("CHAT_MSG_CHANNEL")
f:RegisterEvent("PLAYER_LOGOUT")
f:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")
f:SetScript("OnEvent", f.OnEvent) -- binds f.OnEvent to run everytime an event occurs

SLASH_HAVEWEMET1 = "/hello"
function SlashCmdList.HAVEWEMET(msg)
    print("We meet again, "  .. name .. ". You currently have " .. #data .. " Mythic+ dungeons saved on this account.")
end

--- test these events
--- challenge_mode_start/completed
--- player_dead



-- 3d matrix

-- first d - mythic dungeonn id
-- second d - player id in mythic dungeon
-- third d - type of statistic (ex. dmg dealt, healign, etc.

-- current considered parameters