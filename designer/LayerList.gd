extends VBoxContainer
const Layer := preload("res://designer/Layer.tscn")
var selected_layers: Array[Node]
var layer_theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDarkLayer.tres")
var layer_selected_theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDarkLayerSelected.tres")


func _ready() -> void:
	get_node("../../ButtonNewLayer").connect("pressed", add_layer)
	#for i in range(5):
		#add_layer()


func remove_layer(index: int) -> void:
	remove_child(get_child(index))
	update_buttons()


func update_buttons() -> void:
	for child in get_children():
		child.update_buttons()


func add_layer() -> void:
	var new_layer: Node = Layer.instantiate()
	var name_list: Array
	for child in get_children():
		name_list.append(child.layer_name)
	for i in range(5000):
		if "Layer " + str(i) not in name_list:
			new_layer.layer_name = "Layer " + str(i)
			break
	add_child(new_layer)
	update_buttons()


func select_layer(index: int) -> void:
	selected_layers = [get_child(index)]
	update_selected_themes()


func update_selected_themes() -> void:
	for layer in get_children():
		if layer in selected_layers:
			layer.theme = layer_selected_theme
		else:
			layer.theme = layer_theme
