const EVENT_SIGNATURE = "com.charlierobin.photoshopSaveAll.preferenceChanged";

const checkBox = document.getElementById("myCheck");

function getSaveAllEnabled() {

    cepBridge.evalScript("getSaveAllEnabled()", function (result) {

        var enabled = result === "true";

        checkBox.checked = enabled;
    });
}

function setSaveAllEnabled(value) {

    cepBridge.evalScript("setSaveAllEnabled(" + value + ")", function (result) { });
}

checkBox.addEventListener("click", function () {

    setSaveAllEnabled(checkBox.checked);
});

var csInterface = new CSInterface();

csInterface.addEventListener(EVENT_SIGNATURE, function (event) {

    getSaveAllEnabled();
});

getSaveAllEnabled();
