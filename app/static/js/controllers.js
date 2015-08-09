"use strict";

var RESOURCE_KEYS = ["$promise", "$resolved"];

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
            $scope.addLink = "player-add";
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
                }
                $scope.tab = tab;
            };

            $scope.remove = function(id) {
                switch($scope.tab){
                    case 0:
                        Player.remove({id: id});
                        getPlayers();
                        break;
                    case 1:
                        Level.remove({id: id});
                        getLevels();
                        break;
                    case 2:
                        LevelType.remove({id: id});
                        getLevelTypes();
                        break;
                    case 3:
                        Task.remove({id: id});
                        getTasks();
                        break;
                    case 4:
                        Event.remove({id: id});
                        getEvents();
                        break;
                }
            }

            function getPlayers() {
                var players = [];
                Player.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        var player = {};
                        player["id"] = d.id;
                        player["name"] = d.name;
                        player["view_url"] = "player-view/" + d.id;
                        player["edit_url"] = "player-edit/" + d.id;
                        players.push(player);
                    });
                });
                $scope.rows = players;
                $scope.entity = "Player";
                $scope.addLink = "player-add";
            };

            function getLevels() {
                var levels = [];
                Level.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        var level = {};
                        level["id"] = d.id;
                        level["name"] = d.name;
                        level["description"] = d.description;
                        level["view_url"] = "level-view/" + d.id;
                        level["edit_url"] = "level-edit/" + d.id;
                        levels.push(level);
                    });
                });
                $scope.rows = levels;
                $scope.entity = "Level";
                $scope.addLink = "level-add";
            };

            function getLevelTypes() {
                var levelTypes = [];
                LevelType.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        var levelType = {};
                        levelType["id"] = d.id;
                        levelType["name"] = d.name;
                        levelType["description"] = d.description;
                        levelType["view_url"] = "level_type-view/" + d.id;
                        levelType["edit_url"] = "level_type-edit/" + d.id;
                        levelTypes.push(levelType);
                    });
                });
                $scope.rows = levelTypes;
                $scope.entity = "Level Type";
                $scope.addLink = "level_type-type-add";
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
                $scope.addLink = "task-add";
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
                $scope.addLink = "event-add";
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
    .controller("PlayerAddEditController", [
        "$scope", "$routeParams", "$location", "Player",
        function($scope, $routeParams, $location, Player) {
            $scope.expected_values = ["id", "name"];
            $scope.required_values = ["name"];
            $scope.unique_edit = "";
            $scope.name = "";
            $scope.uniques = [];
            $scope.customKeys = [];
            $scope.customValues = [];
            $scope.customRows = 0;

            getPlayerNames();

            if ($routeParams.hasOwnProperty("id")){
                loadPlayer($routeParams.id);
            }

            $scope.addCustomValue = function () {
                $scope.customKeys.push("");
                $scope.customValues.push("");
                $scope.customRows++;
            };

            $scope.removeCustomValue = function (i) {
                $scope.customRows--;
                $scope.customKeys.splice(i, 1);
                $scope.customValues.splice(i, 1);
            };

            $scope.range = function (n) {
                return new Array(n);
            };

            $scope.save = function () {
                var data = {
                    "name": $scope.name,
                }
                for (var k in $scope.customKeys){
                    if($scope.customKeys.hasOwnProperty(k)){
                        data[$scope.customKeys[k].toLowerCase()] = $scope.customValues[k];
                    }
                }
                if($scope.unique_edit){
                    Player.update({id:$routeParams.id}, data)
                } else {
                    Player.save(data);
                }

                $location.path("entities")
            };

            $scope.cancel = function (form) {
                if (form) {
                    form.$setPristine();
                    form.$setUntouched();
                }
                $scope.name = "";
                $scope.customRows = 0;
                $scope.customKeys = [];
                $scope.customValues = [];
            };

            function getPlayerNames() {
                Player.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        $scope.uniques.push(d.name);
                    });
                });
            };

            function loadPlayer(id) {
                Player.get({id: id}).$promise.then(function (data) {
                    var clone = {};
                    $scope.name = data.name;
                    $scope.unique_edit = data.name;
                    angular.copy(data, clone);
                    for (var key  in RESOURCE_KEYS){
                        delete clone[RESOURCE_KEYS[key]];
                    }
                    for (var key in $scope.expected_values){
                        delete clone[$scope.expected_values[key]];
                    }
                    angular.forEach(clone, function (v, k){
                        $scope.customRows++;
                        $scope.customKeys.push(k);
                        $scope.customValues.push(v);
                    });
                });
            };
    }])
    .controller("PlayerViewController", [
        "$scope", "$routeParams", "$location", "Player",
        function($scope, $routeParams, $location, Player) {
            $scope.expected_values = ["id", "name"];
            $scope.name = "";
            $scope.customValues = {};

            loadPlayer($routeParams.id);

            function loadPlayer(id) {
                Player.get({id: id}).$promise.then(function (data) {
                    var clone = {};
                    $scope.name = data.name;
                    angular.copy(data, clone);
                    for (var key  in RESOURCE_KEYS){
                        delete clone[RESOURCE_KEYS[key]];
                    }
                    for (var key in $scope.expected_values){
                        delete clone[$scope.expected_values[key]];
                    }
                    angular.forEach(clone, function (v, k){
                        $scope.customValues[k] = v;
                    });
                });
            };
    }])
    .controller("LevelAddEditController", [
        "$scope", "$routeParams", "$location", "Level", "LevelType",
        function($scope, $routeParams, $location, Level, LevelType) {
            $scope.expected_values = ["id", "name", "description", "level_types"];
            $scope.required_values = ["name"];
            $scope.unique_edit = "";
            $scope.name = "";
            $scope.description = "";
            $scope.levelTypes = {};
            $scope.levelTypesSelected = {};
            $scope.uniques = [];
            $scope.customKeys = [];
            $scope.customValues = [];
            $scope.customRows = 0;

            getLevelTypes();
            getLevelNames();

            if ($routeParams.hasOwnProperty("id")){
                loadLevel($routeParams.id);
            }

            $scope.addCustomValue = function () {
                $scope.customKeys.push("");
                $scope.customValues.push("");
                $scope.customRows++;
            };

            $scope.removeCustomValue = function (i) {
                $scope.customRows--;
                $scope.customKeys.splice(i, 1);
                $scope.customValues.splice(i, 1);
            };

            $scope.range = function (n) {
                return new Array(n);
            };

            $scope.save = function () {
                var lt = [];
                for (var k in $scope.levelTypesSelected){
                    if($scope.levelTypesSelected.hasOwnProperty(k) &&
                            $scope.levelTypesSelected[k]) {
                        lt.push(k);
                    }
                }
                var data = {
                    "name": $scope.name,
                    "description": $scope.description,
                    "level_types": lt
                }
                for (var k in $scope.customKeys){
                    if($scope.customKeys.hasOwnProperty(k)){
                        data[$scope.customKeys[k].toLowerCase()] = $scope.customValues[k];
                    }
                }
                if($scope.unique_edit){
                    Level.update({id:$routeParams.id}, data)
                } else {
                    Level.save(data);
                }

                $location.path("entities")
            };

            $scope.cancel = function (form) {
                if (form) {
                    form.$setPristine();
                    form.$setUntouched();
                }
                $scope.name = "";
                $scope.description = "";
                $scope.customRows = 0;
                $scope.customKeys = [];
                $scope.customValues = [];
            };

            function getLevelTypes() {
                LevelType.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        $scope.levelTypes[d.id] = d.name;
                        $scope.levelTypesSelected[d.id] = false;
                    });
                });
            };

            function getLevelNames() {
                Level.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        $scope.uniques.push(d.name);
                    });
                });
            };

            function loadLevel(id) {
                Level.get({id: id}).$promise.then(function (data) {
                    var clone = {};
                    $scope.name = data.name;
                    $scope.unique_edit = data.name;
                    $scope.description = data.description;
                    for(var lt in data.level_types){
                        $scope.levelTypesSelected[data.level_types[lt]] = true;
                    }
                    angular.copy(data, clone);
                    for (var key  in RESOURCE_KEYS){
                        delete clone[RESOURCE_KEYS[key]];
                    }
                    for (var key in $scope.expected_values){
                        delete clone[$scope.expected_values[key]];
                    }
                    angular.forEach(clone, function (v, k){
                        $scope.customRows++;
                        $scope.customKeys.push(k);
                        $scope.customValues.push(v);
                    });
                });
            };
    }])
    .controller("LevelViewController", [
        "$scope", "$routeParams", "$location", "Level", "LevelType",
        function($scope, $routeParams, $location, Level, LevelType) {
            $scope.expected_values = ["id", "name", "description", "level_types"];
            $scope.name = "";
            $scope.description = "";
            $scope.levelTypes = {};
            $scope.levelTypesSelected = [];
            $scope.customValues = {};

            getLevelTypes();
            loadLevel($routeParams.id);

            function getLevelTypes() {
                LevelType.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        console.log(d.id, d.name);
                        $scope.levelTypes[d.id] = d.name;
                    });
                });
            };

            function loadLevel(id) {
                Level.get({id: id}).$promise.then(function (data) {
                    var clone = {};
                    $scope.name = data.name;
                    $scope.description = data.description;
                    for(var lt in data.level_types){
                        $scope.levelTypesSelected.push(
                            $scope.levelTypes[data.level_types[lt]]);
                    }
                    angular.copy(data, clone);
                    for (var key  in RESOURCE_KEYS){
                        delete clone[RESOURCE_KEYS[key]];
                    }
                    for (var key in $scope.expected_values){
                        delete clone[$scope.expected_values[key]];
                    }
                    angular.forEach(clone, function (v, k){
                        $scope.customValues[k] = v;
                    });
                });
            };
    }])
    .controller("LevelTypeAddEditController", [
        "$scope", "$routeParams", "$location", "LevelType",
        function($scope, $routeParams, $location, LevelType) {
            $scope.expected_values = ["id", "name", "description"];
            $scope.required_values = ["name"];
            $scope.unique_edit = "";
            $scope.name = "";
            $scope.description = "";
            $scope.uniques = [];
            $scope.customKeys = [];
            $scope.customValues = [];
            $scope.customRows = 0;

            getLevelTypeNames();

            if ($routeParams.hasOwnProperty("id")){
                loadLevelType($routeParams.id);
            }

            $scope.addCustomValue = function () {
                $scope.customKeys.push("");
                $scope.customValues.push("");
                $scope.customRows++;
            };

            $scope.removeCustomValue = function (i) {
                $scope.customRows--;
                $scope.customKeys.splice(i, 1);
                $scope.customValues.splice(i, 1);
            };

            $scope.range = function (n) {
                return new Array(n);
            };

            $scope.save = function () {
                var data = {
                    "name": $scope.name,
                    "description": $scope.description,
                }
                for (var k in $scope.customKeys){
                    if($scope.customKeys.hasOwnProperty(k)){
                        data[$scope.customKeys[k].toLowerCase()] = $scope.customValues[k];
                    }
                }
                if($scope.unique_edit){
                    LevelType.update({id:$routeParams.id}, data)
                } else {
                    LevelType.save(data);
                }

                $location.path("entities")
            };

            $scope.cancel = function (form) {
                if (form) {
                    form.$setPristine();
                    form.$setUntouched();
                }
                $scope.name = "";
                $scope.description = "";
                $scope.customRows = 0;
                $scope.customKeys = [];
                $scope.customValues = [];
            };

            function getLevelTypeNames() {
                LevelType.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        $scope.uniques.push(d.name);
                    });
                });
            };

            function loadLevelType(id) {
                LevelType.get({id: id}).$promise.then(function (data) {
                    var clone = {};
                    $scope.name = data.name;
                    $scope.unique_edit = data.name;
                    $scope.description = data.description;
                    angular.copy(data, clone);
                    for (var key  in RESOURCE_KEYS){
                        delete clone[RESOURCE_KEYS[key]];
                    }
                    for (var key in $scope.expected_values){
                        delete clone[$scope.expected_values[key]];
                    }
                    angular.forEach(clone, function (v, k){
                        $scope.customRows++;
                        $scope.customKeys.push(k);
                        $scope.customValues.push(v);
                    });
                });
            };
    }])
    .controller("LevelTypeViewController", [
        "$scope", "$routeParams", "$location", "LevelType",
        function($scope, $routeParams, $location, LevelType) {
            $scope.expected_values = ["id", "name", "description"];
            $scope.name = "";
            $scope.description = "";
            $scope.customValues = {};

            loadLevelType($routeParams.id);

            function loadLevelType(id) {
                LevelType.get({id: id}).$promise.then(function (data) {
                    var clone = {};
                    $scope.name = data.name;
                    $scope.description = data.description;
                    for (var key  in RESOURCE_KEYS){
                        delete clone[RESOURCE_KEYS[key]];
                    }
                    for (var key in $scope.expected_values){
                        delete clone[$scope.expected_values[key]];
                    }
                    angular.forEach(clone, function (v, k){
                        $scope.customValues[k] = v;
                    });
                });
            };
    }])
    .filter('capitalize', function() {
    return function(input) {
      return input.charAt(0).toUpperCase() + input.substr(1).toLowerCase();
    }})
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
;
