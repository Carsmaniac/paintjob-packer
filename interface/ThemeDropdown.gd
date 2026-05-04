extends OptionButton

@export var simplebox_theme: Theme
@export var pjpdark_theme: Theme


func _ready() -> void:
	connect("item_selected", change_theme)


func change_theme(choice_index) -> void:
	if choice_index == 2:
		get_tree().current_scene.theme = simplebox_theme
	elif choice_index == 0:
		get_tree().current_scene.theme = pjpdark_theme
