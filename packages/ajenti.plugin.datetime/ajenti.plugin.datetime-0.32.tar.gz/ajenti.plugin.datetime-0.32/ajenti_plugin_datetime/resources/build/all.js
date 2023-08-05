'use strict';

angular.module('ajenti.datetime', ['core']);

angular.module('ajenti.datetime').run(function (customization) {
    return customization.plugins.datetime = {};
});

angular.module('ajenti.datetime').directive('neutralTimezone', function () {
    return {
        restrict: 'A',
        priority: 1,
        require: 'ngModel',
        link: function link(scope, element, attrs, ctrl) {
            ctrl.$formatters.push(function (value) {
                var date = new Date(Date.parse(value));
                date = new Date(date.getTime() + 60000 * new Date().getTimezoneOffset());
                return date;
            });

            ctrl.$parsers.push(function (value) {
                return new Date(value.getTime() - 60000 * new Date().getTimezoneOffset());
            });
        }
    };
});


'use strict';

angular.module('core').config(function ($routeProvider) {
    $routeProvider.when('/view/datetime', {
        templateUrl: '/datetime:resources/partial/index.html',
        controller: 'DateTimeIndexController'
    });
});


'use strict';

angular.module('ajenti.datetime').controller('DateTimeIndexController', function ($scope, $interval, $timeout, notify, pageTitle, datetime, gettext) {
    pageTitle.set(gettext('Date & Time'));

    datetime.listTimezones().then(function (data) {
        return $scope.timezones = data;
    });

    $scope.refresh = function () {
        return datetime.getTimezone().then(function (data) {
            $scope.timezone = data.tz;
            $scope.offset = data.offset;

            $scope._.time = undefined;
            datetime.getTime().then(function (time) {
                return $scope._.time = new Date((time + $scope.offset) * 1000);
            });
        });
    };

    $scope.refresh();

    $scope._ = {};

    $scope.setTimezone = function () {
        return datetime.setTimezone($scope.timezone).then(function () {
            return $timeout(function () {
                $scope.refresh();
                notify.success(gettext('Timezone set'));
            }, 1000);
        }).catch(function (e) {
            return notify.error(gettext('Failed'), e.message);
        });
    };

    $scope.setTime = function () {
        return datetime.setTime($scope._.time.getTime() / 1000 - $scope.offset).then(function () {
            return notify.success(gettext('Time set'));
        }, function (e) {
            return notify.error(gettext('Failed'), e.message);
        });
    };

    $scope.syncTime = function () {
        notify.info(gettext('Synchronizing...'));
        return datetime.syncTime().then(function (time) {
            $scope._.time = new Date(time * 1000);
            notify.success(gettext('Time synchronized'));
        }, function (e) {
            return notify.error(gettext('Failed'), e.message);
        });
    };
});


'use strict';

angular.module('ajenti.datetime').service('datetime', function ($http, $q, tasks) {
    this.listTimezones = function () {
        return $http.get("/api/datetime/tz/list").then(function (response) {
            return response.data;
        });
    };

    this.getTimezone = function () {
        return $http.get("/api/datetime/tz/get").then(function (response) {
            return response.data;
        });
    };

    this.setTimezone = function (tz) {
        return $http.get('/api/datetime/tz/set/' + tz).then(function (response) {
            return response.data;
        });
    };

    this.getTime = function () {
        return $http.get('/api/datetime/time/get').then(function (response) {
            return response.data;
        });
    };

    this.setTime = function (time) {
        return $http.get('/api/datetime/time/set/' + time).then(function (response) {
            return response.data;
        });
    };

    this.syncTime = function () {
        return $http.get('/api/datetime/time/sync').then(function (response) {
            return response.data;
        });
    };

    return this;
});


