var mainApp = angular.module("mainApp",[]);

mainApp.factory('dataService', function($http,$sce) {
	return {
		getData: function(category, params){
			var URL='';
			switch(category) {
				case "newsfeed":
					URL = 'http://192.168.1.208:3000/main/users/'+params[0]+'/articles'
					break;
				case "comments":
					break;
				case "rec-friends":
					break;
				case "rec-nodes":
					break;
			}

			return $http({ method: 'GET', url: URL }).success( function(data){ return data; } ).error( function(){ console.log("getData error"); });
		}
	}
});

mainApp.controller("mainController", function($scope, dataService) {

	$scope.feeds = [];
	$scope.gettingFeeds = false;

	$scope.createTimeInfo = function(date) {
		var t_info = [];
		t_info[6] = date.getSeconds();
		t_info[5] = date.getMinutes();
		t_info[3] = (date.getHours()>=12 ? 1 : 0);
		t_info[4] = (date.getHours()%12==0) ? 12 : date.getHours()%12;
		t_info[2] = date.getDay();
		t_info[1] = date.getMonth()+1;
		t_info[0] = date.getYear();

		return t_info;
	}
	
	$scope.createLocalTimeString = function(lang, t_info, cmp_year) {
		// It only supports Hangul and English.
		// pattern is consist of 0:year, 1:month, 2:day, 3:pm and am, 4:hour, 5:minute and 6:second additional character

		var pattern = [];
		var ret= '';

		// TODO : arrange
		// relative time
		if(t_info[0]<24) {
			switch(lang) {
				case "Han":
					ret += (t_info[0]>0 ? (t_info[0].toString()+'시간') : '');
					ret += (t_info[1]>0 ? (t_info[1].toString()+' 분') : '');
					ret += (t_info[1]==0 ? (t_info[2].toString()+' 초') : '');
					ret += '전';
					break;
				case "Eng":
					ret += (t_info[0]>0 ? (t_info[0].toString()+'hrs') : '');
					ret += (t_info[1]>0 ? (t_info[1].toString()+' min') : '');
					ret += (t_info[1]==0 ? (t_info[2].toString()+' sec') : '');
					ret += 'ago';
					break;	
			}

			return ret;
		}

		// absolute time 
		if(cmp_year != t_info[0])
		{
			switch(lang) {
				case "Han":
					pattern = [0,'년 ',1,'월 ',2,'일 ',(t_info[3]==1 ? '오후':'오전'),' ',4,'시 ',5,'분'];
					break;
				case "Eng":
				default:
					pattern = [1,' ',2,', ',0,' at ',4,':',5,(t_info[3]==1 ? 'am':'pm')];
					break;
				
			}
		}
		else
		{
			switch(lang) {
				case "Han":
					pattern = [1,'월 ',2,'일 ',(t_info[3]==1 ? '오후':'오전'),' ',4,'시 ',5,'분'];
					break;
				case "Eng":
				default:
					pattern = [1,' ',2,' at ',4,':',5,(t_info[3]==1 ? 'am':'pm')];
					break;
			}
		}

		for(var i=0; i<pattern.length; i++) {
			if(typeof(pattern[i])!="string") {
				console.log("log pattern[i]" + pattern[i]);
				ret += t_info[pattern[i]].toString();
			}
			else {
				ret += pattern[i];
			}
		}

		return ret;
	}
	$scope.setProperTimeString = function(time) {
		var now = new Date();
		var tmp = new Date(time);
		var diff = new Date(now.valueOf() - tmp.valueOf());

		if( diff.valueOf() >= 86400 /* a Day */ ) {
			return $scope.createLocalTimeString("Han",$scope.createTimeInfo(tmp),now.getYear());
		}
		return $scope.createLocalTimeString("Han",[diff/3600,(diff%3600)/60,diff%60]);
	}

	/* TODO : AJAX */
	$scope.createPost = function() {
		$scope.feeds.push({'name':"bc"});
	};

	$scope.getFeeds = function(st, ed) {

		if($scope.gettingFeeds) return;
		$scope.gettingFeeds = true;

		/* TODO : Processes with other parameter, combine user data */
		dataService.getData("newsfeed","user3@naver.com").then(function(resultData){

			for(var i=resultData.data.length-1;i>=0;i--)
			{
				var temp = new Date(resultData.data[i].reg_time);
				resultData.data[i].reg_time = temp.valueOf();

				$scope.feeds.push(resultData.data[i]);
			}

			$scope.gettingFeeds = false;
			console.log($scope.feeds.length);
		});
	};

	// XXX Trick..! Maybe have to check Element Ready.
	$scope.getFeeds();

});
