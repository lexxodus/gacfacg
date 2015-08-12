"use strict";

angular.module("directives", [])
    .directive("unexpected", function () {
        return {
            require: "ngModel",
            link: function(scope, elm, attrs, ctrl) {
                ctrl.$validators.unexpected = function(modelValue, viewValue){
                    if (ctrl.$isEmpty(modelValue)) {
                        return true;
                    }

                    for (var value in scope.expected_values) {
                        if (modelValue.toLowerCase() == scope.expected_values[value]){
                            return false;
                        }
                    };

                    return true;
                };
            }
        };
    })
    .directive("unique", function () {
        return {
            require: "ngModel",
            link: function(scope, elm, attrs, ctrl) {
                ctrl.$validators.unique = function(modelValue, viewValue){
                    if (ctrl.$isEmpty(modelValue) || modelValue == scope.unique_edit) {
                        return true;
                    }

                    for (var value in scope.uniques) {
                        if (modelValue == scope.uniques[value]){
                            return false;
                        }
                    };

                    return true;
                };
            }
        };
    })
    .directive('convertToNumber', function() {
        return {
            require: 'ngModel',
            link: function(scope, element, attrs, ngModel) {
                ngModel.$parsers.push(function(val) {
                    return parseInt(val, 10);
                });
                ngModel.$formatters.push(function(val) {
                    return '' + val;
                });
            }
        };
    });
;