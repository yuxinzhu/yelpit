$(document).ready(function() {
    console.log('Yelp It Extension Attack!');
    /* hardcoding for the win */
    // var imageURL = 'http://s3-media4.fl.yelpcdn.com/assets/2/www/img/9f83790ff7f6/ico/stars/v1/stars_large_4_half.png';
    // var categories = ['Sandwiches', 'American'];
    // var phoneNumber = "(510) 923 9233";
    // var url = "http://www.yelp.com/biz/brazil-fresh-squeeze-cafe-berkeley";
    var maxQueryLength = 5;

    var _popupHTML = function(phoneNumber, imageURL, ratingCount, url, categories, location) {
        var formattedPhoneNumber = '(' + phoneNumber.substr(0, 3) + ') ' + phoneNumber.substr(3, 3) + '-' + phoneNumber.substr(6,4);
        var html = "" + 
        "<div class='yelp-it-container'>" + 
            "<div class='header'><span class='yelp-it-business-name' data-notify-html='businessName'></span><a href='tel:" + phoneNumber + "' class='yelp-it-phone-number'>" + formattedPhoneNumber + "</a></div>" + 
            "<div class='yelp-it-business-rating'><img src='" + imageURL + "'></img><a target='_blank' href='" + url + "' class='rating-count'>" + ratingCount + " reviews </a></div>" + 
            "<div class='yelp-it-category-container'>";

        $(categories).each(function(index, element) {
            html += "<span class='category'>" + element[0] + "</span>";
        }); 
        html += "</div>";

        html += "<div class='yelp-it-address'>" + location + "</div>";
        html += "</div>";
        return html;
    };

    
    var saveURLKeyToLocalStorage = function(url) {
        /* save url to localStorage as key:Object */
    }
    
    var saveResponseKeyValueToLocalStorage = function(key, value) {
        /* save key:value response to localStorage business_name:jsonAPIResponse */
    }

    var showPopUp = function(json) {
        console.log(json.result);
        if (json == null || json.result == null) {
            return;
        }
        var business = json.result;
        $.notify.addStyle("yelpit", 
            {
                html: _popupHTML(business['phone'], 
                business['rating_img_url_large'], 
                business['review_count'], 
                business['url'],
                business['categories'],
                business['location']['city'])
            });

        $.notify({
          businessName: business['name'],
        }, { 
          style: 'yelpit',
          autoHide: true,
          clickToHide: true
        });
    };

    var request = function(query) {
        if (xhr != null) {
            xhr.abort();
        }

        var formData = {body: $("html").html(), target: String(query), url: document.URL};
        console.log(formData);
        var xhr = $.ajax({
            "url": "http://localhost:5000/rating",
            "data": formData,
            "success": showPopUp,
            "type": "POST",
            "dataType": "json"
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
        if(st!='') {
            var queryLength = st.toString().split(/\s+/).length;
            if (queryLength < maxQueryLength) {
                request(st);
            }
        }
    }

    $(document).ready(function(){
      $(document).bind("mouseup", highlightMouseup);
    });
});

