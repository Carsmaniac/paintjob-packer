extends Panel
@export var linked_node: Node
enum LayerType {RASTER, IMAGE, TEXT, SHAPE}
var layer_type: LayerType
var layer_name: String = "A LONG THING"


func _ready() -> void:
	get_node("ButtonUp").connect("pressed", reorder.bind(false))
	get_node("ButtonDown").connect("pressed", reorder.bind(true))
	get_node("Label").text = self.layer_name
	update_buttons()
	self.connect("gui_input", possibly_select_layer)


func possibly_select_layer(event) -> void:
	if event is InputEventMouseButton and event.button_index == 1 and event.pressed:
		get_parent().select_layer(get_index())


func show_hide() -> void:
	if get_node("ButtonHide").button_pressed:
		pass
	else:
		pass


func reorder(move_down: bool) -> void:
	if move_down:
		get_parent().move_child(get_parent().get_child(get_index()), get_index() + 1)
	else:
		get_parent().move_child(get_parent().get_child(get_index()), get_index() - 1)
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
	get_parent().remove_layer(get_index())
