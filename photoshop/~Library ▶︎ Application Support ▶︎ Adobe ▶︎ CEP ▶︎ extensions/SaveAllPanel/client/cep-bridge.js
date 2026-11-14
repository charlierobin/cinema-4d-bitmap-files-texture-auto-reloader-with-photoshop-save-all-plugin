/*
 * Minimal CEP bridge for this first test panel.
 * It exposes only the evalScript call needed by this project.
 * The full Adobe CSInterface.js library can be added later if we need
 * its wider set of CEP APIs.
 */
(function (global) {
    "use strict";

    global.cepBridge = {
        evalScript: function (script, callback) {
            if (!global.__adobe_cep__ ||
                typeof global.__adobe_cep__.evalScript !== "function") {
                if (callback) callback("CEP bridge is unavailable.");
                return;
            }
            global.__adobe_cep__.evalScript(script, callback || function () {});
        }
    };
}(window));
