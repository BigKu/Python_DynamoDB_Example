var app = angular.module('myApp', []);

app.controller('myCtrl', function($scope, $http) {
    $http.get('memos').then(function(response){
      console.log(response.data);
        $scope.items = response.data;
      console.log($scope.items);
    }, function(response){
        console.log("ERROR: GET /memos");
    });
});
