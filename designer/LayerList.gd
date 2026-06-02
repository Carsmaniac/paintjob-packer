extends VBoxContainer

const Layer := preload("res://designer/Layer.tscn")
var selected_layers: Array[Node]

var layer_theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDarkLayer.tres")
var layer_selected_theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDarkLayerSelected.tres")

var layer_nodes: Node


func _ready() -> void:
	get_node("../../ButtonNewLayer").connect("pressed", create_layer)
	layer_nodes = get_node("../../../TwoUp/ViewCanvas/SubViewport/DesignerCanvas/SubViewportContainer/SubViewport/LayerNodes")
	#for i in range(5):
		#add_layer()


func remove_layer(index: int) -> void:
	remove_child(get_child(index))
	update_buttons()


func update_buttons() -> void:
	for child in get_children():
		child.update_buttons()


func create_layer() -> Node:
	var new_layer: Node = Layer.instantiate()
	var name_list: Array
	for child in get_children():
		name_list.append(child.layer_name)
	for i in range(5000):
		if "Layer " + str(i) not in name_list:
			new_layer.layer_name = "Layer " + str(i)
			break
	return new_layer


func add_text_layer(new_position: Vector2) -> void:
	var new_layer: Node = create_layer()
	new_layer.layer_type = "text"
	new_layer.layer_name = "Text"
	var layer_node = Label.new()
	layer_node.text = "Text"
	layer_node.position = new_position
	layer_node.add_theme_color_override("font_color", Color.BLACK)
	var text_size = get_node("../../../TopPanel/HBoxContainer/ToolButtons/TextButtons/FontSize").value
	layer_node.add_theme_font_size_override("font_size", text_size)
	new_layer.text_size = text_size
	layer_nodes.add_child(layer_node)
	new_layer.linked_node = layer_node
	add_child(new_layer)
	move_child(new_layer, 0)
	update_buttons()
	new_layer.change_text_layer()


func select_layer(index: int) -> void:
	selected_layers = [get_child(index)]
	update_selected_themes()
	get_node("../../../TwoUp/ViewCanvas").sync_tool_to_layer()


func update_selected_themes() -> void:
	for layer in get_children():
		if layer in selected_layers:
			layer.theme = layer_selected_theme
		else:
			layer.theme = layer_theme
