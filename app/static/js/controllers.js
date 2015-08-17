"use strict";

var RESOURCE_KEYS = ["$promise", "$resolved"];

angular.module("controllers", ["directives"])
    .controller("NavController", [
        "$scope", "$location", function($scope, $location) {
            $scope.page = $location.path();

            $scope.isActive = function (page){
                return $scope.page == page;
            };

            $scope.selectPage = function(page){
                $scope.page = page;
            };

    }])
    .controller("EntityController", [
        "$scope", "$route", "Player", "Level", "LevelType", "Task", "Event",
        function($scope, $route, Player, Level, LevelType, Task, Event) {
            $scope.tab = "players";
            $scope.entity = "Player";
            $scope.addLink = "player-add";
            $scope.rows;

            getActive();

            $scope.isActive = function (tab){
                return $scope.tab == tab;
            };

            $scope.selectTab = function(tab){
                switch(tab){
                    case 'players':
                        getPlayers();
                        break;
                    case 'levels':
                        getLevels();
                        break;
                    case 'level-types':
                        getLevelTypes();
                        break;
                    case 'tasks':
                        getTasks();
                        break;
                    case 'events':
                        getEvents();
                        break;
                }
                $scope.tab = tab;
            };

            $scope.remove = function(id) {
                switch($scope.tab){
                    case "players":
                        Player.remove({id: id});
                        getPlayers();
                        break;
                    case "levels":
                        Level.remove({id: id});
                        getLevels();
                        break;
                    case "level-types":
                        LevelType.remove({id: id});
                        getLevelTypes();
                        break;
                    case "tasks":
                        Task.remove({id: id});
                        getTasks();
                        break;
                    case "events":
                        Event.remove({id: id});
                        getEvents();
                        break;
                }
            }

            function getActive(){
                var param = $route.current.params;
                if(param["tab"]){
                    switch(param.tab){
                        case "players":
                            $scope.tab = "players";
                            getPlayers();
                            break;
                        case "levels":
                            $scope.tab = "levels";
                            getLevels();
                            break;
                        case "level-types":
                            $scope.tab = "level-types";
                            getLevelTypes();
                            break;
                        case "tasks":
                            $scope.tab = "tasks";
                            getTasks();
                            break;
                        case "events":
                            $scope.tab = "events";
                            getEvents();
                            break;
                        default:
                            $scope.tab = "players";
                            getPlayers();
                            break;
                    }
                } else {
                    $scope.tab = "players";
                    getPlayers();
                }
            };

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
                        task["view_url"] = "task-view/" + d.id;
                        task["edit_url"] = "task-edit/" + d.id;
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
                        event["skill_points"] = d.skill_points;
                        event["skill_interval"] = d.skill_interval;
                        event["skill_rule"] = d.skill_rule;
                        event["score_points"] = d.score_points;
                        event["score_interval"] = d.score_interval;
                        event["score_rule"] = d.score_rule;
                        event["view_url"] = "event-view/" + d.id;
                        event["edit_url"] = "event-edit/" + d.id;
                        events.push(event);
                    });
                });
                $scope.rows = events;
                $scope.entity = "Event";
                $scope.addLink = "event-add";
            };
    }])
    .controller("HistoryController", [
        "$scope", "$route", "LevelInstance", "Participation", "TriggeredEvent",
        function($scope, $route, LevelInstance, Participation, TriggeredEvent) {
            $scope.tab = "level-instance";
            $scope.entity = "Level Instance";
            $scope.rows;

            getActive();

            $scope.isActive = function (tab){
                return $scope.tab == tab;
            };

            $scope.selectTab = function(tab){
                switch(tab){
                    case 'level-instance':
                        getLevelInstances();
                        break;
                    case 'participations':
                        getParticipations();
                        break;
                    case 'triggered-events':
                        getTriggeredEvents();
                        break;
                }
                $scope.tab = tab;
            };

            function getActive(){
                var param = $route.current.params;
                if(param["tab"]){
                    switch(param.tab){
                        case "level-instances":
                            $scope.tab = "level-instances";
                            getLevelInstances();
                            break;
                        case "participations":
                            $scope.tab = "participations";
                            getParticipations();
                            break;
                        case "triggered-events":
                            $scope.tab = "triggered-events";
                            getTriggeredEvents();
                            break;
                        default:
                            $scope.tab = "level-instances";
                            getLevelInstances();
                            break;
                    }
                } else {
                    $scope.tab = "level-instances";
                    getLevelInstances();
                }
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
                        levelInstance["view_url"] = "level_instance-view/" + d.id;
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
                        participation["view_url"] = "participation-view/" + d.id;
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
                        triggeredEvent["given_skill_points"] = d.given_skill_points;
                        triggeredEvent["given_score_points"] = d.given_score_points;
                        triggeredEvent["view_url"] = "triggered_event-view/" + d.id;
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
    .controller("TaskAddEditController", [
        "$scope", "$routeParams", "$location", "Task",
        function($scope, $routeParams, $location, Task) {
            $scope.expected_values = ["id", "name", "description"];
            $scope.required_values = ["name"];
            $scope.unique_edit = "";
            $scope.name = "";
            $scope.description = "";
            $scope.uniques = [];
            $scope.customKeys = [];
            $scope.customValues = [];
            $scope.customRows = 0;

            getTaskNames();

            if ($routeParams.hasOwnProperty("id")){
                loadTask($routeParams.id);
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
                    Task.update({id:$routeParams.id}, data)
                } else {
                    Task.save(data);
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

            function getTaskNames() {
                Task.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        $scope.uniques.push(d.name);
                    });
                });
            };

            function loadTask(id) {
                Task.get({id: id}).$promise.then(function (data) {
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
    .controller("TaskViewController", [
        "$scope", "$routeParams", "$location", "Task",
        function($scope, $routeParams, $location, Task) {
            $scope.expected_values = ["id", "name", "description"];
            $scope.name = "";
            $scope.description = "";
            $scope.customValues = {};

            loadTask($routeParams.id);

            function loadTask(id) {
                Task.get({id: id}).$promise.then(function (data) {
                    var clone = {};
                    $scope.name = data.name;
                    $scope.description = data.description;
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
    .controller("EventAddEditController", [
        "$scope", "$routeParams", "$location", "Event", "Task",
        function($scope, $routeParams, $location, Event, Task) {
            $scope.expected_values = ["id", "tid", "name", "description",
                "skill_points", "skill_interval", "skill_rule",
                "score_points", "score_interval", "score_rule"];
            $scope.required_values = ["tid", "name"];
            $scope.unique_edit = "";
            $scope.tid = 0;
            $scope.name = "";
            $scope.description = "";
            $scope.skill_points = 0;
            $scope.skill_interval = 1;
            $scope.skill_rule = "";
            $scope.score_points = 0;
            $scope.score_interval = 1;
            $scope.score_rule = "";
            $scope.tasks = {};
            $scope.uniques = [];
            $scope.customKeys = [];
            $scope.customValues = [];
            $scope.customRows = 0;

            getTasks();
            getEventNames();

            if ($routeParams.hasOwnProperty("id")){
                loadEvent($routeParams.id);
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
                    "tid": $scope.tid,
                    "name": $scope.name,
                    "description": $scope.description,
                    "skill_points": $scope.skill_points,
                    "skill_interval": $scope.skill_interval,
                    "skill_rule": $scope.skill_rule,
                    "score_points": $scope.score_points,
                    "score_interval": $scope.score_interval,
                    "score_rule": $scope.score_rule,
                }
                for (var k in $scope.customKeys){
                    if($scope.customKeys.hasOwnProperty(k)){
                        data[$scope.customKeys[k].toLowerCase()] = $scope.customValues[k];
                    }
                }
                if($scope.unique_edit){
                    Event.update({id:$routeParams.id}, data)
                } else {
                    Event.save(data);
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

            function getTasks() {
                Task.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        $scope.tasks[d.id] = [d.name, d.description];
                    });
                });
            };

            function getEventNames() {
                Event.query().$promise.then(function (data) {
                    angular.forEach(data, function (d) {
                        $scope.uniques.push(d.name);
                    });
                });
            };

            function loadEvent(id) {
                Event.get({id: id}).$promise.then(function (data) {
                    var clone = {};
                    $scope.tid = data.tid;
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
    .controller("EventViewController", [
        "$scope", "$routeParams", "$location", "Event", "Task",
        function($scope, $routeParams, $location, Event, Task) {
            $scope.expected_values = ["id", "tid", "name", "description",
                "skill_points", "skill_interval", "skill_rule",
                "score_points", "score_interval", "score_rule"];
            $scope.task = "";
            $scope.name = "";
            $scope.description = "";
            $scope.skill_points = 0;
            $scope.skill_interval = 1;
            $scope.skill_rule = "";
            $scope.score_points = 0;
            $scope.score_interval = 1;
            $scope.score_rule = "";
            $scope.customValues = {};

            loadEvent($routeParams.id);

            function getTask(id) {
                Task.get({id: id}).$promise.then(function (data) {
                    $scope.task = data.name;
                });
            };

            function loadEvent(id) {
                Event.get({id: id}).$promise.then(function (data) {
                    var clone = {};
                    getTask(data.tid);
                    $scope.name = data.name;
                    $scope.description = data.description;
                    $scope.skill_points = data.skill_points;
                    $scope.skill_interval = data.skill_interval;
                    $scope.skill_rule = data.skill_rule;
                    $scope.score_points = data.score_points;
                    $scope.score_interval = data.score_interval;
                    $scope.score_rule = data.score_rule;
                    angular.copy(data, clone);
                    for (var key in RESOURCE_KEYS){
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
    .controller("LevelInstanceViewController", [
        "$scope", "$routeParams", "$location", "LevelInstance", "Level",
        function($scope, $routeParams, $location, LevelInstance, Level) {
            $scope.expected_values = ["id", "lid", "start_time", "end_time"];
            $scope.level = "";
            $scope.start_time = "";
            $scope.end_time = "";
            $scope.customValues = {};

            loadLevelInstance($routeParams.id);

            function getLevel(id) {
                Level.get({id: id}).$promise.then(function (data) {
                    $scope.level = data.name;
                });
            };

            function loadLevelInstance(id) {
                LevelInstance.get({id: id}).$promise.then(function (data) {
                    var clone = {};
                    getLevel(data.lid);
                    $scope.start_time = data.start_time;
                    $scope.end_time = data.end_time;
                    angular.copy(data, clone);
                    for (var key in RESOURCE_KEYS){
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
    .controller("ParticipationViewController", [
        "$scope", "$routeParams", "$location", "Participation",
        "Player", "LevelInstance", "Level",
        function($scope, $routeParams, $location, Participation,
                Player, LevelInstance, Level) {
            $scope.expected_values = ["id", "pid", "liid", "start_time", "end_time"];
            $scope.player = "";
            $scope.level = "";
            $scope.start_time = "";
            $scope.end_time = "";
            $scope.customValues = {};

            loadParticipation($routeParams.id);

            function getPlayer(id) {
                Player.get({id: id}).$promise.then(function (data) {
                    $scope.player = data.name;
                });
            };

            function getLevel(id) {
                LevelInstance.get({id: id}).$promise.then(function (data) {
                    var lid = data.lid;
                    Level.get({id: lid}).$promise.then(function (data) {
                        $scope.level = data.name;
                    });
                });
            };

            function loadParticipation(id) {
                Participation.get({id: id}).$promise.then(function (data) {
                    var clone = {};
                    getPlayer(data.pid);
                    getLevel(data.liid);
                    $scope.start_time = data.start_time;
                    $scope.end_time = data.end_time;
                    angular.copy(data, clone);
                    for (var key in RESOURCE_KEYS){
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
    .controller("TriggeredEventViewController", [
        "$scope", "$routeParams", "$location", "TriggeredEvent",
        "Participation", "Player", "LevelInstance", "Level", "Event",
        function($scope, $routeParams, $location, TriggeredEvent,
                Participation, Player, LevelInstance, Level, Event) {
            $scope.expected_values = ["id", "paid", "eid", "timestamp",
                "given_skill_points", "given_score_points"];
            $scope.player = "";
            $scope.level = "";
            $scope.event = "";
            $scope.timestamp = "";
            $scope.given_skill_points = 0;
            $scope.given_score_points = 0;
            $scope.customValues = {};

            loadTriggeredEvent($routeParams.id);

            function getParticipation(id) {
                Participation.get({id: id}).$promise.then(function (data) {
                    var pid = data.pid;
                    var liid = data.liid;
                    Player.get({id: pid}).$promise.then(function (data) {
                        $scope.player = data.name;
                    });
                    LevelInstance.get({id: liid}).$promise.then(function (data) {
                        var lid = data.lid;
                        Level.get({id: lid}).$promise.then(function (data) {
                            $scope.level = data.name;
                        });
                    });
                });
            };

            function getEvent(id) {
                Event.get({id: id}).$promise.then(function (data) {
                    $scope.event = data.name;
                });
            };

            function loadTriggeredEvent(id) {
                TriggeredEvent.get({id: id}).$promise.then(function (data) {
                    var clone = {};
                    getParticipation(data.paid);
                    getEvent(data.eid);
                    $scope.timestamp = data.timestamp;
                    $scope.given_skill_points = data.given_skill_points;
                    $scope.given_score_points = data.given_score_points;
                    angular.copy(data, clone);
                    for (var key in RESOURCE_KEYS){
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
;
