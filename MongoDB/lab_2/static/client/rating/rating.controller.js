(function(){
    'use strict';

    angular
        .module('db_lab_2')
        .controller("ratingCtrl", [
            '$http',
            '$scope',
            function($http, $scope){

                $scope.getRating = getRating;
                $scope.getRating();
                $scope.count = 1;

                function getRating() {
                    $http.get('/api/rating')
                        .success(function(data){
                            $scope.schools = data.schools;
                            $scope.students = data.students;
                            console.log($scope.students)
                        })
                        .error(function(err){
                            alert(err);
                        });
                }
            }]);
}());
