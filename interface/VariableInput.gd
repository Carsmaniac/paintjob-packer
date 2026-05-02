extends Control

@export var input_name: String
@export_multiline var help_text: String
@export_enum("text_string", "text_number", "text_alphanumeric", "dropdown_cabin", "dropdown_split", "checkbox") var input_type: String

var warning: String


func _ready() -> void:
	$Label.text = input_name
	$WarningButton.visible = false
	$TextInput.visible = false
	$DropdownInput.visible = false
	$CheckboxInput.visible = false
	
	$WarningButton.connect("pressed", show_warnings)
	$HelpButton.connect("pressed", show_help)
	
	if "text" in input_type:
		$TextInput.visible = true
		if input_type == "text_number":
			$TextInput.size[0] = 100
		$TextInput.connect("text_changed", validate_text_input)
	elif "dropdown" in input_type:
		$DropdownInput.visible = true
		if input_type == "dropdown_cabin":
			$DropdownInput.add_item("Largest cabin only")
			$DropdownInput.add_item("All cabins")
			$DropdownInput.add_item("Selected cabins")
		else:
			$DropdownInput.add_item("Don't split, one per truck")
			$DropdownInput.add_item("Split, one per cabin")
	elif input_type == "checkbox":
		$CheckboxInput.visible = true
		$TextInput.visible = true
		$TextInput.position = Vector2(0, 70)
		$HelpButton.position = Vector2(321, 69)
		$WarningButton.position = Vector2(321, 36)
		

func validate_text_input(__) -> void:
	var string: String = $TextInput.text
	if input_type == "text_number":
		if string != "" and not string.is_valid_int():
			warning = "Must be a number with no decimal point or other characters."
			$WarningButton.visible = true
		else:
			$WarningButton.visible = false
			
	elif input_type == "text_alphanumeric":
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
	var popup: Node = get_parent().get_parent().get_parent().get_node("AcceptDialogue")
	popup.title = "Warning"
	popup.dialog_text = warning
	popup.size.y = 0
	popup.ok_button_text = "Okay"
	popup.popup_centered()
	
func show_help() -> void:
	var popup: Node = get_parent().get_parent().get_parent().get_node("AcceptDialogue")
	popup.title = "Help"
	popup.dialog_text = help_text
	# TODO: Set help_text for price based on game selected
	popup.size.y = 0
	popup.ok_button_text = "Okay"
	popup.popup_centered()
	
