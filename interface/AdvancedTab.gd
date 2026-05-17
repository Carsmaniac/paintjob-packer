extends Control

var changeables: Array[Node]


func _ready() -> void:
	changeables = [get_node("ChangeableControls/Changeable1"), get_node("ChangeableControls/Changeable2"), get_node("ChangeableControls/Changeable3")]
	get_node("OkayButton").connect("pressed", switch_to_main)
	get_node("ChangeableEnabled").connect("pressed", show_hide_changeables)
	get_node("ChangeableControls/Changeable1/EnableCheckbox").connect("pressed", show_hide_changeables)
	get_node("ChangeableControls/Changeable2/EnableCheckbox").connect("pressed", show_hide_changeables)
	get_node("ChangeableControls/Changeable3/EnableCheckbox").connect("pressed", show_hide_changeables)
	show_hide_changeables()


func show_hide_changeables() -> void:
	get_node("ChangeableControls").visible = get_node("ChangeableEnabled").button_pressed
	for changeable in changeables:
		if changeable.get_node("EnableCheckbox").button_pressed:
			changeable.get_node("Enabled").visible = true
		else:
			changeable.get_node("Enabled").visible = false


func switch_to_main() -> void:
	get_node("..").switch_from_advanced()
