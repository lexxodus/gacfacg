"use strict";

angular.module("controllers", [])
    .controller("NavController", ["$scope",
        function($scope) {
            $scope.test = 0;
    }])
    .controller("NavController", [
        "$scope", function($scope) {
            $scope.page = 0;

            $scope.isActive = function (page){
                return $scope.page === page;
            };

            $scope.selectPage = function(page){
                $scope.page = page;
            };

    }])
    .controller("EntityController", [
        "$scope", "Player", "Level", "LevelType", "Task", "Event",
        function($scope, Player, Level, LevelType, Task, Event) {
            $scope.tab = 0;
            $scope.entity = "Player";
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
                        players.push(player);
                    });
                });
                $scope.rows = players;
                $scope.entity = "Player";
            };

            function getLevels() {
                var levels = [];
                Level.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        var level = {};
                        level["id"] = d.id;
                        level["name"] = d.name;
                        level["description"] = d.description;
                        levels.push(level);
                    });
                });
                $scope.rows = levels;
                $scope.entity = "Level";
            };

            function getLevelTypes() {
                var levelTypes = [];
                LevelType.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        var levelType = {};
                        levelType["id"] = d.id;
                        levelType["name"] = d.name;
                        levelType["description"] = d.description;
                        levelTypes.push(levelType);
                    });
                });
                $scope.rows = levelTypes;
                $scope.entity = "Level Type";
            };

            function getTasks() {
                var tasks = [];
                Task.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        var task = {};
                        task["id"] = d.id;
                        task["name"] = d.name;
                        task["description"] = d.description;
                        tasks.push(task);
                    });
                });
                $scope.rows = tasks;
                $scope.entity = "Task";
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
                        events.push(event);
                    });
                });
                $scope.rows = events;
                $scope.entity = "Event";
            };
    }])
    .controller("HistoryController", [
        "$scope", "LevelInstance", "Participation", "TriggeredEvent",
        function($scope, LevelInstance, Participation, TriggeredEvent) {
            $scope.tab = 0;
            $scope.entity = "Level Instance";
            $scope.rows;

            // initialize with Level Instances
            getLevelInstances();

            $scope.isActive = function (tab){
                return $scope.tab === tab;
            };

            $scope.selectTab = function(tab){
                console.log(tab);
                switch(tab){
                    case 0:
                        getLevelInstances();
                        break;
                    case 1:
                        getParticipations();
                        break;
                    case 2:
                        getTriggeredEvents();
                        break;
                }
                $scope.tab = tab;
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
                        levelInstances.push(levelInstance);
                    });
                });
                $scope.rows = levelInstances;
                $scope.entity = "Level Instance";
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
                        participation["end time"] = d.end_time;
                        participations.push(participation);
                    });
                });
                $scope.rows = participations;
                $scope.entity = "Participations";
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
                        triggeredEvents.push(triggeredEvent);
                    });
                });
                $scope.rows = triggeredEvents;
                $scope.entity = "Triggered Events";
            };
    }])
    .filter('capitalize', function() {
    return function(input) {
      return input.charAt(0).toUpperCase() + input.substr(1).toLowerCase();
    }
})
;
