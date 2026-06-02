extends HBoxContainer

var layer_list: Node


func _ready() -> void:
	get_node("FontSize").connect("value_changed", change_text_size)
	layer_list = get_node("../../../../RightPanel/ScrollContainer/LayerList")


func change_text_size(text_size: float) -> void:
	for layer in layer_list.selected_layers:
		if layer.layer_type == "text":
			layer.linked_node.remove_theme_font_size_override("font_size")
			layer.text_size = text_size
			layer.linked_node.add_theme_font_size_override("font_size", text_size)
