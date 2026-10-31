extends Button

func _ready() -> void:
	pressed.connect(func(): OS.shell_open("https://discord.gg/mmycFkQAnM"))
