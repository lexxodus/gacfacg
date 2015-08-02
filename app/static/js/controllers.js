"use strict";

angular.module("controllers", [])
    .controller("MainController", ["$scope",
        function($scope) {
            $scope.test = 0;
        }])
    .controller("TableController", [
        "$scope", "Player", "Level", "LevelType", "Task", "Event",
        "LevelInstance", "Participation", "TriggeredEvent",
        function($scope, Player, Level, LevelType, Task, Event,
                LevelInstance, Participation, TriggeredEvent) {
            $scope.tab = 0;
            $scope.rows;

            // initialize with player
            getPlayers();

            $scope.isActive = function (tab){
                return $scope.tab === tab;
            };

            $scope.selectTab = function(tab){
                switch(tab){
                    case 0:
                        getPlayers();
                        break;
                    case 1:
                        getLevels();
                        break;
                    case 2:
                        getLevelTypes();
                        break;
                    case 3:
                        getTasks();
                        break;
                    case 4:
                        getEvents();
                        break;
                    case 5:
                        getLevelInstances();
                        break;
                    case 6:
                        getParticipations();
                        break;
                    case 7:
                        getTriggeredEvents();
                        break;
                }
                $scope.tab = tab;
            };

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
                        levels.push(level);
                    });
                });
                $scope.rows = levels;
            };

            function getLevelTypes() {
                var levelTypes = [];
                LevelType.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        var levelType = {};
                        levelType["id"] = d.id;
                        levelType["name"] = d.name;
                        levelType["description"] = d.description;
                        delete d["id"];
                        delete d["name"];
                        delete d["description"];
                        for (var k in d){
                            if (typeof(d[k]) === "function"){
                                continue;
                            }
                            levelType[k] = d[k];
                        }
                        levelTypes.push(levelType);
                    });
                });
                $scope.rows = levelTypes;
            };

            function getTasks() {
                var tasks = [];
                Task.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        var task = {};
                        task["id"] = d.id;
                        task["name"] = d.name;
                        task["description"] = d.description;
                        delete d["id"];
                        delete d["name"];
                        delete d["description"];
                        for (var k in d){
                            if (typeof(d[k]) === "function"){
                                continue;
                            }
                            task[k] = d[k];
                        }
                        tasks.push(task);
                    });
                });
                $scope.rows = tasks;
            };

            function getEvents() {
                var events = [];
                Event.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        var event = {};
                        event["id"] = d.id;
                        event["tid"] = d.tid;
                        event["name"] = d.name;
                        event["description"] = d.description;
                        delete d["id"];
                        delete d["tid"];
                        delete d["name"];
                        delete d["description"];
                        for (var k in d){
                            if (typeof(d[k]) === "function"){
                                continue;
                            }
                            event[k] = d[k];
                        }
                        events.push(event);
                    });
                });
                $scope.rows = events;
            };

            function getLevelInstances() {
                var levelInstances = [];
                LevelInstance.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        var levelInstance = {};
                        levelInstance["id"] = d.id;
                        levelInstance["lid"] = d.lid;
                        levelInstance["start time"] = d.start_time;
                        levelInstance["end time"] = d.end_time;
                        delete d["id"];
                        delete d["lid"];
                        delete d["start_time"];
                        delete d["end_time"];
                        for (var k in d){
                            if (typeof(d[k]) === "function"){
                                continue;
                            }
                            levelInstance[k] = d[k];
                        }
                        levelInstances.push(levelInstance);
                    });
                });
                $scope.rows = levelInstances;
            };

            function getParticipations() {
                var participations = [];
                Participation.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        var participation = {};
                        participation["id"] = d.id;
                        participation["pid"] = d.pid;
                        participation["liid"] = d.liid;
                        participation["start time"] = d.start_time;
                        participation["end time"] = d.ent_time;
                        delete d["id"];
                        delete d["pid"];
                        delete d["liid"];
                        delete d["start_time"];
                        delete d["end_time"];
                        for (var k in d){
                            if (typeof(d[k]) === "function"){
                                continue;
                            }
                            participation[k] = d[k];
                        }
                        participations.push(participation);
                    });
                });
                $scope.rows = participations;
            };

            function getTriggeredEvents() {
                var triggeredEvents = [];
                TriggeredEvent.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        var triggeredEvent = {};
                        triggeredEvent["id"] = d.id;
                        triggeredEvent["paid"] = d.paid;
                        triggeredEvent["eid"] = d.eid;
                        triggeredEvent["timestamp"] = d.timestamp;
                        // delete d["id"];
                        // delete d["paid"];
                        // delete d["eid"];
                        // delete d["timestamp"];
                        // for (var k in d){
                        //     if (typeof(d[k]) === "function"){
                        //         continue;
                        //     }
                        //     triggeredEvent[k] = d[k];
                        // }
                        triggeredEvents.push(triggeredEvent);
                    });
                });
                $scope.rows = triggeredEvents;
            };
        }])
    .filter('capitalize', function() {
    return function(input) {
      return input.charAt(0).toUpperCase() + input.substr(1).toLowerCase();
    }
});
;
