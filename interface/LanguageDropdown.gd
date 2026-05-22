extends OptionButton

var languages: Array = []
var translations: Array[Array] = [
	["English (UK)", "en_GB"],
	["English (US)", "en_US"],
	["Help us translate!", "automatic"]
]


func _ready() -> void:
	var target_locale: String = TranslationServer.get_locale()
	var locale_found: bool = false
	
	TranslationServer.set_locale("en_GB")
	clear()
	for translation in translations:
		add_item(translation[0])
	connect("item_selected", change_language)
	
	for i in range(len(translations)):
		if translations[i][1] == target_locale or (translations[i][1] == "en_GB" and target_locale in ["en_AU", "en_NZ", "en_IE", "en_ZA", "en_CA"]):
			locale_found = true
			TranslationServer.set_locale(translations[i][1])
			self.selected = i
	if not locale_found:
		for i in range(len(translations)):
			if translations[i][1].substr(0, 2) == target_locale.substr(0, 2):
				locale_found = true
				TranslationServer.set_locale(translations[i][1])
				self.selected = i


func change_language(index: int) -> void:
	if index < len(translations) - 1:
		TranslationServer.set_locale(translations[index][1])
	else:
		OS.shell_open(get_node("../AboutScreen").weblate_link)
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
	get_node("../ExportScreen").update_localisation()
