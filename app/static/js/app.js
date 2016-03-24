"use strict";

angular.module('GACFACG', ["aPIServices", "controllers", "graphController", "ngRoute"])
    .config(["$routeProvider", "$locationProvider",
            function($routeProvider, $locationProvider) {
            $routeProvider
            .when("/entities", {
                templateUrl: "static/views/entity.html",
                controller: "EntityController",
                controllerAs: "entity-ctl"
            })
            .when("/histories", {
                templateUrl: "static/views/history.html",
                controller: "HistoryController",
                controllerAs: "history-ctl"
            })
            .when("/player-add", {
                templateUrl: "static/views/player-add-edit.html",
                controller: "PlayerAddEditController",
                controllerAs: "player-add-edit-ctl"
            })
            .when("/player-view/:id", {
                templateUrl: "static/views/player-view.html",
                controller: "PlayerViewController",
                controllerAs: "player-view-ctl"
            })
            .when("/player-edit/:id", {
                templateUrl: "static/views/player-add-edit.html",
                controller: "PlayerAddEditController",
                controllerAs: "player-add-edit-ctl"
            })
            .when("/level-add", {
                templateUrl: "static/views/level-add-edit.html",
                controller: "LevelAddEditController",
                controllerAs: "level-add-edit-ctl"
            })
            .when("/level-view/:id", {
                templateUrl: "static/views/level-view.html",
                controller: "LevelViewController",
                controllerAs: "level-view-ctl"
            })
            .when("/level-edit/:id", {
                templateUrl: "static/views/level-add-edit.html",
                controller: "LevelAddEditController",
                controllerAs: "level-add-edit-ctl"
            })
            .when("/level_type-add", {
                templateUrl: "static/views/level_type-add-edit.html",
                controller: "LevelTypeAddEditController",
                controllerAs: "level_type-add-edit-ctl"
            })
            .when("/level_type-view/:id", {
                templateUrl: "static/views/level_type-view.html",
                controller: "LevelTypeViewController",
                controllerAs: "level_type-view-ctl"
            })
            .when("/level_type-edit/:id", {
                templateUrl: "static/views/level_type-add-edit.html",
                controller: "LevelTypeAddEditController",
                controllerAs: "level_type-add-edit-ctl"
            })
            .when("/task-add", {
                templateUrl: "static/views/task-add-edit.html",
                controller: "TaskAddEditController",
                controllerAs: "task-add-edit-ctl"
            })
            .when("/task-view/:id", {
                templateUrl: "static/views/task-view.html",
                controller: "TaskViewController",
                controllerAs: "task-view-ctl"
            })
            .when("/task-edit/:id", {
                templateUrl: "static/views/task-add-edit.html",
                controller: "TaskAddEditController",
                controllerAs: "task-add-edit-ctl"
            })
            .when("/event-add", {
                templateUrl: "static/views/event-add-edit.html",
                controller: "EventAddEditController",
                controllerAs: "event-add-edit-ctl"
            })
            .when("/event-view/:id", {
                templateUrl: "static/views/event-view.html",
                controller: "EventViewController",
                controllerAs: "event-view-ctl"
            })
            .when("/event-edit/:id", {
                templateUrl: "static/views/event-add-edit.html",
                controller: "EventAddEditController",
                controllerAs: "event-add-edit-ctl"
            })
            .when("/level_instance-view/:id", {
                templateUrl: "static/views/level_instance-view.html",
                controller: "LevelInstanceViewController",
                controllerAs: "level_instance-view-ctl"
            })
            .when("/participation-view/:id", {
                templateUrl: "static/views/participation-view.html",
                controller: "ParticipationViewController",
                controllerAs: "participation-view-ctl"
            })
            .when("/triggered_event-view/:id", {
                templateUrl: "static/views/triggered_event-view.html",
                controller: "TriggeredEventViewController",
                controllerAs: "triggered_event-view-ctl"
            })
            .when("/graphs", {
                templateUrl: "static/views/graph.html",
                controller: "FlotController",
                controllerAs: "flot-ctl"
            })
            .when("/data-export", {
                redirectTo: "/data-export"
            })
            .otherwise({
                redirectTo: "/entities"
            })
            ;
            $locationProvider.html5Mode(true);
    }])
;
