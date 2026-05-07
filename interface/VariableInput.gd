extends Control
class_name VariableInput

@export var input_name: String
@export_multiline var help_text: String
@export_enum("paint_job_name", "price", "internal_name", "cabin_support", 
		"split_cabins", "unlock_level", "mod_name", "author_name", "version", "description") var input_type: String

var warning: String


func _ready() -> void:
	$Label.text = input_name
	$WarningButton.visible = false
	$TextInput.visible = false
	$DropdownInput.visible = false
	$CheckboxInput.visible = false
	$TextBox.visible = false
	
	$WarningButton.connect("pressed", show_warnings)
	#$HelpButton.tooltip_text = help_text
	$HelpButton.connect("pressed", show_help)
	
	if input_type in ["paint_job_name", "internal_name", "price", "mod_name", "author_name", "version"]:
		$TextInput.visible = true
		if input_type in ["price", "version"]:
			$TextInput.size[0] = 100
	elif input_type in ["cabin_support", "split_cabins"]:
		$DropdownInput.visible = true
		if input_type == "cabin_support":
			$DropdownInput.add_item("Largest cabin only")
			$DropdownInput.add_item("All cabins")
			$DropdownInput.add_item("Selected cabins")
		else:
			$DropdownInput.add_item("Don't split, one per truck")
			$DropdownInput.add_item("Split, one per cabin")
	elif input_type == "unlock_level":
		$CheckboxInput.visible = true
		$CheckboxInput.button_pressed = true
		$TextInput.visible = false
		$TextInput.position = Vector2(0, 80)
		$TextInput.size[0] = 100
		$TextInput.connect("text_changed", validate_text_input)
	elif input_type == "description":
		$TextBox.visible = true
		

func validate_text_input(__) -> void:
	# TODO: replace this function with validation system
	var string: String = $TextInput.text
	if input_type in ["price", "unlock_level"]:
		if string != "" and not string.is_valid_int():
			warning = "Must be a number with no decimal point or other characters."
			$WarningButton.visible = true
		else:
			$WarningButton.visible = false
			
	elif input_type == "internal_name":
		var not_alphanumeric: bool = false
		for letter in string:
			if letter not in "abcdefghijklmnopqrstuvwxyz0123456789_":
				not_alphanumeric = true
		var max_length: int = 12
		if get_node("../SplitPaintJobs/DropdownInput").selected == 1:
			max_length = 10
		
		if string != "":
			if not_alphanumeric:
				warning = "Must consist of only lowercase letters, numbers and underscores.\n\nPermitted characters:\nabcdefghijklmnopqrstuvwxyz0123456789_"
				$WarningButton.visible = true
			elif len(string) > max_length:
				warning = "Must be %s characters or fewer." % max_length
				$WarningButton.visible = true
			# TODO: detect non-unique internal names
			# elif not_unique:
			#     warning = "Must be unique, cannot be the same as the internal name of any other paint job."
			#     $WarningButton.visible = true
			else:
				$WarningButton.visible = false
		else:
			$WarningButton.visible = false

	
func show_warnings() -> void:
	var popup := AcceptDialog.new()
	popup.title = "Warning"
	popup.dialog_text = warning
	popup.size.y = 0
	popup.ok_button_text = "Okay"
	popup.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
	self.add_child(popup)
	popup.popup_centered()


func show_help() -> void:
	var popup := AcceptDialog.new()
	popup.title = "Help"
	popup.dialog_text = help_text + "\n"
	# TODO: Set help_text for price based on game selected
	popup.size.y = 0
	popup.ok_button_text = "Okay"
	popup.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
	self.add_child(popup)
	popup.popup_centered()
