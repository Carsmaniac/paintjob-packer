extends Control
var width: int = 4096
var height: int = 4096

# Toolbar says which tool is active
# ViewCanvas does tool stuff


func resize_canvas(new_size: Vector2i) -> void:
	get_node("SubViewportContainer").size = new_size
	get_node("SubViewportContainer/SubViewport/BackgroundColour").size = new_size
	width = new_size.x
	height = new_size.y
