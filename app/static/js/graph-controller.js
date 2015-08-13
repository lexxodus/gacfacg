"use strict";



angular.module('graphController', ['angular-flot', 'directives'])
.controller('FlotController', [
    '$scope', "$q", "Player", "Level", "LevelType", "Task", "Event",
    "LevelSkill", "LevelTypeSkill", "TaskSkill", "EventSkill",
    function ($scope, $q, Player, Level, LevelType, Task, Event,
            LevelSkill, LevelTypeSkill, TaskSkill, EventSkill) {
        $scope.skillType = "level";
        $scope.interval = "timestamp"
        $scope.players = {};
        $scope.playersSelected = {};
        $scope.cntPlayersSelected = 0;
        $scope.levels = {};
        $scope.levelsSelected = {};
        $scope.levelTypes = {};
        $scope.levelTypesSelected = {};
        $scope.tasks = {};
        $scope.tasksSelected = {};
        $scope.events = {};
        $scope.eventsSelected = {};
        $scope.othersSelected = $scope.levelsSelected;
        $scope.cntOthersSelected = 0;
        $scope.sets = {};
        $scope.dataset = [];
        $scope.options = {
            xaxis: {
                mode: "time",
                timeformat: "%Y/%m/%d - %H:%M"
            },
            series: {
                lines: { show: true },
                points: { show: true }
            },
            grid: {
                hoverable: true
            },
            tooltip: {
                show: true,
                xDateFormat:"%Y/%m/%d - %H:%M:%S"
            }
        };

        $scope.selectSkill = function () {
            console.log($scope.skillType)
            switch($scope.skillType){
                case "level":
                    $scope.othersSelected = $scope.levelsSelected;
                    break;
                case "levelType":
                    $scope.othersSelected = $scope.levelTypesSelected;
                    break;
                case "task":
                    $scope.othersSelected = $scope.tasksSelected;
                    break;
                case "event":
                    $scope.othersSelected = $scope.eventsSelected;
                    break;
            }
            for(var oid in $scope.othersSelected){
                $scope.othersSelected[oid] = false;
            }
            $scope.cntOthersSelected = 0;
            redrawGraph();
        };

        $scope.selectPlayer = function (id) {
            if($scope.playersSelected[id]){
                $scope.cntPlayersSelected++;
                if($scope.othersSelected){
                    updateGraph(id, null);
                }
            } else {
                $scope.cntPlayersSelected--;
                redrawGraph();
            }
        };

        $scope.selectOther = function (id) {
            if($scope.othersSelected[id]){
                $scope.cntOthersSelected++;
                if($scope.cntPlayersSelected){
                    updateGraph(null, id);
                }
            } else {
                $scope.cntOthersSelected--;
                redrawGraph();
            }
        };

        $scope.selectXAxis = function(){
            var xaxis;
            if ($scope.interval == "timestamp"){
                xaxis = {
                    mode: "time",
                    timeformat: "%Y/%m/%d"
                };
            } else {
                xaxis = 1;
            }
            redrawGraph();
            $scope.options.xaxis = xaxis;
        };

        var playersPrep = getPlayers();
        var levelSkillPrep = $q.all([playersPrep, getLevels()]);
        var levelTypeSkillPrep = $q.all([playersPrep, getLevelTypes()]);
        var taskSkillPrep = $q.all([playersPrep, getTasks()]);
        var eventSkillPrep = $q.all([playersPrep, getEvents()]);

        levelSkillPrep.then(loadAllLevelSkills);
        levelTypeSkillPrep.then(loadAllLevelTypeSkills);
        taskSkillPrep.then(loadAllTaskSkills);
        eventSkillPrep.then(loadAllEventSkills);

        function loadAllLevelSkills(){
            for(var pid in $scope.players){
                if(!$scope.sets[pid]){
                    $scope.sets[pid] = {};
                }
                $scope.sets[pid]["level"] = {};
                for(var lid in $scope.levels){
                    $scope.sets[pid]["level"][lid] = {
                        attempt: [],
                        label: "",
                        timestamp: []
                    }
                    loadLevelSkillData(pid, lid)
                }
            }
        };

        function loadAllLevelTypeSkills(){
            for(var pid in $scope.players){
                if(!$scope.sets[pid]){
                    $scope.sets[pid] = {};
                }
                $scope.sets[pid]["levelType"] = {};
                for(var ltid in $scope.levelTypes){
                    $scope.sets[pid]["levelType"][ltid] = {
                        label: "",
                        timestamp: []
                    }
                    loadLevelTypeSkillData(pid, ltid)
                }
            }
        };

        function loadAllTaskSkills(){
            for(var pid in $scope.players){
                if(!$scope.sets[pid]){
                    $scope.sets[pid] = {};
                }
                $scope.sets[pid]["task"] = {};
                for(var tid in $scope.tasks){
                    $scope.sets[pid]["task"][tid] = {
                        label: "",
                        timestamp: []
                    }
                    loadTaskSkillData(pid, tid)
                }
            }
        };

        function loadAllEventSkills(){
            for(var pid in $scope.players){
                if(!$scope.sets[pid]){
                    $scope.sets[pid] = {};
                }
                $scope.sets[pid]["event"] = {};
                for(var eid in $scope.events){
                    $scope.sets[pid]["event"][eid] = {
                        label: "",
                        timestamp: []
                    }
                    loadEventSkillData(pid, eid)
                }
            }
        };

        function getPlayers(){
            var pid;
            var pname;
            var result = Player.query().$promise.then(function (data) {
                angular.forEach(data, function(d){
                    pid = d.id;
                    pname = d.name;
                    $scope.players[pid] = pname;
                    $scope.playersSelected[pid] = false;
                });
            });
            return result;
        };

        function getLevels(){
            var lid;
            var lname;
            var result = Level.query().$promise.then(function (data) {
                angular.forEach(data, function(d){
                    lid = d.id;
                    lname = d.name;
                    $scope.levels[lid] = lname;
                    $scope.levelsSelected[lid] = false;
                });
            });
            return result;
        };

        function getLevelTypes(){
            var ltid;
            var ltname;
            var result = LevelType.query().$promise.then(function (data) {
                angular.forEach(data, function(d){
                    ltid = d.id;
                    ltname = d.name;
                    $scope.levelTypes[ltid] = ltname;
                    $scope.levelTypesSelected[ltid] = false;
                });
            });
            return result;
        };

        function getTasks(){
            var tid;
            var tname;
            var result = Task.query().$promise.then(function (data) {
                angular.forEach(data, function(d){
                    tid = d.id;
                    tname = d.name;
                    $scope.tasks[tid] = tname;
                    $scope.tasksSelected[tid] = false;
                });
            });
            return result;
        };

        function getEvents(){
            var eid;
            var ename;
            var result = Event.query().$promise.then(function (data) {
                angular.forEach(data, function(d){
                    eid = d.id;
                    ename = d.name;
                    $scope.events[eid] = ename;
                    $scope.eventsSelected[eid] = false;
                });
            });
            return result;
        };

        function updateGraph(pid, oid) {
            if(pid){
                for(oid in $scope.othersSelected){
                    if($scope.othersSelected[oid]){
                        drawGraph($scope.sets[pid][$scope.skillType][oid]);
                    }
                }
            } else {
                for(pid in $scope.playersSelected){
                    if($scope.playersSelected[pid]){
                        console.log(pid);
                        console.log($scope.skillType);
                        drawGraph($scope.sets[pid][$scope.skillType][oid]);
                    }
                }
            }
        };

        function redrawGraph() {
            $scope.dataset = [];
            for(var pid in $scope.playersSelected){
                if($scope.playersSelected[pid]){
                    for(var oid in $scope.othersSelected){
                        if($scope.othersSelected[oid]){
                            drawGraph($scope.sets[pid][$scope.skillType][oid]);
                        }
                    }
                }
            }
        };

        function drawGraph (data){
            var xdata;
            if($scope.interval == "attempt"){
                xdata = data.attempt;
            } else {
                xdata = data.timestamp;
            }
            $scope.dataset.push(
                {
                    data: xdata,
                    label: data.label
                }
            );
        };

        function loadLevelSkillData(pid, lid){
            LevelSkill.query({pid:pid, lid:lid}).$promise.then(function (data){
                var dataByAttempt = [];
                var dataByTimeStamp = [];
                var timestamp;
                var attempt;
                var skill_points;
                var high_score;
                angular.forEach(data, function(d){
                    timestamp = isotimeToInt(d.calculated_on);
                    attempt = d.attempt;
                    skill_points = d.skill_points;
                    dataByAttempt.push([attempt, skill_points]);
                    dataByTimeStamp.push([timestamp, skill_points]);
                });
                $scope.sets[pid]["level"][lid].attempt = dataByAttempt;
                $scope.sets[pid]["level"][lid].timestamp = dataByTimeStamp;
                $scope.sets[pid]["level"][lid].label =
                    "Player: " + $scope.players[pid] + " - " +
                    "Level: " + $scope.levels[lid];
            });
        }

        function loadLevelTypeSkillData (pid, ltid){
           LevelTypeSkill.query({pid:pid, lid:ltid}).$promise.then(function (data){
                var dataByAttempt = [];
                var dataByTimeStamp = [];
                var timestamp;
                var skill_points;
                angular.forEach(data, function(d){
                    timestamp = isotimeToInt(d.calculated_on);
                    skill_points = d.skill_points;
                    dataByTimeStamp.push([timestamp, skill_points]);
                });
                $scope.sets[pid]["levelType"][ltid].timestamp = dataByTimeStamp;
                $scope.sets[pid]["levelType"][ltid].label =
                    "Player: " + $scope.players[pid] + " - " +
                    "Level Type: " + $scope.levelTypes[ltid];
            });
        };

        function loadTaskSkillData (pid, tid){
           TaskSkill.query({pid:pid, tid:tid}).$promise.then(function (data){
                var dataByAttempt = [];
                var dataByTimeStamp = [];
                var timestamp;
                var skill_points;
                angular.forEach(data, function(d){
                    timestamp = isotimeToInt(d.calculated_on);
                    skill_points = d.skill_points;
                    dataByTimeStamp.push([timestamp, skill_points]);
                });
                $scope.sets[pid]["task"][tid].timestamp = dataByTimeStamp;
                $scope.sets[pid]["task"][tid].label =
                    "Player: " + $scope.players[pid] + " - " +
                    "Task: " + $scope.tasks[tid];
            });
        };

        function loadEventSkillData (pid, eid){
           EventSkill.query({pid:pid, eid:eid}).$promise.then(function (data){
                var dataByAttempt = [];
                var dataByTimeStamp = [];
                var timestamp;
                var skill_points;
                angular.forEach(data, function(d){
                    timestamp = isotimeToInt(d.calculated_on);
                    skill_points = d.skill_points;
                    dataByTimeStamp.push([timestamp, skill_points]);
                });
                $scope.sets[pid]["event"][eid].timestamp = dataByTimeStamp;
                $scope.sets[pid]["event"][eid].label =
                    "Player: " + $scope.players[pid] + " - " +
                    "Task: " + $scope.events[eid];
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
  };

  $scope.onEventExampleClicked = function (event, pos, item) {
    console.log($scope.eventDataset);
    alert('Click! ' + event.timeStamp + ' ' + pos.pageX + ' ' + pos.pageY)
  };

  $scope.onEventExampleHover = function (event, pos, item) {
    console.log('Hover! ' + event.timeStamp + ' ' + pos.pageX + ' ' + pos.pageY)
  };
}])