'use strict';

angular.module('ajenti.power', ['core']);

angular.module('ajenti.power').run(function (customization) {
    customization.plugins.power = {};
    customization.plugins.power.hideBatteries = false;
    customization.plugins.power.hideAdapters = false;
});


'use strict';

angular.module('core').config(function ($routeProvider) {
    return $routeProvider.when('/view/power', {
        templateUrl: '/power:resources/partial/index.html',
        controller: 'PowerIndexController'
    });
});


'use strict';

angular.module('ajenti.power').controller('PowerIndexController', function ($scope, $interval, notify, pageTitle, power, messagebox, gettext) {
    pageTitle.set(gettext('Power management'));

    power.getUptime().then(function (uptime) {
        $scope.uptime = uptime;

        var int = $interval(function () {
            return $scope.uptime += 1;
        }, 1000);

        return $scope.$on('$destroy', function () {
            return $interval.cancel(int);
        });
    });

    power.getBatteries().then(function (batteries) {
        return $scope.batteries = batteries;
    });

    power.getAdapters().then(function (adapters) {
        return $scope.adapters = adapters;
    });

    $scope.poweroff = function () {
        return messagebox.show({
            title: gettext('Warning'),
            text: gettext('Are you sure you want to shutdown the system now?'),
            positive: gettext('Shutdown'),
            negative: gettext('Cancel')
        }).then(function () {
            return power.poweroff().then(function () {
                return messagebox.show({ progress: true, text: 'System is shutting down' });
            });
        });
    };

    $scope.reboot = function () {
        return messagebox.show({
            title: gettext('Warning'),
            text: gettext('Are you sure you want to reboot the system now?'),
            positive: gettext('Reboot'),
            negative: gettext('Cancel')
        }).then(function () {
            return power.reboot().then(function () {
                return messagebox.show({
                    progress: true,
                    text: gettext('System is rebooting. We will try to reconnect with it.')
                });
            });
        });
    };

    $scope.suspend = function () {
        return messagebox.show({
            title: gettext('Warning'),
            text: gettext('Are you sure you want to suspend the system now?'),
            positive: gettext('Suspend'),
            negative: gettext('Cancel')
        }).then(function () {
            return power.suspend().then(function () {
                return messagebox.show({ progress: true, text: gettext('System is suspending') });
            });
        });
    };

    $scope.hibernate = function () {
        return messagebox.show({
            title: gettext('Warning'),
            text: gettext('Are you sure you want to hibernate the system now?'),
            positive: gettext('Hibernate'),
            negative: gettext('Cancel')
        }).then(function () {
            return power.hibernate().then(function () {
                return messagebox.show({ progress: true, text: gettext('System is hibernating') });
            });
        });
    };
});


'use strict';

angular.module('ajenti.power').controller('PowerWidgetController', function ($scope, services) {
    $scope.$on('widget-update', function ($event, id, data) {
        if (id !== $scope.widget.id) {
            return;
        }
        $scope.batteries = data.batteries;
        $scope.adapters = data.adapters;
    });
});


'use strict';

angular.module('ajenti.power').service('power', function ($http) {
    this.getUptime = function () {
        return $http.get("/api/power/uptime").success(function (response) {
            return response.data;
        });
    };

    this.getBatteries = function () {
        return $http.get("/api/power/batteries").success(function (response) {
            return response.data;
        });
    };

    this.getAdapters = function () {
        return $http.get("/api/power/adapters").success(function (response) {
            return response.data;
        });
    };

    this.poweroff = function () {
        return $http.get("/api/power/poweroff").success(function (response) {
            return response.data;
        });
    };

    this.reboot = function () {
        return $http.get("/api/power/reboot").success(function (response) {
            return response.data;
        });
    };

    this.suspend = function () {
        return $http.get("/api/power/suspend").success(function (response) {
            return response.data;
        });
    };

    this.hibernate = function () {
        return $http.get("/api/power/hibernate").success(function (response) {
            return response.data;
        });
    };

    return this;
});


