var mainApp = angular.module("mainApp",[]);

mainApp.factory('dataService', function($http,$sce) {
	return {
		receiveData: function(category, params){
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
		},
		sendData: function(category, params){
			var URL=''
			switch(category) {
				case "article":
					console.log(params[0])
					URL = 'http://192.168.1.209/users/' + params[0] + '/articles/create'
					return $http({ method: 'POST', url: URL, 
												data: JSON.stringify({tag: params[1], text: params[2],csrfmiddlewaretoken: params[3]})
											}).success(function(){ console.log("abc") }).error( function(){ console.log("asdf")})
				case "comment":
					break;
			}	
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

		var pattern = [];
		var ret= '';

		// TODO : arrange
		// relative time
		if(t_info[0]<24) {
			ret += (t_info[0]>0 ? (t_info[0].toString()+'시간') : '');
			ret += (t_info[1]>0 ? (t_info[1].toString()+' 분') : '');
			ret += (t_info[1]==0 ? (t_info[2].toString()+' 초') : '');
			ret += '전';
					
			return ret;
		}

		// absolute time 
		if(cmp_year != t_info[0])
			pattern = [0,'년 ',1,'월 ',2,'일 ',(t_info[3]==1 ? '오후':'오전'),' ',4,'시 ',5,'분'];
		else
			pattern = [1,'월 ',2,'일 ',(t_info[3]==1 ? '오후':'오전'),' ',4,'시 ',5,'분'];

		for(var i=0; i<pattern.length; i++) {
			if(typeof(pattern[i])!="string") {
				console.log("log pattern[i]" + pattern[i]);
				ret += t_info[pattern[i]].toString();
			}
			else 
				ret += pattern[i];
		}

		return ret;
	}
	$scope.setProperTimeString = function(time) {
		var now = new Date();
		var tmp = new Date(time);
		var diff = new Date(now.valueOf() - tmp.valueOf());

		if( diff.valueOf() >= 86400 /* a Day */ ) 
			return $scope.createLocalTimeString("Han",$scope.createTimeInfo(tmp),now.getYear());
		return $scope.createLocalTimeString("Han",[diff/3600,(diff%3600)/60,diff%60]);
	}

	/* TODO : AJAX */
	$scope.createPost = function(user_id,token) {
		dataService.sendData("article",[user_id,$scope.tag,$scope.text,token])
		//.then(function(abc){ $scope.feeds.push({'name':"bc"}); })
	};

	$scope.getFeeds = function(st, ed) {

		if($scope.gettingFeeds) return;
		$scope.gettingFeeds = true;

		/* TODO : Processes with other parameter, combine user data */
		dataService.receiveData("newsfeed","user3@naver.com").then(function(resultData){

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

	$scope.getFeeds();

});
