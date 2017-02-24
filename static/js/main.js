var mainApp = angular.module("mainApp",[]);

mainApp.factory('dataService', function($http,$sce) {
	return {
		receiveData: function(category, params){
			var URL='';
			switch(category) {
				case "newsfeed":
					URL = 'http://192.168.1.208:3000/api/v1/users/'+params[0]+'/newsfeed'
					return $http({ method: 'GET', url: URL }).success( function(data){ return data; }).error( function(){ console.log("receiveData error"); });
				case "friend_request":
					URL = 'http://192.168.1.209/users/'+params[0]+'/friend_requests'
					break;
				case "friend_recommendation":
					URL = 'http://192.168.1.208:3000/api/v1/users/'+params[0]+'/friends'
					return $http({ method: 'GET', url: URL }).success( function(data){ return data; } ).error( function(){ console.log("receiveData error"); });
				case "comments":
					break;
				case "rec-nodes":
					break;
			}

			return $http({ method: 'GET', url: URL }).success( function(data){ return data; } ).error( function(){ console.log("receiveData error"); });
		},
		sendData: function(category, params){
			var URL=''
			switch(category) {
				case "article":
					URL = 'http://192.168.1.209/users/' + params[0] + '/articles/create'
					return $http({ method: 'POST', url: URL, 
					data: JSON.stringify({tag: params[1], text: params[2],csrfmiddlewaretoken: params[3]})
											}).success(function(data){ return data; }).error(function(){})
				case "friend_request_rep":
					URL = 'http://192.168.1.209/users/' + params[0] + '/friend_requests/' + params[1] + '/update'
					return $http({ method: 'POST', url: URL, 
					data: JSON.stringify({answer: params[2]})}).success(function(){}).error(function(){})
					break;
				case "friend_request_del":
					URL = 'http://192.168.1.209/users/' + params[0] + '/friend_requests/' + params[1] + '/delete'
					return $http({ method: 'DELETE', url: URL }).success(function(){}).error(function(){})
				case "comment":
					break;
			}	
		}
	}
});

mainApp.controller("mainController", function($scope, dataService) {

	$scope.feeds = [];
	$scope.friend_requests = [];
	$scope.friend_recommendation = [];
	$scope.gettingFeeds = false;
	$scope.user_id = "";

	$scope.createTimeInfo = function(date) {
		var t_info = [];
		date = new Date(date)
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
			if(t_info[0]==0 && t_info[1]==0) ret = "방금"
			ret += '전';
					
			return ret;
		}

		// absolute time 
		if(cmp_year != t_info[0])
			pattern = [0,'년 ',1,'월 ',2,'일 ',(t_info[3]==1 ? '오후':'오전'),' ',4,'시 ',5,'분'];
		else
			pattern = [1,'월 ',2,'일 ',(t_info[3]==1 ? '오후':'오전'),' ',4,'시 ',5,'분'];

		console.log(t_info)
		for(var i=0; i<pattern.length; i++) {
			if(typeof(pattern[i])!="string") {
				console.log(pattern[i])
				ret += t_info[pattern[i]].toString();
			}
			else 
				ret += pattern[i];
		}

		return ret;
	}

	$scope.setProperTimeString = function(time) {
		var now = new Date();
		var tmp = time;
		var diff = new Date(now.valueOf() - tmp.valueOf());
		diff = parseInt(diff.valueOf()/1000)
		if( diff >= 86400 /* a Day */ ) 
			return $scope.createLocalTimeString("Han",$scope.createTimeInfo(tmp),now.getYear());
	
		return $scope.createLocalTimeString("Han",[parseInt(diff/3600),parseInt((diff%3600)/60)]);
	}

	$scope.setUserId = function(user_id) {
		$scope.user_id = user_id;
		$scope.getFeeds();
		$scope.getFriendRequests();
		$scope.getFriendRecommendation();
	}

	$scope.createPost = function(user_name,user_img_url) {
		dataService.sendData("article",[$scope.user_id,$scope.tag,$scope.text,document.getElementsByName("csrfmiddlewaretoken")[0].value]).then(function(resultData){ 
																		$scope.feeds.unshift({'writer_name':user_name,
																										 'text':$scope.text,
										  															 'id':resultData.data.article_id,
																										 'tag':$scope.tag,
																										 'emotion':"기쁘메츔~~",
																										 'writer_image':user_img_url,
																										 'registered_time':new Date()}); 
																	},function(){
																	})
	};

	$scope.createComment = function(article_id, idx) {
		window.submitComment(article_id,idx);
	}

	$scope.getFriendRecommendation = function() {
		var cnt = 6 - $scope.friend_requests;
		if(cnt < 0) cnt = 3;
		dataService.receiveData("friend_recommendation",[$scope.user_id,cnt]).then(function(resultData){
			for(var i=0;i<resultData.data.length;i++)
				$scope.friend_recommendation.unshift(resultData.data[i])	
			console.log("debug",$scope.friend_recommendation)
		});
	}
	$scope.getFriendRequests = function() {
		dataService.receiveData("friend_request",[$scope.user_id]).then(function(resultData){
			for(var i=0;i<resultData.data.length;i++)
				$scope.friend_requests.push(resultData.data[i])
		});
  };

	$scope.deleteFriendRequest = function(request_id) {
		dataService.sendData("friend_request_del",[$scope.user_id, request_id]).then(function(){
			for(var i=0;i<$scope.friend_requests.length;i++) {
				if($scope.friend_requests[i].request_id == request_id)
					$scope.friend_requests.splice(i,1);	
			}
		})
	}
	$scope.replyFriendRequest = function(ans, request_id) {
		if(ans == "None")
			$scope.deleteFriendRequest(request_id);
		else {
		dataService.sendData("friend_request_rep",[$scope.user_id, request_id, ans]).then(function(){
				$scope.deleteFriendRequest(request_id)
			});
		}
	};

	$scope.getFeeds = function(st, ed) {
		console.log("asdf")
		if($scope.gettingFeeds) return;
		$scope.gettingFeeds = true; 

		/* TODO : Processes with other parameter, combine user data */
		dataService.receiveData("newsfeed",[$scope.user_id]).then(function(resultData){


			for(var i=0;i<resultData.data.length;i++)
			{
				var temp = new Date(resultData.data[i].registered_time);
				resultData.data[i].registered_time = temp.valueOf();
				$scope.feeds.push(resultData.data[i]);
			}


			$scope.gettingFeeds = false;
		});
	};

});
