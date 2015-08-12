"use strict";



angular.module('graphController', ['angular-flot', 'directives'])
.controller('FlotController', [
    '$scope', "Player", "Level", "LevelSkill", "LevelTypeSkill",
    "TaskSkill", "EventSkill",
    function ($scope, Player, Level, LevelSkill, LevelTypeSkill,
            TaskSkill, EventSkill) {
        $scope.skillType = "level";
        $scope.interval = "timestamp";
        $scope.players = {};
        $scope.playersSelected = {};
        $scope.cntPlayersSelected = 0;
        $scope.cntLevelsSelected = 0;
        $scope.levels = {};
        $scope.levelsSelected = {};
        $scope.sets = {};
        $scope.dataset = [];
        $scope.options = {
            xaxis: {
                mode: "time",
                timeformat: "%Y/%m/%d"
            }
        };

        $scope.selectPlayer = function (id) {
            if($scope.playersSelected[id]){
                $scope.cntPlayersSelected++;
                if($scope.cntLevelsSelected){
                    updateGraph(id, null);
                }
            } else {
                $scope.cntPlayersSelected--;
                redrawGraph();
            }
        };

        $scope.selectLevel = function (id) {
            if($scope.levelsSelected[id]){
                $scope.cntLevelsSelected++;
                if($scope.cntPlayersSelected){
                    updateGraph(null, id);
                }
            } else {
                $scope.cntLevelsSelected--;
                redrawGraph();
            }
        };

        $scope.selectXAxis = function(){
            var xaxis;
            if ($scope.interval == "timestamp"){
                xaxis = {
                    mode: time,
                    timeformat: "%Y/%m/%d"
                };
            } else {
                xaxis = 1;
            }
            redrawGraph();
            $scope.options.xaxis = xaxis;
        };

        getPlayers();
        getLevels();

        function getPlayers(){
            var pid;
            var pname;
            Player.query().$promise.then(function (data) {
                angular.forEach(data, function(d){
                    pid = d.id;
                    pname = d.name;
                    $scope.players[pid] = pname;
                    $scope.playersSelected[pid] = false;
                });
            });
        };

        function getLevels(){
            var lid;
            var lname;
            Level.query().$promise.then(function (data) {
                angular.forEach(data, function(d){
                    lid = d.id;
                    lname = d.name;
                    $scope.levels[lid] = lname;
                    $scope.levelsSelected[lid] = false;
                });
            });
        };

        function updateGraph(pid, lid) {
            // if a player was selected
            if(pid){
                // if there are already sets for player
                if(!$scope.sets[pid]){
                    $scope.sets[pid] = {};
                }
                // for all currently selected levels
                for(lid in $scope.levelsSelected){
                    if($scope.levelsSelected[lid]){
                        // if there are already skilltype
                        if(!$scope.sets[pid][$scope.skillType]){
                            $scope.sets[pid][$scope.skillType] = {};
                        }
                        if(!$scope.sets[pid][$scope.skillType][lid]){
                            $scope.sets[pid][$scope.skillType][lid] = {
                                attempt: [],
                                timestamp: []
                            };
                            loadData(pid, lid);
                        } else {
                            drawLevelSkillGraph($scope.sets[pid][$scope.skillType][lid], pid, lid);
                        }
                    }
                }
            } else {
                for(pid in $scope.playersSelected){
                    if($scope.playersSelected[pid]){
                        if(!$scope.sets[pid]){
                            $scope.sets[pid] = {};
                        }
                        if(!$scope.sets[pid][$scope.skillType]){
                            $scope.sets[pid][$scope.skillType] = {};
                        }
                        if(!$scope.sets[pid][$scope.skillType][lid]){
                            $scope.sets[pid][$scope.skillType][lid] = {
                                attempt: [],
                                timestamp: []
                            };
                            loadData(pid, lid);
                        } else {
                            drawLevelSkillGraph($scope.sets[pid][$scope.skillType][lid], pid, lid);
                        }
                    }
                }
            }
        };

        function redrawGraph() {
            $scope.dataset = [];
            for(var pid in $scope.playersSelected){
                if($scope.playersSelected[pid]){
                    for(var lid in $scope.levelsSelected){
                        if($scope.levelsSelected[lid]){
                            drawLevelSkillGraph($scope.sets[pid][$scope.skillType][lid], pid, lid);
                        }
                    }
                }
            }
        };

        function drawGraph (data, label){
            var xdata;
            if($scope.interval == "attempt"){
                xdata = data.attempt;
            } else {
                xdata = data.timestamp;
            }
            $scope.dataset.push(
                {
                    data: xdata,
                    label:label
                }
            );
        }

        function drawLevelSkillGraph(data, pid, lid){
            var label =
                "Player: " + $scope.players[pid] + " - " +
                "Level: " + $scope.levels[lid];
            drawGraph(data, label);
        }

        function loadData (pid, lid){
            LevelSkill.query({pid:pid, lid:lid}).$promise.then(function (data){
                var dataByAttempt = [];
                var dataByTimeStamp = [];
                var timestamp;
                var attempt;
                var skill_points;
                angular.forEach(data, function(d){
                    timestamp = isotimeToInt(d.calculated_on);
                    attempt = d.attempt;
                    skill_points = d.skill_points;
                    dataByAttempt.push([attempt, skill_points]);
                    dataByTimeStamp.push([timestamp, skill_points]);
                });
                $scope.sets[pid][$scope.skillType][lid].attempt = dataByAttempt;
                $scope.sets[pid][$scope.skillType][lid].timestamp = dataByTimeStamp;
                drawLevelSkillGraph($scope.sets[pid][$scope.skillType][lid], pid, lid);
            });
        };

        function isotimeToInt(iso){
            return (new Date(iso)).getTime();
        };
//   //
//   // Standard Chart Example
//   //
//
//   $scope.dataset = [{ data: [], yaxis: 1, label: 'sin' }]
//   $scope.options = {
//     legend: {
//       container: '#legend',
//       show: true
//     }
//   }
//
//   for (var i = 0; i < 14; i += 0.5) {
//     $scope.dataset[0].data.push([i, Math.sin(i)])
//   }

  //
  // Categories Example
  //

  $scope.categoriesDataset = [[['January', 10], ['February', 8], ['March', 4], ['April', 13], ['May', 17], ['June', 9]]]
  $scope.categoriesOptions = {
    series: {
      bars: {
        show: true,
        barWidth: 0.6,
        align: 'center'
      }
    },
    xaxis: {
      mode: 'categories',
      tickLength: 0
    }
  }

  //
  // Pie Chart Example
  //

  $scope.pieDataset = []
  $scope.pieOptions = {
    series: {
      pie: {
        show: true
      }
    }
  }

  var pieSeries = Math.floor(Math.random() * 6) + 3

  for (var i = 0; i < pieSeries; i++) {
    $scope.pieDataset[i] = {
      label: 'Series' + (i + 1),
      data: Math.floor(Math.random() * 100) + 1
    }
  }

  //
  // Event example
  //

  $scope.eventDataset = angular.copy($scope.categoriesDataset)
  $scope.eventOptions = angular.copy($scope.categoriesOptions)
  $scope.eventOptions.grid = {
    clickable: true,
    hoverable: true
  }

  $scope.onEventExampleClicked = function (event, pos, item) {
    alert('Click! ' + event.timeStamp + ' ' + pos.pageX + ' ' + pos.pageY)
  }

  $scope.onEventExampleHover = function (event, pos, item) {
    console.log('Hover! ' + event.timeStamp + ' ' + pos.pageX + ' ' + pos.pageY)
  }
}])