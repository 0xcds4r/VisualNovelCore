LOG_TAG = "debug"

Log = {}

function Log.print(log, special_tag)
	if special_tag ~= nil then
		VN.log("["..special_tag.."] "..log)
	else
		VN.log("["..LOG_TAG.."] "..log)
	end
end