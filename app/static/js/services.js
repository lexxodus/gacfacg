"use strict";

angular.module('aPIServices', ["ngResource"])
    .config(["$resourceProvider", function($resourceProvider) {
        // Don't strip trailing slashes from calculated URLs
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }])
    .factory("Player", ["$resource",
        function($resource){
        return $resource("/api/player/:id");
    }])
    .factory("Level", ["$resource",
        function($resource){
        return $resource("/api/level/:id");
    }])
    .factory("LevelType", ["$resource",
        function($resource){
        return $resource("/api/level_type/:id");
    }])
    .factory("Task", ["$resource",
        function($resource){
        return $resource("/api/task/:id");
    }])
    .factory("Event", ["$resource",
        function($resource){
        return $resource("/api/event/:id");
    }])
;

