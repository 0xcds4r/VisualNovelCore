local FileManager = {}
FileManager.__index = FileManager

function FileManager.new()
    local self = setmetatable({}, FileManager)
    self.fm = core.getFileManager()
    return self
end

-- Define Lua functions that call the methods of the FileManager instance stored in the userdata

function FileManager:set_folder_path(path)
    self.fm:set_folder_path(path)
end

function FileManager:create_file(file_name, content, flag)
    if flag ~= nil then
        self.fm:create_file(file_name, content, flag)
    else
        self.fm:create_file(file_name, content)
    end
end

function FileManager:edit_file(file_name, new_content, flag)
    if flag ~= nil then
        self.fm:edit_file(file_name, new_content, flag)
    else
        self.fm:edit_file(file_name, new_content)
    end
end

function FileManager:read_file(file_name, flag)
    if flag ~= nil then
        return self.fm:read_file(file_name, flag)
    else
        return self.fm:read_file(file_name)
    end
end

function FileManager:save_file(file_name, content, flagIfExists, flagIfNotExists)
    if flagIfExists ~= nil and flagIfNotExists ~= nil then
        self.fm:save_file(file_name, content, flagIfExists, flagIfNotExists)
    else
        if flagIfExists ~= nil then
            self.fm:save_file(file_name, content, flagIfExists)
        else
            self.fm:save_file(file_name, content)
        end
    end
end

function FileManager:read_file_lines(file_name, flag)
    if flag ~= nil then
        return self.fm:read_file_lines(file_name, flag)
    else
        return self.fm:read_file_lines(file_name)
    end
end

function FileManager:read_file_delimited(file_name, delimiter)
    return self.fm:read_file_delimited(file_name, delimiter)
end