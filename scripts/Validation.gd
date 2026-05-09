extends Node


func validate_all_inputs() -> void:
	var valid: bool = true
	var mod_screen_valid: bool = true
	var invalid_paint_jobs: Array[Node] = []
	
	var mod_screen: Node = get_node("../ScreenLoader/ModInfoScreen")
	var paint_jobs: Array[Node] = []
	for paint_job in get_node("../ScreenLoader/MainScreen/PaintJobTabContainer").get_children():
		paint_jobs.append(paint_job)
	
	var mod_name: Node = mod_screen.get_node("Name")
	var mod_name_text: String = mod_name.find_child("TextInput").text
	mod_name.warnings = []
	if mod_name_text == "":
		mod_screen_valid = false
		mod_name.warnings.append(PackedStringArray(["Mod name is blank", "Mod name cannot be blank, please enter a mod name"]))
	if has_invalid_file_character(mod_name_text):
		mod_screen_valid = false
		mod_name.warnings.append(PackedStringArray(["Mod name has invalid character", "Mod name cannot contain the following characters:\n< > : \" / \\ | ? *"]))
	if ends_in_full_stop(mod_name_text):
		mod_screen_valid = false
		mod_name.warnings.append(PackedStringArray(["Mod name ends with a full stop", "Mod name cannot end with a full stop, this character: ."]))
	if ends_in_space(mod_name_text):
		mod_screen_valid = false
		mod_name.warnings.append(PackedStringArray(["Mod name ends with a space", "Mod name cannot end with a space"]))
	if is_reserved_file_name(mod_name_text):
		mod_screen_valid = false
		mod_name.warnings.append(PackedStringArray(["Mod name is a reserved file name", "Mod name cannot be any of the following:\n CON, PRN, AUX, NUL, COM1-9, LPT1-9"]))
	
	var mod_author: Node = mod_screen.get_node("Author")
	var mod_author_text: String = mod_author.find_child("TextInput").text
	mod_author.warnings = []
	if mod_author_text == "":
		# TODO: double check if this actually can be blank
		mod_screen_valid = false
		mod_author.warnings.append(PackedStringArray(["Mod author is blank", "Mod author cannot be blank, please enter a mod author"]))
	if has_invalid_sii_character(mod_author_text):
		mod_screen_valid = false
		mod_author.warnings.append(PackedStringArray(["Mod author contains invalid characters", "Mod author cannot contain the following characters:\n\" / \\"]))
	
	var mod_version: Node = mod_screen.get_node("Version")
	var mod_version_text: String = mod_version.find_child("TextInput").text
	mod_version.warnings = []
	if mod_version_text == "":
		mod_screen_valid = false
		mod_version.warnings.append(PackedStringArray(["Mod version is blank", "Mod version cannot be blank, please enter a mod version"]))
	if has_invalid_sii_character(mod_version_text):
		mod_screen_valid = false
		mod_version.warnings.append(PackedStringArray(["Mod version contains invalid characters", "Mod version cannot contain the following characters:\n\" / \\"]))
	
	var mod_description = mod_screen.get_node("Description")
	var mod_description_text = mod_description.find_child("TextBox").text
	mod_description.warnings = []
	if mod_description_text == "":
		mod_screen_valid = false
		mod_description.warnings.append(PackedStringArray(["Mod description is blank", "Mod description cannot be blank, please enter a mod description"]))
	
	for paint_job in paint_jobs:
		var paint_job_name = paint_job.get_node("Name")
		var paint_job_name_text = paint_job_name.find_child("TextInput").text
		paint_job_name.warnings = []
		if paint_job_name == "":
			if paint_job not in invalid_paint_jobs:
				invalid_paint_jobs.append(paint_job)
			paint_job_name.warnings.append(PackedStringArray(["Paint job name is blank", "Paint job name cannot be blank, please enter a paint job name"]))
		if has_invalid_file_character(paint_job_name_text):
			if paint_job not in invalid_paint_jobs:
				invalid_paint_jobs.append(paint_job)
			paint_job_name.warnings.append(PackedStringArray(["Paint job name contains invalid characters", "Paint job name cannot contain the following characters:\n< > : \" / \\ | ? *"]))
		if ends_in_full_stop(paint_job_name_text):
			if paint_job not in invalid_paint_jobs:
				invalid_paint_jobs.append(paint_job)
			paint_job_name.warnings.append(PackedStringArray(["Paint job name ends with a full stop", "Paint job name cannot end with a full stop, this character: ."]))
		if ends_in_space(paint_job_name_text):
			if paint_job not in invalid_paint_jobs:
				invalid_paint_jobs.append(paint_job)
			paint_job_name.warnings.append(PackedStringArray(["Paint job name ends with a space", "Paint job name cannot end with a space"]))
		if is_reserved_file_name(paint_job_name_text):
			if paint_job not in invalid_paint_jobs:
				invalid_paint_jobs.append(paint_job)
			paint_job_name.warnings.append(PackedStringArray(["Paint job name is a reserved file name", "Paint job name cannot be any of the following:\nCON, PRN, AUX, NUL, COM1-9, LPT1-9"]))
		if not is_ascii(paint_job_name_text):
			if paint_job not in invalid_paint_jobs:
				invalid_paint_jobs.append(paint_job)
			paint_job_name.warnings.append(PackedStringArray(["Paint job name is not ASCII", "Paint job name can only contain ASCII characters:\nabcdefghijklmnopqrstuvwxyz\nABCDEFGHIJKLMNOPQRSTUVWXYZ\n0123456789\n! @ # $ % ^ & ( ) - _ = + [ ] { } ; ' , ` ~"]))
		paint_job_name.find_child("TextInput").text = remove_escape_characters(paint_job_name_text)
		
		#if not paint_job.get_node("Unlock").find_child("CheckboxInput").button_pressed:
			#if paint_job.get_node("Unlock").find_child("NumberInput")
	
	
	
	
	
	
	if valid:
		pass # change screen
	else:
		pass # do not pass go
		# if warnings only on one screen, switch to that screen
		# if warnings only on one paint job, switch to that paint job
	
	

func ends_in_space(input: String) -> bool:
	return input.substr(len(input) - 1) == " "


func ends_in_full_stop(input: String) -> bool:
	return input.substr(len(input) - 1) == "."


func is_alphanumeric(input: String) -> bool:
	var alphanumeric: bool = true
	for letter in input:
		if letter not in "abcdefghijklmnopqrstuvwxyz0123456789_":
			alphanumeric = false
	return alphanumeric


func is_ascii(input: String) -> bool:
	var ascii: bool = true
	for letter in input:
		if letter not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&()-_=+[]{};',`~ ":
			ascii = false
	return ascii


func is_number(input: String) -> bool:
	return input.is_valid_int()


func has_invalid_file_character(input: String) -> bool:
	var invalid_character: bool = false
	for character in ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]:
		if character in input:
			invalid_character = true
	return invalid_character


func has_invalid_sii_character(input: String) -> bool:
	var invalid_character: bool = false
	for character in ["\"", "/", "\\"]:
		if character in input:
			invalid_character = true
	return invalid_character


func is_reserved_file_name(input: String) -> bool:
	var reserved_names: PackedStringArray = ["CON", "PRN", "AUX", "NUL"]
	for i in range(9):
		reserved_names.append("COM" + str(i + 1))
		reserved_names.append("LPT" + str(i + 1))
	var is_reserved: bool = false
	for res_name in reserved_names:
		if input.to_upper() == res_name:
			is_reserved = true
	return is_reserved


func remove_escape_characters(input: String) -> String:
	return input.strip_escapes()


func remove_diacritics(input: String) -> String:
	return TextServerManager.get_primary_interface().strip_diacritics(input)


func internal_name_too_long(paint_job_tab: Node) -> bool:
	if paint_job_tab.find_child("SplitPaintJobs").selected == 0:
		return len(paint_job_tab.find_child("InternalName").find_child("TextInput").text) > 12
	else:
		return len(paint_job_tab.find_child("InternalName").find_child("TextInput").text) > 10


func incompatible_vehicles(paint_job_tab: Node) -> Array:
	var selected_list: Array[PackedStringArray] = []
	for child in paint_job_tab.find_child("VehicleTabContainer").get_children():
		for selection in child.find_child("VBoxContainer").get_children():
			if selection.find_child("VehicleCheckbox").button_pressed:
				selected_list.append(PackedStringArray([selection.vehicle_dict["path"], selection.vehicle_dict["name"]]))
				
	var identical_list: Array[PackedStringArray] = []
	for i in range(len(selected_list)):
		for j in range(i + 1, len(selected_list)):
			if selected_list[i][0] == selected_list[j][0]:
				identical_list.append(PackedStringArray([selected_list[i][1], selected_list[j][1]]))
	return identical_list


func non_unique_internal_names(paint_job_tabs: Array[Node]) -> bool:
	var name_list: PackedStringArray
	var non_unique: bool = false
	for tab in paint_job_tabs:
		name_list.append(tab.find_child("Name").find_child("TextInput").text)
	for i in range(len(name_list)):
		for j in range(i + 1, len(name_list)):
			if name_list[i][0] == name_list[j][0]:
				non_unique = true
	return non_unique

func no_vehicles_selected(paint_job_tab: Node) -> bool:
	var no_vehicles: bool = true
	for child in paint_job_tab.find_child("VehicleTabContainer").get_children():
		for selection in child.find_child("VBoxContainer").get_children():
			if selection.find_child("VehicleCheckbox").button_pressed:
				no_vehicles = false
	return no_vehicles
