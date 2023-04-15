-- Create a new FileManager instance
local sfm = FileManager.new()

-- Define a function to save the game state to a file
function save_game(slot, content)
	-- Set the folder path to "saves"
	sfm:set_folder_path("saves")

    -- Save the game state to a file with the name "save<slot>.txt" (where <slot> is the slot number)
    sfm:save_file("save-" .. slot .. ".vncsave", content)

    -- Print a message to the console to confirm that the game was saved
    Log.print("Game saved to slot " .. slot)
end

-- Define a function to load the game state from a file
function load_game(slot)
	-- Set the folder path to "saves"
	sfm:set_folder_path("saves")

    -- Try to read the game state from a file with the name "save<slot>.txt"
    local content = sfm:read_file("save-" .. slot .. ".vncsave")

    -- If the file doesn't exist, return false to indicate that the game couldn't be loaded
    if not content then
        return false
    end

   	-- todo

    -- Print a message to the console to confirm that the game was loaded
    Log.print("Game loaded from slot " .. slot)

    -- Return true to indicate that the game was loaded successfully
    return true
end