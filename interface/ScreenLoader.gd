extends Control
@onready var screens: Array[Node] = [$SetupScreen, $ModInfoScreen, $MainScreen, $ExportScreen]
var current_screen_index: int = 0
@onready var prev_button: Node = $PrevButton
@onready var next_button: Node = $NextButton
@onready var save_button: Node = $SaveButton

var loaded_game: String


func _ready() -> void:
	switch_screen(true, true)
	$SetupScreen/Panel/VersionText.text = tr("SETUP_VERSION") % ProjectSettings.get_setting("application/config/version")
	$SaveButton.connect("pressed", PJPProject.save_inform)
	$SetupScreen/Panel/CreateButton.connect("pressed", PJPProject.new)
	$SetupScreen/Panel/LoadButton.connect("pressed", PJPProject.load_dialogue)
	$SetupScreen/Panel/AboutButton.connect("pressed", switch_screen.bind(false))
	$SetupScreen/Panel/CreateImage.connect("gui_input", maybe_click.bind("new"))
	$SetupScreen/Panel/LoadImage.connect("gui_input", maybe_click.bind("load"))
	$AboutScreen/OkayButton.connect("pressed", switch_screen.bind(true))
	$ModInfoScreen/Panel/ATSButton.connect("pressed", switch_game.bind("ats"))
	$ModInfoScreen/Panel/ETSButton.connect("pressed", switch_game.bind("ets"))
	$ModInfoScreen/Panel/ATSImage.connect("gui_input", maybe_click.bind("ats"))
	$ModInfoScreen/Panel/ETSImage.connect("gui_input", maybe_click.bind("ets"))


func maybe_click(input_event: InputEvent, button: String):
	if input_event is InputEventMouseButton and input_event.button_index == 1 and input_event.pressed:
		if button in ["ats", "ets"]:
			switch_game(button)
		elif button == "new":
			PJPProject.new()
		elif button == "load":
			PJPProject.load_dialogue()


func switch_game(game: String) -> void:
	if loaded_game != game:
		VehicleDatabase.load_vehicle_lists(game)
		$MainScreen/PaintJobTabContainer.load_tabs()
		loaded_game = game
	$ExportScreen.change_image($ExportScreen/Panel/PlaceholderDropdown.selected)
	if game == "ets":
		$ModInfoScreen/Panel/ETSButton.button_pressed = true
		$ModInfoScreen/Panel/ATSButton.button_pressed = false
		if not next_button.is_connected("pressed", switch_screen.bind("true")):
			next_button.connect("pressed", switch_screen.bind(true))
		save_button.disabled = false
		next_button.disabled = false
	elif game == "ats":
		$ModInfoScreen/Panel/ETSButton.button_pressed = false
		$ModInfoScreen/Panel/ATSButton.button_pressed = true
		if not next_button.is_connected("pressed", switch_screen.bind("true")):
			next_button.connect("pressed", switch_screen.bind(true))
		save_button.disabled = false
		next_button.disabled = false
	elif game == "none":
		$ModInfoScreen/Panel/ETSButton.button_pressed = false
		$ModInfoScreen/Panel/ATSButton.button_pressed = false
		next_button.disconnect("pressed", switch_screen.bind(true))
		next_button.disabled = true


func switch_screen(next: bool, startup: bool = false) -> void:
	for screen in screens:
		screen.visible = false
		$AboutScreen.visible = false
	if next:
		current_screen_index += 1
	else:
		current_screen_index -= 1
	if startup:
		current_screen_index = 0
	
	if current_screen_index == -1:
		$AboutScreen.visible = true
	else:
		screens[current_screen_index].visible = true
	if current_screen_index == -1:
		prev_button.visible = false
		next_button.visible = false
		$LoadButton.disabled = true
	elif current_screen_index == 0:
		prev_button.disabled = true
		prev_button.visible = true
		next_button.disabled = true
		next_button.visible = true
		next_button.text = tr("BUTTON_NEXT")
		save_button.disabled = true
		$LoadButton.disabled = false
		if not $LoadButton.is_connected("pressed", PJPProject.confirm_load):
			$LoadButton.connect("pressed", PJPProject.confirm_load)
	elif current_screen_index == 1:
		prev_button.disabled = false
		if prev_button.is_connected("pressed", switch_screen.bind(false)):
			prev_button.disconnect("pressed", switch_screen.bind(false))
		if not prev_button.is_connected("pressed", PJPProject.confirm_return):
			prev_button.connect("pressed", PJPProject.confirm_return)
		next_button.disabled = true
		next_button.text = tr("BUTTON_NEXT")
		if not next_button.is_connected("pressed", switch_screen.bind(true)):
			next_button.connect("pressed", switch_screen.bind(true))
		if next_button.is_connected("pressed", Validation.validate_all_inputs):
			next_button.disconnect("pressed", Validation.validate_all_inputs)
		if loaded_game != "none":
			next_button.disabled = false
			save_button.disabled = false
	elif current_screen_index == 2:
		prev_button.disabled = false
		if prev_button.is_connected("pressed", PJPProject.confirm_return):
			prev_button.disconnect("pressed", PJPProject.confirm_return)
		if not prev_button.is_connected("pressed", switch_screen.bind(false)):
			prev_button.connect("pressed", switch_screen.bind(false))
		next_button.disabled = false
		next_button.visible = true
		next_button.text = tr("BUTTON_EXPORT")
		if next_button.is_connected("pressed", switch_screen.bind(true)):
			next_button.disconnect("pressed", switch_screen.bind(true))
		if not next_button.is_connected("pressed", Validation.validate_all_inputs):
			next_button.connect("pressed", Validation.validate_all_inputs)
		save_button.disabled = false
	elif current_screen_index == 3:
		next_button.visible = false
		get_node("ExportScreen").try_desktop_folder()

func update_localisation() -> void:
	next_button.text = tr("BUTTON_NEXT")
	if current_screen_index == 2:
		next_button.text = tr("BUTTON_EXPORT")
	$SetupScreen/Panel/VersionText.text = tr("SETUP_VERSION") % ProjectSettings.get_setting("application/config/version")
