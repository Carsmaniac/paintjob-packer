extends OptionButton


func _ready() -> void:
	connect("item_selected", switch_view_side)


func switch_view_side(option: int) -> void:
	get_node("../TwoUp").move_child(get_node("../TwoUp/ViewModel"), option)
