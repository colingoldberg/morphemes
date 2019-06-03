
var lastWord = ""

function getWordSegments() {
	var str = document.getElementById("word1").value;
	if (str.length == 0) { 
	    document.getElementById("results").innerHTML = "";
        document.getElementById("result_buttons").innerHTML = "";
        document.getElementById("report_makes_sense").innerHTML = "";
        lastWord = "";
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
        lastWord = word;
        document.getElementById("results").innerHTML = "\n<pre>\n" + JSON.stringify(data, undefined, 2) + "\n</pre>\n";
        buttonsHtml = "<button type=\"button\" onclick=\"ajaxReportResult(true)\">Result Makes Sense</button><br />"
                    + "<button type=\"button\" onclick=\"ajaxReportResult(false)\">Result Does Not Make Sense</button>"
        document.getElementById("result_buttons").innerHTML = buttonsHtml;
        document.getElementById("report_makes_sense").innerHTML = "";
    },
    error: function(jqXHR,textStatus,errorThrown) {
        if (jqXHR.status === 401) {
            console.log("Unexpected 401 error:",jqXHR.status,textStatus);
         } else {
             console.log("Unexpected error:",jqXHR.status,textStatus);
         }
         console.log('Error:'+data);
         document.getElementById("report_makes_sense").innerHTML = "A system error occurred";
         lastWord = "";
    }
});
}

function ajaxReportResult(ok) {
    $.ajax({
    headers: {
        //"Authorization": "Bearer be2d148ef09c15fabd960cac9e79de2d9ec1329a:",
        "Accept": "application/json"
    },
    dataType: "json",
    cache: false,
    url: 'https://morphemes.ritc.io/report_result?word=' + lastWord + '&ok=' + ok,
    success: function (data) {
        console.log('Success:'+data);
        document.getElementById("report_makes_sense").innerHTML = "Your assessment has been reported";
        lastWord = "";
    },
    error: function(jqXHR,textStatus,errorThrown) {
        if (jqXHR.status === 401) {
            console.log("Unexpected 401 error:",jqXHR.status,textStatus);
         } else {
             console.log("Unexpected error:",jqXHR.status,textStatus);
         }
         console.log('Error:'+data);
         document.getElementById("report_makes_sense").innerHTML = "A system error occurred";
         lastWord = "";
    }
});
}
