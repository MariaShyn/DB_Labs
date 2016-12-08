(function(){
    'use strict';

    angular
        .module('db_lab_2')
        .controller("categoryCtrl", [
            '$http',
            '$scope',
            function($http, $scope){

                $scope.getCategories = getCategories;
                $scope.toggleCheckbox = toggleCheckbox;
                $scope.getCategories();

                $scope.searchCategories = [];

                function getCategories() {
                    var url = '/api/category';

                    if($scope.searchCategories && $scope.searchCategories.length) {
                        $http.post(url, $scope.searchCategories)
                            .success(function(data){
                                $scope.categories = data;
                            })
                            .error(function(err){
                                alert(err);
                            });
                    }else{
                        $http.get(url)
                            .success(function(data){
                                $scope.categories = data;
                                $scope.savedCategories = data;
                            })
                            .error(function(err){
                                alert(err);
                            });
                    }
                }

                function toggleCheckbox(category) {
                    var index = $scope.searchCategories.indexOf(category.id);
                    if(index > -1) {
                        $scope.searchCategories.splice(index, 1);
                    }else{
                        $scope.searchCategories.push(category.id);
                    }
                }

            }]);
}());