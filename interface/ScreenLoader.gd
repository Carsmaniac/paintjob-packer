extends Control
@onready var screens: Array[Node] = [$SetupScreen, $ModInfoScreen, $MainScreen]
var current_screen_index: int = 0
@onready var prev_button: Node = $PrevButton
@onready var next_button: Node = $NextButton
@onready var save_button: Node = $SaveButton

var loaded_game: String


func _ready() -> void:
	switch_screen(true, true)
	$SetupScreen/Panel/VersionText.text = "Version " + ProjectSettings.get_setting("application/config/version")
	$SaveButton.connect("pressed", PJPProject.save)
	$LoadButton.connect("pressed", PJPProject.load)
	$SetupScreen/Panel/CreateButton.connect("pressed", PJPProject.new)
	$SetupScreen/Panel/LoadButton.connect("pressed", PJPProject.load)
	$SetupScreen/Panel/CreateImage.connect("gui_input", maybe_click.bind("new"))
	$SetupScreen/Panel/LoadImage.connect("gui_input", maybe_click.bind("load"))
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
			PJPProject.load()


func switch_game(game: String) -> void:
	# TODO: confirmation dialogue because will lose unsaved information
	if loaded_game != game:
		VehicleDatabase.load_vehicle_lists(game)
		$MainScreen/PaintJobTabContainer.load_tabs()
		loaded_game = game
	if game == "ets":
		$ModInfoScreen/Panel/ETSButton.button_pressed = true
		$ModInfoScreen/Panel/ATSButton.button_pressed = false
	else:
		$ModInfoScreen/Panel/ETSButton.button_pressed = false
		$ModInfoScreen/Panel/ATSButton.button_pressed = true


func switch_screen(next: bool, startup: bool = false) -> void:
	for screen in screens:
		screen.visible = false
	if next:
		current_screen_index += 1
	else:
		current_screen_index -= 1
	if startup:
		current_screen_index = 0 # TODO: Ensure 0
	
	screens[current_screen_index].visible = true
	if current_screen_index == 0:
		prev_button.disabled = true
		next_button.disabled = true
		save_button.disabled = true
	elif current_screen_index == len(screens) - 1:
		prev_button.disabled = false
		next_button.disabled = true
		save_button.disabled = false
	else:
		prev_button.disabled = false
		next_button.disabled = false
		save_button.disabled = false
