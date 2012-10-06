'use strict';

/* Controllers */


function MyCtrl1($scope, $http) {

  $http.jsonp('http://hidden-inlet-2627.herokuapp.com/place/NYC?callback=JSON_CALLBACK').
  success(function(data, status, headers, config){
    console.log(data)
    $scope.venues = data["venues"];
    console.log("Status " + status);
  }).
  error(function(data, status, headers, config) {

  });

//	$http.get('venues/venues.json').success(function(data) {
//   	 	$scope.venues = data;
//   	 	$scope.location = "Vegas";
//  	});

}

function get_instagram_image($scope, $http){
  var instagram_client_id = "0790cbf24ff84eb2ab0f57660dacc016"
  var instagram_client_secret = "055b5b7661564c2197c0b92d1105bbb1"
  var id = 644104;
  $http.jsonp("https://api.instagram.com/v1/locations/"+id+"/media/recent?client_id=0790cbf24ff84eb2ab0f57660dacc016&callback=JSON_CALLBACK").
  success(function(object, status, headers, config){
    var url = object["data"][0]["images"]["standard_resolution"]["url"];
    console.log(url);
    $scope.img = url;
  }).
  error(function(data, status, headers, config) {

  });
}

//MyCtrl1.$inject = [$scope, $http];


function MyCtrl2() {
}
MyCtrl2.$inject = [];
