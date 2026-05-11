extends Control


var status_array: PackedStringArray = [tr("EXPORT_SELECT"), "", ""]
var valid_folder: bool = false
var mod_name: String
var current_path: String = ""


func update_values() -> void:
	change_image(get_node("Panel/PlaceholderDropdown").selected)
	change_status("")
	change_warning()
	if mod_name != get_node("../ModInfoScreen/Panel/Name/TextInput").text:
		verify_path(current_path)


func change_image(dropdown_index: int) -> void:
	var game: String = get_node("..").loaded_game
	get_node("Panel/PlaceholderImageATS").visible = false
	get_node("Panel/PlaceholderImageETS").visible = false
	get_node("Panel/TemplateImageATS").visible = false
	get_node("Panel/TemplateImageETS").visible = false
	if dropdown_index == 0 and game == "ats":
		get_node("Panel/PlaceholderImageATS").visible = true
	elif dropdown_index == 0 and game == "ets":
		get_node("Panel/PlaceholderImageETS").visible = true
	elif dropdown_index == 1 and game == "ats":
		get_node("Panel/TemplateImageATS").visible = true
	elif dropdown_index == 1 and game == "ets":
		get_node("Panel/TemplateImageETS").visible = true


func choose_path() -> void:
	var export_window := FileDialog.new()
	export_window.title = tr("EXPORT_TTILE")
	export_window.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
	export_window.use_native_dialog = true
	export_window.file_mode = FileDialog.FILE_MODE_OPEN_DIR
	export_window.connect("dir_selected", verify_path)
	get_node("..").add_child(export_window)
	export_window.popup_file_dialog()


func verify_path(file_path: String) -> void:
	mod_name = get_node("../ModInfoScreen/Panel/Name/TextInput").text
	if file_path != "":
		if not DirAccess.dir_exists_absolute(file_path + "/" + mod_name):
			valid_folder = true
			current_path = file_path
		else:
			valid_folder = false
			current_path = ""
			var popup := AcceptDialog.new()
			popup.title = tr("EXPORT_EXISTST")
			popup.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
			popup.dialog_text = tr("EXPORT_EXISTS") % [file_path, mod_name] + "\n\n" + tr("EXPORT_EXISTS2") % mod_name + "\n"
			popup.size.y = 0
			popup.ok_button_text = tr("BUTTON_OKAY")
			self.add_child(popup)
			popup.popup_centered()
		update_values()


func change_warning() -> void:
	if current_path == "":
		get_node("Panel/LocationLabel").text = tr("EXPORT_SELECT")
	else:
		get_node("Panel/LocationLabel").text = tr("EXPORT_FOLDER") % (current_path + "/" + mod_name)
	if valid_folder:
		get_node("Panel/WarningLabel").text = tr("EXPORT_CREATE") % mod_name
	else:
		get_node("Panel/WarningLabel").text = ""


func change_status(new_message: String = "") -> void:
	if new_message == "":
		if valid_folder:
			status_array = PackedStringArray([tr("EXPORT_READY"), "", ""])
			get_node("Panel/ExportButton").disabled = false
		else:
			status_array = PackedStringArray([tr("EXPORT_SELECT"), "", ""])
			get_node("Panel/ExportButton").disabled = true
	else:
		var __ = status_array.insert(0, new_message)
		status_array.remove_at(3)
	get_node("Panel/StatusLabel").text = "\n".join(status_array)


func update_localisation() -> void:
	change_status()
	change_warning()
