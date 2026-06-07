extends HSplitContainer

var left_panel: Node
var right_panel: Node
@export var right_panel_max_width: float


func _ready() -> void:
	connect("resized", limit_right_panel_size)
	left_panel = get_child(0)
	right_panel = get_child(0)


func limit_right_panel_size() -> void:
	left_panel.custom_minimum_size.x = self.size.x - right_panel_max_width
