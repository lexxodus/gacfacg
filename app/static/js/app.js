"use strict";

angular.module('GACFACG', ["aPIServices", "controllers", "ngRoute"])
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
            .otherwise({
                redirectTo: "/entities"
            })
            ;
            $locationProvider.html5Mode(true);
    }])
;
