extends OptionButton

var languages: Array = []
var translations: Array[Array] = [
	["English (US)", "en_US"],
	["English (UK)", "en_GB"],
	["eeeeeeeeee", "ee"],
	["Help us translate!", "automatic"]
]


func _ready() -> void:
	TranslationServer.set_locale("en_GB")
	clear()
	for translation in translations:
		add_item(translation[0])
	connect("item_selected", change_language)


func change_language(index: int) -> void:
	if index < len(translations) - 1:
		TranslationServer.set_locale(translations[index][1])
	else:
		pass # TODO: open browser window to weblate
	for child in get_node("../ModInfoScreen/Panel").get_children():
		if child is VariableInput:
			child.update_localisation()
	for child in get_node("../MainScreen/PaintJobTabContainer").get_children():
		child.find_child("VehicleTabContainer").update_localisation()
		child.update_vehicles_selected_number()
		for grandchild in child.get_children():
			if grandchild is VariableInput:
				grandchild.update_localisation()
	get_node("..").update_localisation()
