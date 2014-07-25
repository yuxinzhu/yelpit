$(document).ready(function() {
	console.log('Welcome to the Yelp It Extension');
	var $pageText = $('body').text();
	var $target = 'Gary Danko';
	
	var showPopUp = function(json) {
		console.log('response');
		console.log(json);
	};

	var request = function(target) {
		$.ajax({
			url: "http://localhost:5000/rating",
			data: {'body': $pageText, 'target': $target},
			success: showPopUp,
			type: "POST",
			dataType: "json"
		});
	}

	var getSelected = function(){
	  var t = '';
	  if(window.getSelection){
	    t = window.getSelection();
	  }else if(document.getSelection){
	    t = document.getSelection();
	  }else if(document.selection){
	    t = document.selection.createRange().text;
	  }
	  return t;
	}

	var highlightMouseup = function(){
	  var st = getSelected();
	  if(st!=''){
	    console.log("You selected:\n"+st);
	  }
	}

	$(document).ready(function(){
	  $(document).bind("mouseup", highlightMouseup);
	});
});

