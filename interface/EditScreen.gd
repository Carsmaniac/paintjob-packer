extends Control
var veh_tree: Tree
var vehicle_list: Array = []

const EditVehicleCabin := preload("res://interface/EditVehicleCabin.tscn")
const EditVehicleAccessory := preload("res://interface/EditVehicleAccessory.tscn")


func _ready() -> void:
	veh_tree = get_node("%VehicleSelectionTree")
	VehicleDatabase.load_vehicle_lists("ets")
	vehicle_list = VehicleDatabase.universal_vehicle_list
	vehicle_list.sort_custom(func(a, b): return a["game"]+a["author"]+a["path"] < b["game"]+b["author"]+b["path"])
	load_vehicle_tree()
	get_node("Panel/LoadButton").pressed.connect(load_vehicle_file)
	get_node("Panel/SaveButton").pressed.connect(save_vehicle_file)
	get_node("Panel/FinishedButton").pressed.connect(return_to_main)
	get_node("%Cabins/HBoxContainer/Button").pressed.connect(func(): get_node("%Cabins/VBoxContainer").add_child(EditVehicleCabin.instantiate()))
	get_node("%EditAccessories/HBoxContainer/Button").pressed.connect(func(): get_node("%EditAccessories/VBoxContainer").add_child(EditVehicleAccessory.instantiate()))


func show_edit_screen() -> void:
	get_parent().switch_screen(true, false, 5)


func return_to_main() -> void:
	get_parent().switch_screen(true, false, 2)


func alphanumericise(in_str: String) -> String:
	var out_str = ""
	for character in in_str:
		if character.to_lower() in "abcdefghijklmnopqrstuvwxyz1234567890":
			out_str += character
	return out_str


func load_vehicle_tree() -> void:
	veh_tree.clear()
	var root = veh_tree.create_item()
	veh_tree.hide_root = true
	
	for dict in vehicle_list:
		var game_exists: bool = false
		var game_item: TreeItem
		for game in root.get_children():
			if game.get_text(0) == dict["game"]:
				game_exists = true
				game_item = game
		if not game_exists:
			game_item = veh_tree.create_item(root)
			game_item.set_text(0, dict["game"])
		
		var author_exists: bool = false
		var author_item: TreeItem
		for author in game_item.get_children():
			if author.get_text(0) == dict["author"]:
				author_exists = true
				author_item = author
		if not author_exists:
			author_item = veh_tree.create_item(game_item)
			author_item.set_text(0, dict["author"])
		
		var vehicle_item = veh_tree.create_item(author_item)
		vehicle_item.set_text(0, dict["path"])
		
		game_item.collapsed = true
		author_item.collapsed = true


func get_vehicle_dictionary(path: String) -> Dictionary:
	for vehicle in vehicle_list:
		if vehicle["game"]+vehicle["author"]+vehicle["path"] == path:
			return vehicle
	return {}


func load_vehicle_file() -> void:
	var selected_item: TreeItem = veh_tree.get_selected()
	if selected_item != null:
		if selected_item.get_parent() != null:
			if selected_item.get_parent().get_parent() != null:
				if selected_item.get_parent().get_parent().get_parent() != null:
					var vehicle_dictionary = get_vehicle_dictionary(
						selected_item.get_parent().get_parent().get_text(0)+selected_item.get_parent().get_text(0)+selected_item.get_text(0))
					
					if vehicle_dictionary["game"] == "ets":
						get_node("%EditGame/OptionButton").selected = 0
					else:
						get_node("%EditGame/OptionButton").selected = 1
					get_node("%EditAuthorASCII/LineEdit").text = selected_item.get_parent().get_text(0)
					get_node("%EditVehiclePath/LineEdit").text = vehicle_dictionary["path"]
					get_node("%EditVehicleName/LineEdit").text = vehicle_dictionary["name"]
					if vehicle_dictionary["type"] == "truck":
						get_node("%EditType/OptionButton").selected = 0
					elif vehicle_dictionary["type"] == "trailer":
						get_node("%EditType/OptionButton").selected = 1
					elif vehicle_dictionary["type"] == "bus":
						get_node("%EditType/OptionButton").selected = 2
					elif vehicle_dictionary["type"] == "car":
						get_node("%EditType/OptionButton").selected = 3
					get_node("%EditMod/CheckBox").button_pressed = vehicle_dictionary["mod"]
					get_node("%EditModAuthor/LineEdit").text = vehicle_dictionary["mod_author"]
					get_node("%EditLinkWorkshop/LineEdit").text = vehicle_dictionary["mod_links"]["workshop"]
					get_node("%EditLinkForums/LineEdit").text = vehicle_dictionary["mod_links"]["forums"]
					get_node("%EditLinkTrucky/LineEdit").text = vehicle_dictionary["mod_links"]["trucky"]
					get_node("%EditLinkAuthor/LineEdit").text = vehicle_dictionary["mod_links"]["author"]
					get_node("%EditColourPicker/CheckBox").button_pressed = vehicle_dictionary["colour_picker"]
					get_node("%EditAltUV/CheckBox").button_pressed = vehicle_dictionary["alt_uv"]
					get_node("%EditSeparatePaintJobs/CheckBox").button_pressed = vehicle_dictionary["separate_paint_jobs"]
					for child: Node in get_node("%Cabins/VBoxContainer").get_children():
						get_node("%Cabins/VBoxContainer").remove_child(child)
					for cabin: Dictionary in vehicle_dictionary["cabins"]:
						var new_cabin: Node = EditVehicleCabin.instantiate()
						new_cabin.get_node("CabinCode/LineEdit").text = cabin["code"]
						new_cabin.get_node("CabinDesignation/LineEdit").text = cabin["designation"]
						new_cabin.get_node("CabinName/LineEdit").text = cabin["name"]
						new_cabin.get_node("CabinInternalName/TextEdit").text = "\n".join(cabin["internal_name"])
						get_node("%Cabins/VBoxContainer").add_child(new_cabin)
					get_node("%EditUsesAccessories/CheckBox").button_pressed = vehicle_dictionary["uses_accessories"]
					for child: Node in get_node("%EditAccessories/VBoxContainer").get_children():
						get_node("%EditAccessories/VBoxContainer").remove_child(child)
					for acc: String in vehicle_dictionary["accessories"].keys():
						var new_acc: Node = EditVehicleAccessory.instantiate()
						new_acc.get_node("HBoxContainer/LineEdit").text = acc
						new_acc.get_node("TextEdit").text = "\n".join(vehicle_dictionary["accessories"][acc])
						get_node("%EditAccessories/VBoxContainer").add_child(new_acc)


func save_vehicle_file() -> void:
	if alphanumericise(get_node("%EditAuthorASCII/LineEdit").text) != "" and \
			alphanumericise(get_node("%EditVehiclePath/LineEdit").text) != "":
		var popup := ConfirmationDialog.new()
		popup.title = "Overwrite?"
		popup.dialog_text = "Saving will overwrite the existing %s file.\n\nAre you sure you want to continue?" % "make.model"
		popup.size.y = 0
		popup.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
		popup.get_ok_button().pressed.connect(confirm_save_vehicle_file)
		self.add_child(popup)
		popup.popup_centered()


func confirm_save_vehicle_file() -> void:
	pass
	print("yep")
