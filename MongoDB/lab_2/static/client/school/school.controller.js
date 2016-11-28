(function(){
    'use strict';

    angular
        .module('db_lab_2')
        .controller("schoolCtrl", [
            '$http',
            '$scope',
            function($http, $scope){

                $scope.getSchools = getSchools;
                $scope.fillDB = fillDB;
                $scope.getSchools();

                function getSchools() {
                    $http.get('/api/school')
                        .success(function(data){
                            $scope.schools = data;
                        })
                        .error(function(err){
                            alert(err);
                        });
                }

                function fillDB() {
                    $http.get('/api/db')
                        .success(function(){
                        })
                        .error(function(err){
                            alert(err);
                        });
                }


            }]);
}());
