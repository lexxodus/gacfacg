"use strict";

angular.module('aPIServices', ["ngResource"])
    .config(["$resourceProvider", function($resourceProvider) {
        // Don't strip trailing slashes from calculated URLs
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }])
    .factory("Player", ["$resource",
        function($resource){
        return $resource("worddomination1/api/player/:id", {}, {
            query: {
                method: "GET",
                params: {},
                isArray: false
            }
        });
    }])
;

