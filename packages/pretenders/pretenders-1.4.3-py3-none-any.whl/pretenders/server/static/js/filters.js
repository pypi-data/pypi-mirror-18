'use strict';

/* Filters */

angular.module('pretenders.filters', [])
.filter('interpolate', ['version', function (version) {
    return function (text) {
        return String(text).replace(/\%VERSION\%/mg, version);
    };
}]);
