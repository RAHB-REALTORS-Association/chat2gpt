$("#userForm").submit(function(e) {
    e.preventDefault();
    const userInput = $("#userInput").val();
    const wrappedEventData = {
        "type": "MESSAGE",
        "user": { "name": "users/simulated" },
        "message": { "text": userInput }
    };
    $.ajax({
        url: "/post",
        type: "POST",
        data: JSON.stringify(wrappedEventData),
        contentType: "application/json",
        success: function(response) {
            // Handle the response
            const markdownText = response.text;
            const htmlFormattedText = marked.parse(markdownText);
            $("#formatted").html(htmlFormattedText);
            $("#raw").html('<pre>' + JSON.stringify(response, null, 2) + '</pre>');
        },              
        error: function(error) {
            // Handle the error
            $("#responseContainer").html("<h6>Response:</h6><pre>" + JSON.stringify(error, null, 2) + "</pre>");
        }
    });
});