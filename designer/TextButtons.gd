extends HBoxContainer

var layer_list: Node


func _ready() -> void:
	get_node("FontSize").connect("value_changed", change_text_size)
	layer_list = get_node("%LayerList")


func change_text_size(text_size: float) -> void:
	for layer in layer_list.selected_layers:
		if layer.layer_type == "text":
			layer.change_text_size(text_size)
