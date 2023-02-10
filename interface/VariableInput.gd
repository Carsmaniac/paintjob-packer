extends Node2D

export var input_name: String
export(String, "Text", "Dropdown", "Checkbox") var input_type

# Called when the node enters the scene tree for the first time.
func _ready():
	$Label.text = input_name
	$WarningButton.visible = false
	$TextInput.visible = false
	$DropdownInput.visible = false
	$CheckboxInput.visible = false
	
	if input_type == "Text":
		$TextInput.visible = true
	elif input_type == "Dropdown":
		$DropdownInput.visible = true
	elif input_type == "Checkbox":
		$CheckboxInput.visible = true


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
