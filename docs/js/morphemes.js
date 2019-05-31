
function getWordSegments() {
	var str = document.getElementById("word1").value;
	if (str.length == 0) { 
	    document.getElementById("results").innerHTML = "";
	    return;
	}
	ajaxGetWordSegments(str);
}

function ajaxGetWordSegments(word) {
	$.ajax({
    headers: {
        //"Authorization": "Bearer be2d148ef09c15fabd960cac9e79de2d9ec1329a:",
        "Accept": "application/json"
    },
    dataType: "json",
    cache: false,
    url: 'https://morphemes.ritc.io/word_segments?word=' + word,
    success: function (data) {
        //console.log('Success:'+data);
        document.getElementById("results").innerHTML = "\n<pre>\n" + JSON.stringify(data, undefined, 2) + "\n</pre>\n";
    },
    error: function(jqXHR,textStatus,errorThrown) {
        if (jqXHR.status === 401) {
            console.log("Unexpected 401 error:",jqXHR.status,textStatus);
         } else {
             console.log("Unexpected error:",jqXHR.status,textStatus);
         }
         alert('Error');
         //$select.html('<option id="-1">none available</option>');
    }
});
}