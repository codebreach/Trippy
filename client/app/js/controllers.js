'use strict';

/* Controllers */


function MyCtrl1($scope, $http) {

  $http.jsonp('http://hidden-inlet-2627.herokuapp.com/place/NYC?callback=JSON_CALLBACK').
  success(function(data, status, headers, config){
    $scope.venues = data["venues"];
  }).
  error(function(data, status, headers, config) {

  });
}

function get_instagram_image($scope, $http){
  var instagram_client_id = "0790cbf24ff84eb2ab0f57660dacc016"
  var instagram_client_secret = "055b5b7661564c2197c0b92d1105bbb1"
  var instagram_id = 644104;
  $http.jsonp("https://api.instagram.com/v1/locations/search?foursquare_v2_id="+$scope.venue.id+"&client_id=0790cbf24ff84eb2ab0f57660dacc016&callback=JSON_CALLBACK").
  success(function(object, status, headers, config){
   // console.log(object["data"][0]["id"]);
    instagram_id = object["data"][0]["id"];
    console.log(instagram_id);

    $http.jsonp("https://api.instagram.com/v1/locations/"+instagram_id+"/media/recent?client_id=0790cbf24ff84eb2ab0f57660dacc016&callback=JSON_CALLBACK").
    success(function(object, status, headers, config){
      var url = object["data"][0]["images"]["standard_resolution"]["url"];
      $scope.img = url;
    }).
    error(function(data, status, headers, config) {

    });
    

  }).
  error(function(data, status, headers, config) {

  });
  console.log(instagram_id);


  
}

//MyCtrl1.$inject = [$scope, $http];


function MyCtrl2() {
}
MyCtrl2.$inject = [];
