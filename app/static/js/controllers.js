"use strict";

angular.module("controllers", [])
    .controller("MainController", ["$scope",
        function($scope) {
            $scope.test = 0;
        }])
    .controller("TableController", ["$scope", "Player",
        function($scope, Player) {
            $scope.players = Player.query();
        }])
;
