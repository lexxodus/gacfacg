"use strict";

angular.module('GACFACG', ["aPIServices", "controllers", "ngRoute"])
    .config(["$routeProvider", "$locationProvider",
            function($routeProvider, $locationProvider) {
            $routeProvider
            .when("/", {
                templateUrl: "static/views/entity.html",
                controller: "EntityController",
                controllerAs: "entity-ctl"
            })
            ;
            //.when("/history", {
            //    templateUrl: "static/views/history.html",
            //    controller: "HistoryController",
            //    controllerAs: "history"
            //})
            //.otherwise({
            //    redirectTo: "/entities"
            //})

            $locationProvider.html5Mode(true);
    }])
;
