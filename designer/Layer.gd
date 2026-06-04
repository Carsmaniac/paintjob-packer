extends Panel

@export var linked_node: Node
@export var layer_name: String = "Layer"
var custom_layer_name: bool = false
@export_enum("raster", "text", "image", "rect", "ellipse") var layer_type: String

var text_size: float
var layer_colour: Color


func _ready() -> void:
	get_node("ButtonUp").connect("pressed", reorder.bind(false))
	get_node("ButtonDown").connect("pressed", reorder.bind(true))
	get_node("ButtonHide").connect("pressed", show_hide)
	get_node("Label").text = self.layer_name
	update_buttons()
	self.connect("gui_input", maybe_select_layer)
	
	get_node("RenameWindow/Button").connect("pressed", rename_layer)
	get_node("RenameWindow/LineEdit").connect("text_submitted", rename_layer)
	get_node("RenameWindow").connect("close_requested", cancel_rename)
	
	get_node("ChangeTextWindow/Button").connect("pressed", confirm_change_text)
	# TODO: Ctrl-Enter confirms text entry, esc cancels it
	# get_node("ChangeTextWindow/LineEdit").connect("text_submitted", confirm_change_text)


func maybe_select_layer(event) -> void:
	# Rename on double click
	if event is InputEventMouseButton and event.button_index == 1 and event.double_click:
		get_node("RenameWindow").popup_centered()
		get_node("RenameWindow/LineEdit").grab_focus()
		get_node("RenameWindow/LineEdit").text = layer_name
		get_node("RenameWindow/LineEdit").set_caret_column(len(get_node("RenameWindow/LineEdit").text))
	
	# Select on click
	elif event is InputEventMouseButton and event.button_index == 1 and event.pressed:
		get_parent().select_layer(get_index())


func rename_layer(new_name: String = "") -> void:
	if new_name == "":
		new_name = get_node("RenameWindow/LineEdit").text
	layer_name = new_name.replace("\n", "")
	custom_layer_name = true
	get_node("Label").text = new_name.replace("\n", "")
	get_node("RenameWindow").visible = false


func cancel_rename() -> void:
	get_node("RenameWindow").visible = false


func change_text_layer() -> void:
	get_node("ChangeTextWindow").popup_centered()
	get_node("ChangeTextWindow/LineEdit").grab_focus()
	get_node("ChangeTextWindow/LineEdit").text = linked_node.text
	get_node("ChangeTextWindow/LineEdit").set_caret_column(len(get_node("ChangeTextWindow/LineEdit").text))


func confirm_change_text(_new_name: String = "") -> void:
	linked_node.text = get_node("ChangeTextWindow/LineEdit").text
	if not custom_layer_name:
		rename_layer(linked_node.text)
	get_node("ChangeTextWindow").visible = false
	get_parent().select_layer(get_index())


func change_colour(new_colour: Color) -> void:
	layer_colour = new_colour
	if layer_type == "rect":
		var new_style: StyleBoxFlat = linked_node.theme.get_stylebox("panel", "Panel")
		new_style.bg_color = new_colour
		linked_node.theme.set_stylebox("panel", "Panel", new_style)
	elif layer_type == "ellipse":
		linked_node.modulate = new_colour
	elif layer_type == "text":
		linked_node.add_theme_color_override("font_color", new_colour)


func show_hide() -> void:
	if get_node("ButtonHide").button_pressed:
		linked_node.visible = false
	else:
		linked_node.visible = true


func reorder(move_down: bool) -> void:
	if move_down:
		get_parent().move_child(get_parent().get_child(get_index()), get_index() + 1)
		linked_node.get_parent().move_child(linked_node, linked_node.get_index() - 1)
	else:
		get_parent().move_child(get_parent().get_child(get_index()), get_index() - 1)
		linked_node.get_parent().move_child(linked_node, linked_node.get_index() + 1)
	get_parent().update_buttons()


func update_buttons() -> void:
	if get_index() == 0:
		get_node("ButtonUp").disabled = true
	else:
		get_node("ButtonUp").disabled = false
	if get_index() == get_parent().get_child_count() - 1:
		get_node("ButtonDown").disabled = true
	else:
		get_node("ButtonDown").disabled = false
	if get_parent().get_child_count() == 1:
		get_node("ButtonDelete").disabled = true
	else:
		get_node("ButtonDelete").disabled = false


func delete() -> void:
	linked_node.queue_free()
	if self in get_parent().selected_layers:
		get_parent().remove_selection(self)
	get_parent().remove_layer(get_index())
