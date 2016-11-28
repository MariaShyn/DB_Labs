(function(){
    'use strict';

    angular
        .module('db_lab_2')
        .controller("examCtrl", [
            '$http',
            '$scope',
            '$timeout',
            function($http, $scope, $timeout){

                $scope.getExams = getExams;
                $scope.removeExam = removeExam;
                $scope.addNewExam = addNewExam;
                $scope.startEditing = startEditing;
                $scope.updateExam = updateExam;
                $scope.ifPassed = false;
                $scope.passedOptions = ['true', 'false'];
                $scope.getExams();

                function getExams(passed) {
                    var url = '/api/exam';
                    if(passed !== undefined) {
                        url += '?passed='+passed
                    }
                    $http.get(url)
                        .success(function(data){
                            $scope.exams = data.exams;
                            $scope.people = data.people;
                            $scope.drivingSchools = data.drivingSchools;
                            $scope.categories = data.categories;
                        })
                        .error(function(err){
                            alert(err);
                        });
                }

                function removeExam(date, name, index) {
                    $http.delete('/api/exam?date=' + date + '&name=' + name)
                        .success(function(){
                            $scope.exams.splice(index, 1);
                        })
                        .error(function(err){
                            console.error(err);
                        });
                }

                $scope.getList = function(){
                    return $scope.exams;
                }

                function addNewExam() {
                    $http.post('/api/exam', $scope.newExam)
                        .success(function(){
                            $scope.exams.push({
                                date : $scope.newExam.date,
                                category : $scope.newExam.category,
                                person : $scope.newExam.person,
                                school: $scope.newExam.school,
                                passed : $scope.newExam.passed
                            })
                            $scope.newExam.date = '';
                            $scope.newExam.category = '';
                            $scope.newExam.person = '';
                            $scope.newExam.school = '';
                            $scope.newExam.passed = '';

                        })
                        .error(function(err){
                            console.error(err);
                        })
                        .finally(function(){
                            $timeout(function(){
                                $scope.$apply();
                            })
                        })
                }

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
