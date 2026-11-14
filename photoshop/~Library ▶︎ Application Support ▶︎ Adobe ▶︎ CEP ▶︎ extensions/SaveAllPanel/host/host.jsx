/* ExtendScript loaded by the CEP panel into Photoshop's scripting engine. */

// var scriptFilePath = Folder($.fileName).parent.fsName;
// var f = new File(scriptFilePath + 'PhotoshopSaveAll_lib.jsx.inc')
// $.evalFile(f);

// hoped to be able to share some constants with other scripts, but can't get above to work

var PREF_KEY = "com.charlierobin.photoshopSaveAll";
var PREF_ID = app.stringIDToTypeID("enabled");

function getSaveAllEnabled() {

    try {
        var desc = app.getCustomOptions(PREF_KEY);
        return desc.getBoolean(PREF_ID);
    }
    catch (e) {
        // No preference has been stored yet, so return default: true
        return true;
    }
}

function setSaveAllEnabled(enabled) {

    var desc = new ActionDescriptor();
    desc.putBoolean(PREF_ID, enabled);

    app.putCustomOptions(PREF_KEY, desc, true);

    return enabled;
}
