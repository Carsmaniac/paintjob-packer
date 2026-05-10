extends Node


func validate_all_inputs() -> void:
	var mod_screen_valid: bool = true
	var internal_names_valid: bool = true
	var invalid_paint_jobs: Array[Node] = []
	var warnings: PackedStringArray = []
	
	var mod_screen: Node = get_node("../ScreenLoader/ModInfoScreen")
	var paint_jobs: Array[Node] = []
	for paint_job in get_node("../ScreenLoader/MainScreen/PaintJobTabContainer").get_children():
		paint_jobs.append(paint_job)
	
	var mod_name: Node = mod_screen.get_node("Panel/Name")
	var mod_name_text: String = mod_name.find_child("TextInput").text
	mod_name.warnings = []
	if mod_name_text == "":
		mod_screen_valid = false
		mod_name.warnings.append(PackedStringArray(["Mod name is blank", "Mod name cannot be blank, please enter a mod name"]))
		warnings.append("Mod name is blank")
	if has_invalid_file_character(mod_name_text):
		mod_screen_valid = false
		mod_name.warnings.append(PackedStringArray(["Mod name contains invalid character", "Mod name cannot contain the following characters:\n< > : \" / \\ | ? *"]))
		warnings.append("Mod name contains invalid characters")
	if ends_in_full_stop(mod_name_text):
		mod_screen_valid = false
		mod_name.warnings.append(PackedStringArray(["Mod name ends with a full stop", "Mod name cannot end with a full stop ( . )"]))
		warnings.append("Mod name ends with a full stop")
	if ends_in_space(mod_name_text):
		mod_screen_valid = false
		mod_name.warnings.append(PackedStringArray(["Mod name ends with a space", "Mod name cannot end with a space"]))
		warnings.append("Mod name ends with a space")
	if is_reserved_file_name(mod_name_text):
		mod_screen_valid = false
		mod_name.warnings.append(PackedStringArray(["Mod name is a reserved file name", "Mod name cannot be any of the following:\n CON, PRN, AUX, NUL, COM1-9, LPT1-9"]))
		warnings.append("Mod name is a reserved file name")
	mod_name.show_hide_warning_button()
	
	var mod_author: Node = mod_screen.get_node("Panel/Author")
	var mod_author_text: String = mod_author.find_child("TextInput").text
	mod_author.warnings = []
	if mod_author_text == "":
		# TODO: double check if this actually can be blank
		mod_screen_valid = false
		mod_author.warnings.append(PackedStringArray(["Mod author is blank", "Mod author cannot be blank, please enter a mod author"]))
		warnings.append("Mod author is blank")
	if has_invalid_sii_character(mod_author_text):
		mod_screen_valid = false
		mod_author.warnings.append(PackedStringArray(["Mod author contains invalid characters", "Mod author cannot contain the following characters:\n\" / \\"]))
		warnings.append("Mod author contains invalid characters")
	mod_author.show_hide_warning_button()
	
	var mod_version: Node = mod_screen.get_node("Panel/Version")
	var mod_version_text: String = mod_version.find_child("TextInput").text
	mod_version.warnings = []
	if mod_version_text == "":
		mod_screen_valid = false
		mod_version.warnings.append(PackedStringArray(["Mod version is blank", "Mod version cannot be blank, please enter a mod version"]))
		warnings.append("Mod version is blank")
	if has_invalid_sii_character(mod_version_text):
		mod_screen_valid = false
		mod_version.warnings.append(PackedStringArray(["Mod version contains invalid characters", "Mod version cannot contain the following characters:\n\" / \\"]))
		warnings.append("Mod version contains invalid characters")
	mod_version.show_hide_warning_button()
	
	var mod_description = mod_screen.get_node("Panel/Description")
	var mod_description_text = mod_description.find_child("TextBox").text
	mod_description.warnings = []
	if mod_description_text == "":
		mod_screen_valid = false
		mod_description.warnings.append(PackedStringArray(["Mod description is blank", "Mod description cannot be blank, please enter a mod description"]))
		warnings.append("Mod description is blank")
	mod_description.show_hide_warning_button()
	
	for paint_job in paint_jobs:
		if paint_job.name != "+":
			var paint_job_name = paint_job.get_node("Name")
			var paint_job_name_text = paint_job_name.find_child("TextInput").text
			paint_job_name.warnings = []
			if paint_job_name_text == "":
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				paint_job_name.warnings.append(PackedStringArray(["Paint job name is blank", "Paint job name cannot be blank, please enter a paint job name"]))
				warnings.append("Paint job name is blank")
			if has_invalid_file_character(paint_job_name_text):
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				paint_job_name.warnings.append(PackedStringArray(["Paint job name contains invalid characters", "Paint job name cannot contain the following characters:\n< > : \" / \\ | ? *"]))
				warnings.append("Paint job name contains invalid characters")
			if ends_in_full_stop(paint_job_name_text):
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				paint_job_name.warnings.append(PackedStringArray(["Paint job name ends with a full stop", "Paint job name cannot end with a full stop ( . )"]))
				warnings.append("Paint job name ends with a full stop")
			if ends_in_space(paint_job_name_text):
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				paint_job_name.warnings.append(PackedStringArray(["Paint job name ends with a space", "Paint job name cannot end with a space"]))
				warnings.append("Paint job name ends with a space")
			if is_reserved_file_name(paint_job_name_text):
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				paint_job_name.warnings.append(PackedStringArray(["Paint job name is a reserved file name", "Paint job name cannot be any of the following:\nCON, PRN, AUX, NUL, COM1-9, LPT1-9"]))
				warnings.append("Paint job name is a reserved file name")
			if not is_ascii(paint_job_name_text):
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				paint_job_name.warnings.append(PackedStringArray(["Paint job name is not ASCII", "Paint job name can only contain ASCII characters:\nabcdefghijklmnopqrstuvwxyz\nABCDEFGHIJKLMNOPQRSTUVWXYZ\n0123456789\n! @ # $ % ^ & ( ) - _ = + [ ] { } ; ' , ` ~"]))
				warnings.append("Paint job name is not ASCII")
			paint_job_name.find_child("TextInput").text = remove_escape_characters(paint_job_name_text)
			paint_job_name.show_hide_warning_button()
			
			if paint_job.get_node("Unlock").find_child("NumberInput").value == 0:
				paint_job.get_node("Unlock").find_child("CheckboxInput").button_pressed = true
			elif paint_job.get_node("Unlock").find_child("CheckboxInput").button_pressed == true:
				paint_job.get_node("Unlock").find_child("NumberInput").value = 0
				
			var internal_name = paint_job.get_node("InternalName")
			var internal_name_text = internal_name.find_child("TextInput").text
			internal_name.warnings = []
			if internal_name_text == "":
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				internal_name.warnings.append(PackedStringArray(["Internal name is blank", "Internal name cannot be blank, please enter an internal name"]))
				warnings.append("Paint job internal name is blank")
			if internal_name_too_long(paint_job):
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				if paint_job.get_node("SplitPaintJobs").find_child("DropdownInput").selected == 0:
					internal_name.warnings.append(PackedStringArray(["Internal name is too long", "Internal name cannot be longer than 12 characters"]))
				else:
					internal_name.warnings.append(PackedStringArray(["Internal name is too long", "Internal name cannot be longer than 10 characters"]))
				warnings.append("Paint job internal name is too long")
			if not is_alphanumeric(internal_name_text):
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				internal_name.warnings.append(PackedStringArray(["Internal name is not alphanumeric", "Internal name can only contain the following characters, with no spaces:\nabcdefghijkjlmnopqrstuvwxyz\n0123456789_"]))
				warnings.append("Paint job internal name is not alphanumeric")
			if is_reserved_file_name(internal_name_text):
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				internal_name.warnings.append(PackedStringArray(["Internal name is a reserved file name", "Internal name cannot be any of the following:\nCON, PRN, AUX, NUL, COM1-9, LPT1-9"]))
				warnings.append("Paint job internal name is a reserved file name")
			internal_name.show_hide_warning_button()
			
			paint_job.warnings = []
			if no_vehicles_selected(paint_job):
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				paint_job.warnings.append(PackedStringArray(["No vehicles selected", "Please select at least one truck, trailer or mod for your paint job to support"]))
				warnings.append("No vehicles selected")
			var incompat_vehicles: Array[PackedStringArray] = incompatible_vehicles(paint_job)
			if len(incompat_vehicles) > 0:
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				var incompat_string: PackedStringArray = []
				for pair in incompat_vehicles:
					incompat_string.append(" and ".join(pair))
				paint_job.warnings.append(PackedStringArray(["Incompatible vehicles", "\n".join(incompat_string)]))
				warnings.append("Incompatible vehicles")
			paint_job.show_hide_warning_button()
	
	var non_unique_names: Array[PackedStringArray] = non_unique_internal_names(paint_jobs)
	if len(non_unique_names) > 0:
		internal_names_valid = false
		var duplicate_names: String = ""
		for names in non_unique_names:
			duplicate_names += " and ".join(names) + "\n"
		duplicate_names = duplicate_names.substr(0, len(duplicate_names) - 1)
		# paint_jobs[0] is the scapegoat here, it really doesn't deserve all this
		paint_jobs[0].get_node("InternalName").warnings.append(PackedStringArray(["Conflicting internal names", "The following paint jobs have the same internal names:\n" + duplicate_names]))
		warnings.append("Conflicting paint job internal names")
		if paint_jobs[0] not in invalid_paint_jobs:
			invalid_paint_jobs.append(paint_jobs[0])
		paint_jobs[0].get_node("InternalName").show_hide_warning_button()
	
	if len(warnings) > 0:
		var popup := AcceptDialog.new()
		popup.title = "Warning"
		popup.dialog_text = "The following errors need to be fixed before continuing:\n\n%s\n" % "\n".join(warnings)
		popup.size.y = 0
		popup.ok_button_text = "Okay"
		popup.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
		self.add_child(popup)
		popup.popup_centered()
	if mod_screen_valid and len(invalid_paint_jobs) == 0 and internal_names_valid:
		get_node("../ScreenLoader").switch_screen(true)
	elif len(invalid_paint_jobs) == 0:
		get_node("../ScreenLoader").switch_screen(false)
	else:
		var tab_container: Node = get_node("../ScreenLoader/MainScreen/PaintJobTabContainer")
		tab_container.current_tab = tab_container.get_tab_idx_from_control(invalid_paint_jobs[0])
		# TODO: warn about bus mod stuff
		# ErrorBus1=Because of limitations of the game, bus mods use a workaround in order for paint jobs to appear on their doors. This means that paint job mods work a little strangely, and will not affect the vehicles' doors. ; The first part of the message displayed when making a paint job for a bus, explaining how bus paint jobs differ from truck/trailer paint jobs when trying to paint their doors
		# ErrorBus2=Any paint jobs generated by Paint Job Packer for bus mods will have a color picker, which will allow you to change the color of the doors, however you'll be unable to apply patterns/logos/text/etc to them. ; The second part of the message displayed when making a paint job for a bus, explaining how bus paint jobs differ from truck/trailer paint jobs when trying to paint their doors
		# ErrorBus3=In order to make a paint job for a bus mod that works properly, try replacing the texture files of an existing paint job, instead of making a brand new one. If you choose to continue, expect some weirdness with your mod, and note that it cannot be fixed.


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
	if paint_job_tab.find_child("SplitPaintJobs").find_child("DropdownInput").selected == 0:
		return len(paint_job_tab.find_child("InternalName").find_child("TextInput").text) > 12
	else:
		return len(paint_job_tab.find_child("InternalName").find_child("TextInput").text) > 10


func incompatible_vehicles(paint_job_tab: Node) -> Array:
	var selected_list: Array[PackedStringArray] = []
	for child in paint_job_tab.find_child("VehicleTabContainer").get_children():
		for selection in child.find_child("VBoxContainer").get_children():
			if selection.find_child("VehicleCheckbox").button_pressed:
				if selection.vehicle_dict["mod"]:
					selected_list.append(PackedStringArray([selection.vehicle_dict["path"], "%s's %s" % [selection.vehicle_dict["mod_author"], selection.vehicle_dict["name"]]]))
				else:
					selected_list.append(PackedStringArray([selection.vehicle_dict["path"], selection.vehicle_dict["name"]]))
				
	var identical_list: Array[PackedStringArray] = []
	for i in range(len(selected_list)):
		for j in range(i + 1, len(selected_list)):
			if selected_list[i][0] == selected_list[j][0]:
				identical_list.append(PackedStringArray([selected_list[i][1], selected_list[j][1]]))
	return identical_list


func non_unique_internal_names(paint_job_tabs: Array[Node]) -> Array[PackedStringArray]:
	var name_list: Array[PackedStringArray]
	var non_unique: Array[PackedStringArray]
	for tab in paint_job_tabs:
		name_list.append(PackedStringArray([tab.find_child("InternalName").find_child("TextInput").text, tab.find_child("Name").find_child("TextInput").text]))
	for i in range(len(name_list)):
		for j in range(i + 1, len(name_list)):
			if name_list[i][0] == name_list[j][0]:
				if name_list[i][1] != "" and name_list[j][1] != "":
					non_unique.append(PackedStringArray([name_list[i][1], name_list[j][1]]))
	return non_unique

func no_vehicles_selected(paint_job_tab: Node) -> bool:
	var no_vehicles: bool = true
	for child in paint_job_tab.find_child("VehicleTabContainer").get_children():
		for selection in child.find_child("VBoxContainer").get_children():
			if selection.find_child("VehicleCheckbox").button_pressed:
				no_vehicles = false
	return no_vehicles
