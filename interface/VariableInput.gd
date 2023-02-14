extends Node2D

export var input_name: String
export(String, "Text", "Dropdown", "CheckboxAndText") var input_type

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	$Label.text = input_name
	$WarningButton.visible = false
	$TextInput.visible = false
	$DropdownInput.visible = false
	$CheckboxInput.visible = false
	
	if input_type == "Text":
		$TextInput.visible = true
	elif input_type == "Dropdown":
		$DropdownInput.visible = true
	elif input_type == "CheckboxAndText":
		$CheckboxInput.visible = true
		$TextInput.visible = true
		$TextInput.rect_position = Vector2(0, 70)
		$HelpButton.rect_position = Vector2(321, 69)
		$WarningButton.rect_position = Vector2(321, 36)


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
