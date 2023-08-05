'use strict';

angular.module('ajenti.network', ['core']);


'use strict';

angular.module('core').config(function ($routeProvider) {
    $routeProvider.when('/view/network', {
        templateUrl: '/network:resources/partial/index.html',
        controller: 'NetworkIndexController'
    });
});


'use strict';

angular.module('ajenti.network').controller('NetworkIndexController', function ($scope, $routeParams, $timeout, messagebox, notify, pageTitle, network, gettext) {
    pageTitle.set(gettext('Network'));

    $scope.knownFamilies = {
        inet: ['static', 'dhcp', 'manual', 'loopback'],
        inet6: ['static', 'dhcp', 'manual', 'loopback', 'auto']
    };

    $scope.knownAddressingNames = {
        static: gettext('Static'),
        auto: gettext('Auto'),
        dhcp: 'DHCP',
        manual: gettext('Manual'),
        loopback: gettext('Loopback')
    };

    $scope.reloadState = function () {
        $scope.state = {};
        $scope.config.forEach(function (iface) {
            return function (iface) {
                return network.getState(iface.name).then(function (state) {
                    return $scope.state[iface.name] = state;
                });
            }(iface);
        });
    };

    $scope.reload = function () {
        $scope.config = null;
        network.getConfig().then(function (data) {
            $scope.config = data;
            $scope.reloadState();
        });
        network.getHostname().then(function (hostname) {
            return $scope.hostname = hostname;
        });
    };

    $scope.save = function () {
        return network.setConfig($scope.config).then(function () {
            return $scope.reload();
        });
    };

    $scope.reload();

    $scope.upInterface = function (iface) {
        return network.up(iface.name).then(function () {
            notify.success(gettext('Interface activated'));
            $scope.reloadState();
        });
    };

    $scope.downInterface = function (iface) {
        return messagebox.show({
            title: gettext('Warning'),
            text: gettext('Deactivating a network interface can lock you out of the remote session'),
            positive: gettext('Deactivate'),
            negative: gettext('Cancel')
        }).then(function () {
            return network.down(iface.name).then(function () {
                notify.success(gettext('Interface deactivated'));
                $scope.reloadState();
            });
        });
    };

    $scope.restartInterface = function (iface) {
        return messagebox.show({
            title: gettext('Warning'),
            text: gettext('Restarting a network interface can lock you out of the remote session'),
            positive: gettext('Restart'),
            negative: gettext('Cancel')
        }).then(function () {
            return network.downup(iface.name).then(function () {
                return $timeout(function () {
                    notify.success(gettext('Interface reactivated'));
                    return $scope.reloadState();
                }, 2000);
            });
        });
    };

    $scope.setHostname = function (hostname) {
        return network.setHostname(hostname).then(function () {
            notify.success(gettext('Hostname changed'));
        }, function (e) {
            notify.error(gettext('Failed'), e.message);
        });
    };
});


'use strict';

angular.module('ajenti.network').controller('NetworkDNSController', function ($scope, notify, augeas, gettext) {
    augeas.get('resolv').then(function (config) {
        return $scope.config = config;
    });

    $scope.addNameserver = function () {
        $scope.config.insert('nameserver', $scope.newNameserver);
        $scope.newNameserver = '';
    };

    $scope.save = function () {
        return augeas.set('resolv', $scope.config).then(function () {
            notify.success(gettext('Saved'));
        }, function (e) {
            notify.error(gettext('Could not save'), e.message);
        });
    };
});


'use strict';

angular.module('ajenti.network').controller('NetworkHostsController', function ($scope, notify, augeas, gettext) {
    augeas.get('hosts').then(function (config) {
        return $scope.config = config;
    });

    $scope._ = {};

    $scope.addHost = function () {
        var path = $scope.config.insert('99', null);
        $scope.config.insert(path + '/ipaddr', '127.0.0.1');
        $scope.config.insert(path + '/canonical', $scope.newHost);
        $scope.newHost = '';
    };

    $scope.addAlias = function (path) {
        path = $scope.config.insert(path + '/alias', $scope._.newAlias);
        $scope._.newAlias = '';
    };

    $scope.save = function () {
        return augeas.set('hosts', $scope.config).then(function () {
            notify.success(gettext('Saved'));
        }, function (e) {
            notify.error(gettext('Could not save'), e.message);
        });
    };
});


'use strict';

angular.module('ajenti.network').service('network', function ($http, $q, tasks) {
    this.getConfig = function () {
        return $http.get("/api/network/config/get").then(function (response) {
            return response.data;
        });
    };

    this.setConfig = function (config) {
        return $http.post("/api/network/config/set", config).then(function (response) {
            return response.data;
        });
    };

    this.getState = function (iface) {
        return $http.get('/api/network/state/' + iface).then(function (response) {
            return response.data;
        });
    };

    this.up = function (iface) {
        return $http.get('/api/network/up/' + iface).then(function (response) {
            return response.data;
        });
    };

    this.down = function (iface) {
        return $http.get('/api/network/down/' + iface).then(function (response) {
            return response.data;
        });
    };

    this.downup = function (iface) {
        return $http.get('/api/network/downup/' + iface).then(function (response) {
            return response.data;
        });
    };

    this.getHostname = function () {
        return $http.get("/api/network/hostname/get").then(function (response) {
            return response.data;
        });
    };

    this.setHostname = function (hostname) {
        return $http.post("/api/network/hostname/set", hostname).then(function (response) {
            return response.data;
        });
    };

    return this;
});


