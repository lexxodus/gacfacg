"use strict";

angular.module('GACFACG', ["aPIServices", "controllers", "ngRoute"])
    .config(["$routeProvider", "$locationProvider",
            function($routeProvider, $locationProvider) {
            $routeProvider
            .when("/", {
                templateUrl: "static/views/table.html",
                controller: "TableController",
                controllerAs: "table"
            })
            // .otherwise({
            //     redirectTo: "/"
            // })
            ;

            $locationProvider.html5Mode(true);
    }])
;
