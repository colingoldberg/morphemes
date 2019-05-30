$.ajax({
    headers: {
        "Authorization": "Bearer be2d148ef09c15fabd960cac9e79de2d9ec1329a:",
        "Accept": "application/json"
    },
    dataType: "json",
    cache: false,
    url: 'http://162.243.39.95:8005/word_segments?word=abbreviated',
    success: function (data) {
        //console.log('Success:'+data);
        var $select = $('#results');
		$select.html('');
        alert(data);
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
