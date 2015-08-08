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
                templateUrl: "static/views/player-add.html",
                controller: "PlayerAddController",
                controllerAs: "player-add-ctl"
            })
            .when("/level-add", {
                templateUrl: "static/views/level-add.html",
                controller: "LevelAddController",
                controllerAs: "level-add-ctl"
            })
            .otherwise({
                redirectTo: "/entities"
            })
            ;
            $locationProvider.html5Mode(true);
    }])
;
