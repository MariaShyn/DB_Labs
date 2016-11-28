(function(){
    'use strict';

    angular
        .module('db_lab_2')
        .controller("studentCtrl", [
            '$http',
            '$scope',
            function($http, $scope){

                $scope.getStudents = getStudents;
                $scope.searchPerson = searchPerson;

                $scope.getStudents();

                function getStudents() {
                    $http.get('/api/student')
                        .success(function(data){
                            $scope.students = data.students;
                            $scope.cities = data.cities;
                        })
                        .error(function(err){
                            alert(err);
                        });
                }

                function searchPerson() {
                    $http.get('/api/search?name=' + $scope.searchInput)
                        .success(function(data){
                            $scope.people = data;
                        })
                        .error(function(err){
                            alert(err);
                        });
                }

                function searchPerson() {
                    $http.get('/api/search?name=' + $scope.searchInput)
                        .success(function(data){
                            $scope.people = data;
                        })
                        .error(function(err){
                            alert(err);
                        });
                }
            }]);
}());
