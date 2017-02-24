var str = ""

function search(type,user_id) {
	if(type == "t") {
		if( $('#search-input').val() == "" ) {
			console.log("asd")
			$('#search-result').empty()
			return;
		}
		var keyword = $('#search-input').val()
		var middle_word = $('#search-select').val()
	}
	else {
		var keyword = $('#asearch-input').val()
		var middle_word = "arture"
		var result_str="";
		result_str+="<div class='result'><button class='result-button' onclick="+'"location.assign('+"'"+'http://192.168.1.209/users/'+"')"+';"'+"><img class='result-img' src='http://192.168.1.209/media/" + "'><span class='result-name'>ewlkfj</span></button></div>"
		$('#asearch-result').empty()
		$('#asearch-result').append(result_str)
	}

	var URL = 'http://192.168.1.210/search/'+user_id+'/'+ middle_word +'/'+ keyword
	console.log(URL)
	if(str == URL) return;

	$.ajax({
		url:URL,
		type:'get',
		success:function(data) {
			var tt = type;
			var result_str="";
			data.forEach(function(result) {
				if(result.is_friend == "t") {
					result_str+="<div class='result'><button class='result-button' onclick="+'"location.assign('+"'"+'http://192.168.1.209/users/'+ result._id + "')"+';"'+"><img class='result-img' src='http://192.168.1.209/media/" + result.image + "'><span class='result-name'>" + result.name + "(친구)</span></button></div>"
				}
				else {
					result_str+="<div class='result'><button class='result-button' onclick="+'"location.assign('+"'"+'http://192.168.1.209/users/'+ result._id + "')"+';"'+"><img class='result-img' src='http://192.168.1.209/media/" + result.image + "'><span class='result-name'>" + result.name + "</span></button></div>"
				}
			})	
			if(tt == "t") {
				$('#search-result').empty()
				$('#search-result').append(result_str)
			}
			else {
				$('#asearch-result').empty()
				$('#asearch-result').append(result_str)
			}
			console.log(result_str);	
			str = URL;
		}
	})
}

