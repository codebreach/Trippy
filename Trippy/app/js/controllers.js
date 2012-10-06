'use strict';

/* Controllers */


function MyCtrl1($scope, $http) {
	$http.get('venues/venues.json').success(function(data) {
		console.log(data);
   	 	$scope.venues = data;
   	 	$scope.location = "Vegas";
  	});

}

function setBackgroundImage($scope){
	var image = $scope.venue.img;
	console.log(image);

	$scope.mystyle = {
        "background":"red",
        "backgroundImage":"url("+image+")",
        "backgroundSize":"220px 220px"

    };
}

//MyCtrl1.$inject = [$scope, $http];


function MyCtrl2() {
}
MyCtrl2.$inject = [];
