extends OptionButton

var pjp_dark_theme: Theme
var pjp_light_theme: Theme

var pjp_dark_warning_theme: Theme
var pjp_light_warning_theme: Theme
var warning_theme_displayed: bool = false

var dark_themes: Array[Theme]
var light_themes: Array[Theme]

var current_theme: Theme


func _ready() -> void:
	connect("item_selected", change_theme)
	current_theme = get_tree().current_scene.theme
	pjp_dark_theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
	pjp_light_theme = ResourceLoader.load("res://simple-box-theme/pjp-light/PJPLight.tres")
	
	pjp_dark_warning_theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDarkWarning.tres")
	pjp_light_warning_theme = ResourceLoader.load("res://simple-box-theme/pjp-light/PJPLightWarning.tres")
	
	dark_themes = [pjp_dark_theme]
	light_themes = [pjp_light_theme]
	
	if DisplayServer.is_dark_mode():
		change_theme(0)
		self.selected = 0
	else:
		change_theme(1)
		self.selected = 1


func change_theme(choice_index) -> void:
	if choice_index == 0:
		get_tree().current_scene.theme = pjp_dark_theme
		current_theme = pjp_dark_theme
		get_tree().current_scene.find_child("BackgroundColour").color = Color.hex(0x4c4c4cff)
		for child in get_node("../MainScreen/PaintJobTabContainer").get_children():
			child.get_node("SearchIconLight").visible = false
			if child.get_node("Name").visible:
				child.get_node("SearchIconDark").visible = true
	elif choice_index == 1:
		get_tree().current_scene.theme = pjp_light_theme
		current_theme = pjp_light_theme
		get_tree().current_scene.find_child("BackgroundColour").color = Color.hex(0xffffffff)
		for child in get_node("../MainScreen/PaintJobTabContainer").get_children():
			child.get_node("SearchIconDark").visible = false
			if child.get_node("Name").visible:
				child.get_node("SearchIconLight").visible = true
	get_node("../ThemeTimer").start()
	switch_warning_theme()


func switch_warning_theme() -> void:
	if warning_theme_displayed:
		set_warning_theme(current_theme)
	else:
		if current_theme in dark_themes:
			set_warning_theme(pjp_dark_warning_theme)
		else:
			set_warning_theme(pjp_light_warning_theme)
	warning_theme_displayed = not warning_theme_displayed


func set_warning_theme(new_theme: Theme) -> void:
	for child in get_node("../ModInfoScreen/Panel").get_children():
		if child is VariableInput:
			child.find_child("WarningButton").theme = new_theme
	for child in get_node("../MainScreen/PaintJobTabContainer").get_children():
		for warning_button in child.find_children("WarningButton"):
			warning_button.theme = new_theme
	get_node("../SetupScreen/Panel/UpdateChecker/UpdateButton").theme = new_theme
