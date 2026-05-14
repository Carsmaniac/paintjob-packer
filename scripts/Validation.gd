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
		mod_name.warnings.append(PackedStringArray([tr("WARN_MNAME_BLANKS"), tr("WARN_MNAME_BLANK")]))
		warnings.append(tr("WARN_MNAME_BLANKS"))
	if has_invalid_file_character(mod_name_text):
		mod_screen_valid = false
		mod_name.warnings.append(PackedStringArray([tr("WARN_MNAME_INVALS"), tr("WARN_MNAME_INVAL") + "\n< > : \" / \\ | ? *"]))
		warnings.append(tr("WARN_MNAME_INVALS"))
	if ends_in_full_stop(mod_name_text):
		mod_screen_valid = false
		mod_name.warnings.append(PackedStringArray([tr("WARN_MNAME_FULLS"), tr("WARN_MNAME_FULL") + " ( . )"]))
		warnings.append(tr("WARN_MNAME_FULLS"))
	if ends_in_space(mod_name_text):
		mod_screen_valid = false
		mod_name.warnings.append(PackedStringArray([tr("WARN_MNAME_SPCS"), tr("WARN_MNAME_SPC")]))
		warnings.append(tr("WARN_MNAME_SPCS"))
	if is_reserved_file_name(mod_name_text):
		mod_screen_valid = false
		mod_name.warnings.append(PackedStringArray([tr("WARN_MNAME_RESERS"), tr("WARN_MNAME_RESER") + "\n CON, PRN, AUX, NUL, COM1-9, LPT1-9"]))
		warnings.append(tr("WARN_MNAME_RESERS"))
	mod_name.show_hide_warning_button()
	
	var mod_author: Node = mod_screen.get_node("Panel/Author")
	var mod_author_text: String = mod_author.find_child("TextInput").text
	mod_author.warnings = []
	#if mod_author_text == "":
		#mod_screen_valid = false
		#mod_author.warnings.append(PackedStringArray([tr("WARN_MAUTH_BLANKS"), tr("WARN_MAUTH_BLANK")]))
		#warnings.append(tr("WARN_MAUTH_BLANKS"))
	if has_invalid_sii_character(mod_author_text):
		mod_screen_valid = false
		mod_author.warnings.append(PackedStringArray([tr("WARN_MAUTH_INVALS"), tr("WARN_MAUTH_INVAL") + "\n\" / \\"]))
		warnings.append(tr("WARN_MAUTH_INVALS"))
	mod_author.show_hide_warning_button()
	
	var mod_version: Node = mod_screen.get_node("Panel/Version")
	var mod_version_text: String = mod_version.find_child("TextInput").text
	mod_version.warnings = []
	#if mod_version_text == "":
		#mod_screen_valid = false
		#mod_version.warnings.append(PackedStringArray([tr("WARN_MVER_BLANKS"), tr("WARN_MVER_BLANK")]))
		#warnings.append(tr("WARN_MVER_BLANKS"))
	if has_invalid_sii_character(mod_version_text):
		mod_screen_valid = false
		mod_version.warnings.append(PackedStringArray([tr("WARN_MVER_INVALS"), tr("WARN_MVER_INVAL") + "\n\" / \\"]))
		warnings.append(tr("WARN_MVER_INVALS"))
	mod_version.show_hide_warning_button()
	
	#var mod_description = mod_screen.get_node("Panel/Description")
	#var mod_description_text = mod_description.find_child("TextBox").text
	#mod_description.warnings = []
	#if mod_description_text == "":
		#mod_screen_valid = false
		#mod_description.warnings.append(PackedStringArray([tr("WARN_MDESC_BLANKS"), tr("WARN_MDESC_BLANK")]))
		#warnings.append(tr("WARN_MDESC_BLANKS"))
	#mod_description.show_hide_warning_button()
	
	for paint_job in paint_jobs:
		if paint_job.name != "+":
			var paint_job_name = paint_job.get_node("Name")
			var paint_job_name_text = paint_job_name.find_child("TextInput").text
			paint_job_name.warnings = []
			if paint_job_name_text == "":
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				paint_job_name.warnings.append(PackedStringArray([tr("WARN_PNAME_BLANKS"), tr("WARN_PNAME_BLANK")]))
				warnings.append(tr("WARN_PNAME_BLANKS"))
			if has_invalid_file_character(paint_job_name_text):
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				paint_job_name.warnings.append(PackedStringArray([tr("WARN_PNAME_INVALS"), tr("WARN_PNAME_INVAL") + "\n< > : \" / \\ | ? *"]))
				warnings.append(tr("WARN_PNAME_INVALS"))
			if ends_in_full_stop(paint_job_name_text):
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				paint_job_name.warnings.append(PackedStringArray([tr("WARN_PNAME_FULLS"), tr("WARN_PNAME_FULL")]))
				warnings.append(tr("WARN_PNAME_FULLS"))
			if ends_in_space(paint_job_name_text):
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				paint_job_name.warnings.append(PackedStringArray([tr("WARN_PNAME_SPCS"), tr("WARN_PNAME_SPC")]))
				warnings.append(tr("WARN_PNAME_SPCS"))
			if is_reserved_file_name(paint_job_name_text):
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				paint_job_name.warnings.append(PackedStringArray([tr("WARN_PNAME_RESERS"), tr("WARN_PNAME_RESER") + "\nCON, PRN, AUX, NUL, COM1-9, LPT1-9"]))
				warnings.append(tr("WARN_PNAME_RESERS"))
			if not is_ascii(paint_job_name_text):
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				paint_job_name.warnings.append(PackedStringArray([tr("WARN_PNAME_ASCIIS"), tr("WARN_PNAME_ASCII") + "\nabcdefghijklmnopqrstuvwxyz\nABCDEFGHIJKLMNOPQRSTUVWXYZ\n0123456789\n! @ # $ % ^ & ( ) - _ = + [ ] { } ; ' , ` ~"]))
				warnings.append(tr("WARN_PNAME_ASCIIS"))
			paint_job_name.find_child("TextInput").text = remove_escape_characters(paint_job_name_text)
			paint_job_name.show_hide_warning_button()
			
			var price = paint_job.get_node("Price")
			var price_value = price.find_child("NumberInput").value
			price.warnings = []
			if price_value == 0:
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				price.warnings.append(PackedStringArray([tr("WARN_PRICE_ZEROS"), tr("WARN_PRICE_ZERO")]))
				warnings.append(tr("WARN_PRICE_ZEROS"))
			price.show_hide_warning_button()
			
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
				internal_name.warnings.append(PackedStringArray([tr("WARN_INAME_BLANKS"), tr("WARN_INAME_BLANK")]))
				warnings.append(tr("WARN_INAME_BLANKW"))
			if internal_name_too_long(paint_job):
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				if paint_job.get_node("SplitPaintJobs").find_child("DropdownInput").selected == 0:
					internal_name.warnings.append(PackedStringArray([tr("WARN_INAME_LONGS"), tr("WARN_INAME_LONG12")]))
				else:
					internal_name.warnings.append(PackedStringArray([tr("WARN_INAME_LONGS"), tr("WARN_INAME_LONG10")]))
				warnings.append(tr("WARN_INAME_LONGW"))
			if not is_alphanumeric(internal_name_text):
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				internal_name.warnings.append(PackedStringArray([tr("WARN_INAME_ALPHAS"), tr("WARN_INAME_ALPHA") + "\nabcdefghijkjlmnopqrstuvwxyz\n0123456789_"]))
				warnings.append(tr("WARN_INAME_ALPHAW"))
			if is_reserved_file_name(internal_name_text):
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				internal_name.warnings.append(PackedStringArray([tr("WARN_INAME_RESERS"), tr("WARN_INAME_RESER") + "\nCON, PRN, AUX, NUL, COM1-9, LPT1-9"]))
				warnings.append(tr("WARN_INAME_RESERW"))
			internal_name.show_hide_warning_button()
			
			paint_job.warnings = []
			if no_vehicles_selected(paint_job):
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				paint_job.warnings.append(PackedStringArray([tr("WARN_VEH_NONES"), tr("WARN_VEH_NONE")]))
				warnings.append(tr("WARN_VEH_NONES"))
			var incompat_vehicles: Array[PackedStringArray] = incompatible_vehicles(paint_job)
			if len(incompat_vehicles) > 0:
				if paint_job not in invalid_paint_jobs:
					invalid_paint_jobs.append(paint_job)
				var incompat_string: PackedStringArray = []
				for pair in incompat_vehicles:
					incompat_string.append(" and ".join(pair))
				paint_job.warnings.append(PackedStringArray([tr("WARN_VEH_INCOM"), "\n".join(incompat_string)]))
				warnings.append(tr("WARN_VEH_INCOM"))
			paint_job.show_hide_warning_button()
	
	var non_unique_names: Array[PackedStringArray] = non_unique_internal_names(paint_jobs)
	if len(non_unique_names) > 0:
		internal_names_valid = false
		var duplicate_names: String = ""
		for names in non_unique_names:
			duplicate_names += " and ".join(names) + "\n"
		duplicate_names = duplicate_names.substr(0, len(duplicate_names) - 1)
		# paint_jobs[0] is the scapegoat here, it really doesn't deserve all this
		paint_jobs[0].get_node("InternalName").warnings.append(PackedStringArray([tr("WARN_INAME_CONFS"), tr("WARN_INAME_CONF") + "\n" + duplicate_names]))
		warnings.append(tr("WARN_INAME_CONFW"))
		if paint_jobs[0] not in invalid_paint_jobs:
			invalid_paint_jobs.append(paint_jobs[0])
		paint_jobs[0].get_node("InternalName").show_hide_warning_button()
	
	if len(warnings) > 0:
		var popup := AcceptDialog.new()
		popup.title = tr("WARNING_TITLE")
		popup.dialog_text = tr("WARN_TEXT") + "\n\n%s\n" % "\n".join(warnings)
		popup.size.y = 0
		popup.ok_button_text = tr("BUTTON_OKAY")
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
