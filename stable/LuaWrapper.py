import lupa
from lupa import LuaRuntime
from datetime import datetime, date

class LuaWrapper:
    def __init__(self, core, script_path):
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        
        SDKLua.setCore(core)
        self.begin = '''
function(obj)
    if obj.__name__ == 'SDKLua' then
        rawset(_G, 'SDKLua', obj)
    end

    VN = _G['SDKLua']

    if not VN then
        return
    end'''

        self.end = '''
end
        '''

        with open(script_path, 'r') as f:
            lines = f.readlines()
            str_temp = "\n"
            for line in lines:
        	    str_temp += ('    ') * 1 + line
            
            self.final = self.begin + str_temp + self.end;
            # print(self.final)
            self.interface = self.lua.eval(self.final)

        self.interface(SDKLua)

class SDKLua:
	core = None
	def setCore(_core):
		global core
		core = _core

	def log(message):
		now = datetime.now()
		current_time = str(now.strftime("%H:%M:%S"))
		today = str(date.today())
		msg = f"[{current_time}] {message}"
		print(msg)

	def getCore():
		return core
		