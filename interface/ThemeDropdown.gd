extends OptionButton

@export var simplebox_theme: Theme
@export var pjpdark_theme: Theme
@export var pjplight_theme: Theme


func _ready() -> void:
	connect("item_selected", change_theme)


func change_theme(choice_index) -> void:
	if choice_index == 0:
		get_tree().current_scene.theme = pjpdark_theme
		get_tree().current_scene.find_child("BackgroundColour").color = Color.hex(0x4c4c4cff)
	elif choice_index == 1:
		get_tree().current_scene.theme = pjplight_theme
		get_tree().current_scene.find_child("BackgroundColour").color = Color.hex(0xffffffff)
	elif choice_index == 2:
		get_tree().current_scene.theme = simplebox_theme
		get_tree().current_scene.find_child("BackgroundColour").color = Color.hex(0x4c4c4cff)
