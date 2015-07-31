"use strict";

angular.module("controllers", [])
    .controller("MainController", ["$scope",
        function($scope) {
            $scope.test = 0;
        }])
    .controller("TableController", [
        "$scope", "Player", "Level", "LevelType", "Task", "Event",
        function($scope, Player, Level, LevelType, Task, Event) {
            $scope.rows = Player.query(); //$scope.getPlayers();

            $scope.getPlayers = function () {
                var data = Player.query();
                console.log(data);
                var players = [];
                for(var d in data){
                    var player = {};
                    player["id"] = d.id;
                    delete d["id"];
                    for (var k in d){
                        player[k] = d[k];
                    }
                    players.push(player);
                }
                // $scope.rows = players;
                // $scope.rows = Player.query();
                return $scope.rows;
            };
        }])
;
