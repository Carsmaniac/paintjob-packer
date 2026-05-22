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


func show_help(type: String) -> void:
	var help_text: String
	if type == "base":
		help_text = tr("HELP_BASE")
	elif type == "change":
		help_text = tr("HELP_CHANGE")
	elif type == "1":
		help_text = tr("HELP_CHANGER")
	elif type == "2":
		help_text = tr("HELP_CHANGEG")
	elif type == "3":
		help_text = tr("HELP_CHANGEB")
	var popup := AcceptDialog.new()
	popup.title = tr("WARNING_HELP")
	popup.dialog_text = help_text + "\n"
	popup.max_size[0] = 500
	popup.dialog_autowrap = true
	popup.size.y = 0
	popup.ok_button_text = tr("BUTTON_OKAY")
	popup.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
	self.add_child(popup)
	popup.popup_centered()


func switch_to_main() -> void:
	get_node("..").switch_from_advanced()
