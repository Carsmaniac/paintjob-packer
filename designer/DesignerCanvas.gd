extends Sprite2D


func resize_canvas(new_size: Vector2i) -> void:
	get_node("SubViewportContainer").size = new_size
	get_node("SubViewportContainer/SubViewport/BackgroundColour").size = new_size
