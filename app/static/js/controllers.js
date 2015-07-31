"use strict";

angular.module("controllers", [])
    .controller("MainController", ["$scope",
        function($scope) {
            $scope.test = 0;
        }])
    .controller("TableController", [
        "$scope", "Player", "Level", "LevelType", "Task", "Event",
        function($scope, Player, Level, LevelType, Task, Event) {
            $scope.tab = 1;
            $scope.rows;

            getPlayers();

            function getPlayers() {
                var players = [];
                Player.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        var player = {};
                        player["id"] = d.id;
                        delete d["id"];
                        for (var k in d){
                            if (typeof(d[k]) === "function"){
                                continue;
                            }
                            player[k] = d[k];
                        }
                        players.push(player);
                    });
                });
                $scope.rows = players;
            };

            function getLevels() {
                var levels = [];
                Level.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        var level = {};
                        level["id"] = d.id;
                        level["name"] = d.name;
                        level["description"] = d.description;
                        delete d["id"];
                        delete d["name"];
                        delete d["description"];
                        for (var k in d){
                            if (typeof(d[k]) === "function"){
                                continue;
                            }
                            level[k] = d[k];
                        }
                        levels.push(player);
                    });
                });
                $scope.rows = levels;
            };

            // $scope.getRows = function () {
            //     console.log("lalal");
            //     return $scope.getPlayers();
            // };

            // $scope.rows = function () {
            //     console.log("lalal");
            //     return $scope.getPlayers();
            // };

            //  $scope.rows = function () {
            //      console.log("la");
            //      var data = Player.query();
            //      console.log(data);
            //      var players = [];
            //      for(var d in data){
            //          var player = {};
            //          player["id"] = d.id;
            //          delete d["id"];
            //          for (var k in d){
            //              player[k] = d[k];
            //          }
            //          players.push(player);
            //      }
            //      // $scope.rows = players;
            //      // $scope.rows = Player.query();
            //      return $scope.rows;
            //  };
        }])
    .filter('capitalize', function() {
    return function(input) {
      return input.charAt(0).toUpperCase() + input.substr(1).toLowerCase();
    }
});
;
