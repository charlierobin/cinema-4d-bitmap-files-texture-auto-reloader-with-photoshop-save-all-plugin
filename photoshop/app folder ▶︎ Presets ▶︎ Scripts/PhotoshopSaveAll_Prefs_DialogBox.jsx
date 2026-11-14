
#target photoshop

var scriptFilePath = Folder($.fileName).parent.fsName;
$.evalFile(new File(scriptFilePath + '/PhotoshopSaveAll_lib.jsx.inc'));

function getSaveAllEnabled() {

	try {
		var desc = app.getCustomOptions(PREF_KEY);
		return desc.getBoolean(PREF_ID);
	}
	catch (e) {
		return true;
	}
}

function setSaveAllEnabled(enabled) {

	var desc = new ActionDescriptor();
	desc.putBoolean(PREF_ID, enabled);

	app.putCustomOptions(PREF_KEY, desc, true);
}

function sendEventToPaletteIfListening() {
	try {
		var plugPlug = new ExternalObject("lib:PlugPlugExternalObject");

		var eventObj = new CSXSEvent();
		eventObj.type = EVENT_SIGNATURE;
		eventObj.dispatch();
	}
	catch (e) {
		alert("Event error: " + e);
	}
}

var dlg = new Window("dialog", "Save All Preference");

dlg.orientation = "column";
dlg.alignChildren = "left";
dlg.spacing = 12;
dlg.margins = 16;

var chk = dlg.add(
	"checkbox",
	undefined,
	"Automatically save all other open documents"
);

chk.value = getSaveAllEnabled();

var buttons = dlg.add("group");
buttons.alignment = "right";

buttons.add("button", undefined, "OK");
buttons.add("button", undefined, "Cancel");

if (dlg.show() == 1) {
	setSaveAllEnabled(chk.value);
	sendEventToPaletteIfListening();
}
