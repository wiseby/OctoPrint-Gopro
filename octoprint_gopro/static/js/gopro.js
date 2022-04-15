/*
 * View model for OctoPrint-Gopro
 *
 * Author: Lucas Wiseby
 * License: AGPLv3
 */
$(function() {
    function GoproViewModel(parameters) {
        var self = this;

        self.settingsViewModel = parameters[0];

        self.connecting = ko.observable(false);
        self.paired = ko.observable(false);
        self.message = ko.observable('');

        self.resolution = ko.observable('4k');
        self.frames = ko.observable('60');
        self.mode = ko.observable('cinematic');

        self.connectGopro = function() {
            const payload = {
                command: 'connect',
                identifier: ''
            };
            self.connecting(true);
            $.ajax({
                url: API_BASEURL + "plugin/gopro",
                type: "POST",
                dataType: "json",
                data: JSON.stringify(payload),
                contentType: "application/json; charset=UTF-8",
                success: function(response) {
                    console.log('Response: ', response);
                    self.paired(response.success);
                    if (!response.success && response.hasOwnProperty("msg")) {
                        self.message(response.msg);
                    } else {
                        self.message(undefined);
                    }
                },
                complete: function() {
                    self.connecting(false);
                }
            });
        }

        self.testPhoto = function() {
            const payload = {
                command: 'testPic',
                identifier: ''
            };
            $.ajax({
                url: API_BASEURL + "plugin/gopro",
                type: "POST",
                dataType: "json",
                data: JSON.stringify(payload),
                contentType: "application/json; charset=UTF-8",
                success: function(response) {
                    console.log('Response: ', response);
                    self.paired(response.success);
                    if (!response.success && response.hasOwnProperty("msg")) {
                        self.message(response.msg);
                    } else {
                        self.message(undefined);
                    }
                },
                complete: function() {
                    self.connecting(false);
                }
            });
        }

        // TODO: Implement your plugin's view model here.
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: GoproViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ "settingsViewModel" ],
        // Elements to bind to, e.g. #settings_plugin_gopro, #tab_plugin_gopro, ...
        elements: [ settings_plugin_gopro ]
    });
});
