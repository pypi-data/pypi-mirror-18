'use strict';

angular.module('ajenti.supervisor', ['core', 'ajenti.augeas', 'ajenti.services', 'ajenti.passwd']);


'use strict';

angular.module('core').config(function ($routeProvider) {
    return $routeProvider.when('/view/supervisor', {
        templateUrl: '/supervisor:resources/partial/index.html',
        controller: 'SupervisorIndexController'
    });
});


'use strict';

angular.module('ajenti.supervisor').controller('SupervisorIndexController', function ($scope, augeas, notify, pageTitle, passwd, services, gettext) {
    pageTitle.set(gettext('Supervisor'));

    $scope.addProcess = function (name) {
        var path = $scope.config.insert('program:' + $scope.newProcessName, null);
        $scope.config.insert(path + '/command', 'true');
        $scope.newProcessName = '';
    };

    $scope.extractName = function (path) {
        if (!$scope.config || !path) {
            return null;
        }
        return $scope.config.getNode(path).name.split(':')[1];
    };

    $scope.save = function () {
        return augeas.set('supervisor', $scope.config).then(function () {
            return notify.success(gettext('Saved'));
        }).catch(function (e) {
            return notify.error(gettext('Could not save'), e.message);
        });
    };

    $scope.reload = function () {
        augeas.get('supervisor').then(function (config) {
            return $scope.config = config;
        });
        $scope.processServices = {};
        return services.getServices('supervisor').then(function (data) {
            return data.forEach(function (service) {
                return $scope.processServices[service.name] = service;
            });
        });
    };

    $scope.start = function (name) {
        return services.runOperation($scope.processServices[name], 'start').then(function () {
            return $scope.reload();
        }).catch(function (e) {
            return notify.error(gettext('Failed'), e.message);
        });
    };

    $scope.stop = function (name) {
        return services.runOperation($scope.processServices[name], 'stop').then(function () {
            return $scope.reload();
        }).catch(function (e) {
            return notify.error(gettext('Failed'), e.message);
        });
    };

    passwd.list().then(function (l) {
        return $scope.systemUsers = l;
    });

    $scope.reload();
});


