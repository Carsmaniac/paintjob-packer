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


func convert_to_scs(colour: Color) -> PackedFloat32Array:
	# From Drive Safely's website
	# Formula help from knox_xss
	var red: float = colour.r
	var green: float = colour.g
	var blue: float = colour.b
	for element in [red, green, blue]:
		if element >= 0.04045:
			element = (element + 0.055) / 1.055
			element = element ** 2.4
		else:
			element = element / 12.92
	return PackedFloat32Array([red, green, blue])


#func show_hide_metallic(dropdown_index) -> void:
	#if dropdown_index == 0:
		#get_node("MetallicControls").visible = false
	#else:
		#get_node("MetallicControls").visible = true


func switch_to_main() -> void:
	get_node("..").switch_from_advanced()
