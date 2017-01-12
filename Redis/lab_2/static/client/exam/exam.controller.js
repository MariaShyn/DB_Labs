(function(){
    'use strict';

    angular
        .module('db_lab_2')
        .controller("examCtrl", [
            '$http',
            '$scope',
            '$timeout',
            function($http, $scope, $timeout){

                $scope.filteredExams = [],
                $scope.currentPage = 1,
                $scope.numPerPage = 100,
                $scope.maxSize = 5;
                $scope.searchStarted = false;

                $scope.getExams = getExams;
                $scope.removeExam = removeExam;
                $scope.startEditing = startEditing;
                $scope.updateExam = updateExam;
                $scope.ifPassed = false;
                $scope.passedOptions = ['true', 'false'];


                //pagination
                $scope.$watch("currentPage + numPerPage", updatefilteredItems)
                getExams();


                function updatefilteredItems(){
                    var begin = (($scope.currentPage - 1) * $scope.numPerPage),
                    end = begin + $scope.numPerPage;
                    $scope.filteredExams = $scope.exams.slice(begin, end);
                }


                function getExams() {
                    $scope.exams = [];
                    var url = '/api/exam';
                    $http.get(url)
                        .success(function(data){
                            $scope.exams = data.exams;
                            $scope.drivingSchools = data.drivingSchools;
                            updatefilteredItems();

                        })
                        .error(function(err){
                            alert(err);
                        });
                }


                function removeExam(id, index) {
                    if(typeof id === "object"){
                        id = id.$oid
                    }
                    $http.delete('/api/exam?id=' + id)
                        .success(function(){
                            $scope.filteredExams.splice(index, 1);
                            $scope.exams.length--;
                        })
                        .error(function(err){
                            console.error(err);
                        });
                }


                $scope.update = function(name){
                    var d1 = new Date();
                    var startTime = d1.getTime();
                    var url = '/api/search?name=' + name;
                    if(name) $scope.searchStarted = true;
                    $http.get(url)
                        .success(function(data){
                            $scope.exams = JSON.parse(data.exams);
                            var d2 = new Date();
                            var finishTime = d2.getTime();
                            $scope.searchTime = (finishTime - startTime) / 1000;
                            $scope.searchType = data.cash ? "Using cash" : "Without cash";
                            updatefilteredItems();
                        })
                        .error(function(err){
                            alert(err);
                        });
                 };

                function updateExam(index) {
                    var clearedData = angular.copy($scope.editedElem);
                    delete clearedData.listIndex;

                    $http.put('/api/exam', clearedData)
                        .success(function(){
                            $scope.exams[$scope.editedElem.listIndex] = clearedData;
                            $scope.editedElem = {};
                            $scope.detail.toggle = false;
                        })
                        .error(function(err){
                            console.error(err);
                        });
                }

                function startEditing(data, listIndex) {
                    $scope.editedElem = {
                        listIndex : listIndex,
                        id: data.id,
                        date : new Date(data.date),
                        category : data.category,
                        school : data.school,
                        person : data.person,
                        passed : data.passed
                    }
                }

           }]);
}());
