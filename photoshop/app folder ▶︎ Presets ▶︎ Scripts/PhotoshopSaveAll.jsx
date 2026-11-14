#target photoshop

var begDesc = "$$$/JavaScripts/PhotoshopSaveAll/Description=Whenever a document starts saving, save all other open documents." // endDesc
var begName = "$$$/JavaScripts/PhotoshopSaveAll/MenuName=SaveAll" // endName

var scriptFilePath = Folder($.fileName).parent.fsName;
$.evalFile(new File(scriptFilePath + '/PhotoshopSaveAll_lib.jsx.inc'));

function getSaveAllEnabled() {

	try {
		var preferences = app.getCustomOptions(PREF_KEY);

		return preferences.getBoolean(PREF_ID);
	}
	catch (e) {
		return true;
	}
}

var isEvent = (arguments.length > 0 && arguments[0] != null);

var errorsSaving = "";

if (getSaveAllEnabled() || !isEvent) {

	if (app.documents.length > 0) {

		var origActive = app.activeDocument;

		try {

			for (var i = 0; i < app.documents.length; i++) {

				var doc = app.documents[i];

				// if triggered by event, origActive will be saved directly by Photoshop
				// if NOT triggered by event, eg: by script command, we have to do the save ourselves

				if (isEvent && doc == origActive) continue;

				// if doc is unsaved, ie: no path to file on drive, I'm going to skip it

				var hasPath = true;

				try {
					var file = doc.fullName;
				}
				catch (e) {
					hasPath = false;
				}

				if (hasPath && !doc.saved) {

					app.activeDocument = doc;

					try {
						app.activeDocument.save();
					}
					catch (e) {
						errorsSaving = errorsSaving + doc.name + ": " + e.message + "\n";
					}
				}
			}
		}

		catch (e) {
			alert(e);
		}
		finally {
			app.activeDocument = origActive;
		}
	}
}

if (errorsSaving != "") {
	alert(errorsSaving);
}
