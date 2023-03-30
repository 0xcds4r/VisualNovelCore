function(obj)
	print("added new class: " .. obj.__name__)
	if obj.__name__ == 'Core' then
		rawset(_G, 'Core', obj)
	end

	if obj.__name__ == 'Game' then
		rawset(_G, 'Game', obj)
	end

	local Game = _G['Game']
	local Core = _G['Core']

	if not Core then
		return
	end

	if not Game then
		return
	end

	function main()
		Core:runGame()
		Game:putVar('a', {5,5,5})
		print(Game:getVar('a')[1])
	end

	main()
end