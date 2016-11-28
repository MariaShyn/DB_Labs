'use strict';

var app = angular.module("db_lab_2",[
    "ui.router",
    "ui.bootstrap"
]);

app.config([
    "$locationProvider",
    "$stateProvider",
    "$httpProvider",
     function($locationProvider, $stateProvider, $httpProvider) {

        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $httpProvider.defaults.withCredentials = true;

        $stateProvider
            .state('main', {
                url: '',
                controller : ['$state',function($state){
                    $state.go('school');
                }]
            })
            .state('school', {
                url: '/school',
                controller: 'schoolCtrl',
                templateUrl: '/static/client/school/school.html'
            })
            .state('category', {
                url: '/category',
                controller: 'categoryCtrl',
                templateUrl: '/static/client/category/category.html'
            })
            .state('student', {
                url: '/student',
                controller: 'studentCtrl',
                templateUrl: '/static/client/student/student.html'
            })
            .state('exam', {
                url: '/exam',
                controller: 'examCtrl',
                templateUrl: '/static/client/exam/exam.html'
            })
            .state('rating', {
                url: '/rating',
                controller: 'ratingCtrl',
                templateUrl: '/static/client/rating/rating.html'
            });
}]);