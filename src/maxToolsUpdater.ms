max_updater_start_path =  @"###MAXTOOLUPDATERPATH###\main.py"

macroScript OpenMaxToolsUpdater category:"Tools Updater" buttontext:"Open Max Tools Updater"
(
    global MTU_FORCE_LOAD = true
	python.ExecuteFile max_updater_start_path
)

maxToolMenu = menuMan.createMenu "Tools Updater"

maxToolMenu.addItem (menuMan.createActionItem "OpenMaxToolsUpdater" "Tools Updater") -1


mainMenu = menuMan.getMainMenuBar()
for i = mainMenu.numItems() to 1 by -1 do
	if (mainMenu.getItem i).getTitle() == "Tools Updater" then
		mainMenu.removeItem (mainMenu.getItem i)
mainMenu.addItem (menuMan.createSubMenuItem "Tools Updater" maxToolMenu) -1
menuMan.updateMenuBar()

global MTU_FORCE_LOAD = false
python.ExecuteFile max_updater_start_path