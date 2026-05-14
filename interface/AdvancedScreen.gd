extends Control

var changeables: Array[Node]


func _ready() -> void:
	#changeables = [get_node("ChangeableControls/Changeable1")]
	changeables = [get_node("Panel/ChangeableControls/Changeable1"), get_node("Panel/ChangeableControls/Changeable2"), get_node("Panel/ChangeableControls/Changeable3")]
	get_node("Panel/ChangeableDropdown").connect("item_selected", show_hide_changeables)
	get_node("Panel/MetallicDropdown").connect("item_selected", show_hide_metallic)
	get_node("Panel/OkayButton").connect("pressed", switch_to_main)
	show_hide_changeables(0)
	show_hide_metallic(0)

func show_hide_changeables(dropdown_index: int) -> void:
	for changeable in changeables:
		changeable.visible = false
	for i in range(dropdown_index):
		changeables[i].visible = true

func show_hide_metallic(dropdown_index) -> void:
	if dropdown_index == 0:
		get_node("Panel/MetallicControls").visible = false
	else:
		get_node("Panel/MetallicControls").visible = true


func switch_to_main() -> void:
	get_node("..").switch_screen(true, false, 2)
