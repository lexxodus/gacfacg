"use strict";

angular.module('aPIServices', ["ngResource"])
    .config(["$resourceProvider", function($resourceProvider) {
        // Don't strip trailing slashes from calculated URLs
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }])
    .factory("Player", ["$resource",
        function($resource){
           return $resource("/api/player/:id", null,
           {
                "update": { method:"PUT"}
           });
    }])
    .factory("Level", ["$resource",
        function($resource){
           return $resource("/api/level/:id", null,
           {
                "update": { method:"PUT"}
           });
    }])
    .factory("LevelType", ["$resource",
        function($resource){
            return $resource("/api/level_type/:id", null,
           {
                "update": { method:"PUT"}
           });
    }])
    .factory("Task", ["$resource",
        function($resource){
            return $resource("/api/task/:id", null,
           {
                "update": { method:"PUT"}
           });
    }])
    .factory("Event", ["$resource",
        function($resource){
            return $resource("/api/event/:id", null,
           {
                "update": { method:"PUT"}
           });
    }])
    .factory("LevelInstance", ["$resource",
        function($resource){
            return $resource("/api/level_instance/:id");
    }])
    .factory("Participation", ["$resource",
        function($resource){
            return $resource("/api/participation/:id");
    }])
    .factory("TriggeredEvent", ["$resource",
        function($resource){
            return $resource("/api/triggered_event/:id");
    }])
    .factory("LevelSkill", ["$resource",
        function($resource){
            return $resource("/api/level_skill/:id");
    }])
    .factory("LevelTypeSkill", ["$resource",
        function($resource){
            return $resource("/api/level_type_skill/:id");
    }])
    .factory("TaskSkill", ["$resource",
        function($resource){
            return $resource("/api/task_skill/:id");
    }])
    .factory("EventSkill", ["$resource",
        function($resource){
            return $resource("/api/event_skill/:id");
    }])
;

