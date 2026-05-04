extends Control
@onready var screens = [$SetupScreen, $MainScreen]
var current_screen_index = 0
@onready var prev_button = $PrevButton
@onready var next_button = $NextButton


func _ready() -> void:
	_switch_screen(true, true)
	$SetupScreen/PictureATS.connect("gui_input", thing.bind("ats"))
	$SetupScreen/PictureETS.connect("gui_input", thing.bind("ets"))
	$SetupScreen/VersionText.text = "Version " + ProjectSettings.get_setting("application/config/version")


func thing(input_event: InputEvent, game):
	if input_event is InputEventMouseButton and input_event.button_index == 1 and input_event.pressed:
		VehicleDatabase.load_vehicle_lists(game)
		$MainScreen/PaintJobTabContainer._load_tabs()
		_switch_screen(true)


func _switch_screen(next: bool, startup: bool = false, ) -> void:
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
	elif current_screen_index == len(screens) - 1:
		prev_button.disabled = false
		next_button.disabled = true
	else:
		prev_button.disabled = false
		next_button.disabled = false
		
