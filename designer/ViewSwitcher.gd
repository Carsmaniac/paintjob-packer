extends OptionButton

var view_canvas: Node
var view_model: Node
var two_up: Node


func _ready() -> void:
	connect("item_selected", switch_view_side)
	view_canvas = get_node("../..").find_child("ViewCanvas")
	view_model = get_node("../..").find_child("ViewModel")
	two_up = get_node("../../TwoUp")


func switch_view_side(option: int) -> void:
	two_up.move_child(view_model, option)
