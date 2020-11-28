 $(document).ready(function(e){
    $('.search-panel .dropdown-genre').find('a').click(function(e) {
        e.preventDefault();
		var param = $(this).attr("href").replace("#","");
		var genre = $(this).text();
		$('.search-panel span#genreButton').text(genre);
	});
    $("#submitButton").click(function(e){
        e.preventDefault();
        var genre = $('.search-panel span#genreButton').text();
        var movie = $('#search').val();
        var director = $('#searchDirector').val();
        var actor = $('#searchActor').val();
        
        var jsonObj = {
            "genre" : genre,
            "movie" : movie,
            "director" : director,
            "actor" : actor
        }
        
        console.log(JSON.stringify(jsonObj));
        
        $.ajax({
    		type :'GET',
    		url  : "/result",
    		contentType : "application/json",
    		data : jsonObj,
    		crossDomain : true,
    		success : function (result){
        		var parsed_result = JSON.parse(result);
        		var list = parsed_result.res;
        		$("table tbody").empty();
        		for (var i = 0; i < list.length; i++) {
            		markup = "<tr>";
                	for (var j = 0; j < 10; j++) {
                    	markup += "<td>";
                    	markup += list[i][j];
                    	markup += "</td>";
                	}
                	markup += "</tr>";
                	var tableBody = $("table tbody");
                	console.log(markup);
                    tableBody.append(markup);
        		}
    		},
    		error: function(xhr,textstatus,error)
    		{
    			var eval = JSON.parse(xhr.responseText);
    			alert("Error :"+"\n"+eval.code+"\n"+eval.status+"\n"+eval.description);
    		}
    	});
    });
});