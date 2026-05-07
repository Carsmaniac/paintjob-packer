extends Control


func on_visible() -> void:
	pass

func change_image(dropdown_index: int) -> void:
	var game: String = get_node("..").loaded_game
	get_node("Panel/PlaceholderImageATS").visible = false
	get_node("Panel/PlaceholderImageETS").visible = false
	get_node("Panel/TemplateImageATS").visible = false
	get_node("Panel/TemplateImageETS").visible = false
	if dropdown_index == 0 and game == "ats":
		get_node("Panel/PlaceholderImageATS").visible = true
	elif dropdown_index == 0 and game == "ets":
		get_node("Panel/PlaceholderImageETS").visible = true
	elif dropdown_index == 1 and game == "ats":
		get_node("Panel/TemplateImageATS").visible = true
	elif dropdown_index == 1 and game == "ets":
		get_node("Panel/TemplateImageETS").visible = true
