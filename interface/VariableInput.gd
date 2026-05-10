extends Control
class_name VariableInput

@export var input_name: String
@export_multiline var help_text: String
@export_enum("paint_job_name", "price", "internal_name", "cabin_support", 
		"split_cabins", "unlock_level", "mod_name", "author_name", "version", "description") var input_type: String

var warnings: Array = []


func _ready() -> void:
	$Label.text = input_name
	$WarningButton.visible = false
	$TextInput.visible = false
	$DropdownInput.visible = false
	$CheckboxInput.visible = false
	$TextBox.visible = false
	$NumberInput.visible = false
	
	$WarningButton.connect("pressed", show_warnings)
	#$HelpButton.tooltip_text = help_text
	$HelpButton.connect("pressed", show_help)
	
	if input_type in ["paint_job_name", "internal_name", "mod_name", "author_name", "version"]:
		$TextInput.visible = true
		if input_type == "version":
			$TextInput.size[0] = 150
	elif input_type == "price":
			$NumberInput.visible = true
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
		$NumberInput.position = Vector2(0, 80)
	elif input_type == "description":
		$TextBox.visible = true


func show_hide_warning_button() -> void:
	if len(warnings) > 0:
		$WarningButton.visible = true
	else:
		$WarningButton.visible = false


func show_warnings() -> void:
	var popup := AcceptDialog.new()
	popup.title = "Warning"
	var dialogue_text = ""
	for warning in warnings:
		dialogue_text += "%s\n%s\n\n" % [warning[0], warning[1]]
	dialogue_text = dialogue_text.substr(0, len(dialogue_text) - 1)
	popup.dialog_text = dialogue_text
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
