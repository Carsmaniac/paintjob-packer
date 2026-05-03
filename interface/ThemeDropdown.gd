extends OptionButton

@export var simplebox_theme: Theme
@export var pjpdark_theme: Theme


func _ready() -> void:
	connect("item_selected", change_theme)


func change_theme(choice_index) -> void:
	if choice_index == 0:
		get_parent().theme = simplebox_theme
	elif choice_index == 1:
		get_parent().theme = pjpdark_theme
