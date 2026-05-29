extends Control

var github_link: String = "https://github.com/Carsmaniac/paintjob-packer?tab=contributing-ov-file"
var weblate_link: String = "https://hosted.weblate.org/projects/paint-job-packer/paint-job-packer/"


func _ready() -> void:
	get_node("../SetupScreen/Panel/UpdateChecker/UpdateButton").connect("pressed", open_update_link)
	fetch_version_json()
	
	#if not FileAccess.file_exists("user://popup_seen.dat"):
		#var popup := AcceptDialog.new()
		#popup.title = tr("Single Popup")
		#popup.dialog_text = "This popup should only appear once\n"
		#popup.max_size[0] = 500
		#popup.dialog_autowrap = true
		#popup.size.y = 0
		#popup.ok_button_text = tr("BUTTON_OKAY")
		#popup.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
		#self.add_child(popup)
		#popup.popup_centered()
	#
	#var save_file := FileAccess.open("user://popup_seen.dat", FileAccess.WRITE)
	#save_file.store_string("seen")
	#save_file.close()


func open_github_link() -> void:
	OS.shell_open(github_link)


func open_weblate_link() -> void:
	OS.shell_open(weblate_link)


func open_update_link() -> void:
	OS.shell_open("https://carsmani.ac/paint-job-packer#downloads")


func fetch_version_json() -> void:
	var http_request := HTTPRequest.new()
	add_child(http_request)
	http_request.connect("request_completed", process_version_json)
	var _error = http_request.request("https://carsmani.ac/paint-job-packer.json")


func process_version_json(_result:int , _response_code: int, _headers: PackedStringArray, body: PackedByteArray) -> void:
	var json := JSON.new()
	if json.parse(body.get_string_from_utf8()) == OK:
		var json_data = json.get_data()
		
		if json_data["format_version"] == 1:
			github_link = json_data["github_link"]
			weblate_link = json_data["translation_link"]
			
			var version_string := PackedStringArray(ProjectSettings.get_setting("application/config/version").split("."))
			var version: PackedInt32Array
			if len(version_string) == 2:
				version_string.append("0")
			for string in version_string:
				version.append(string.to_int())
			
			var new_version_string := PackedStringArray(json_data["version"].split("."))
			var new_version: PackedInt32Array
			if len(new_version_string) == 2:
				new_version_string.append("0")
			for string in new_version_string:
				new_version.append(string.to_int())
			
			var update_checker: Node = get_node("../SetupScreen/Panel/UpdateChecker")
			if new_version[0] > version[0]:
				update_checker.visible = true
			elif new_version[1] > version[1]:
				update_checker.visible = true
			elif new_version[2] > version[2]:
				update_checker.visible = true
