// Close button for the tweets overlay
$('#close_button').click(function () {
    // document.getElementById("tweets_overlay").style.display = 'none';
    $("#tweets_overlay").toggle();
});
// When a trend button is clicked, make an AJAX request to the server to get the tweets
const get_tweets = e => {
    // console.log($(this).data("query"));
    console.log(e.dataset.query);
    let tweetsArea = $("#tweetsArea");
    let trendTitle = $("#trendTitle");
    trendTitle.text("");
    // document.getElementById("tweets_overlay").style.display = 'block';
    $("#tweets_overlay").toggle();
    tweetsArea.empty();
    $("#tweetSpinner").append(`
        <div class="spinner-grow text-primary" role="status">
            <span class="sr-only">Loading...</span>
        </div>
    `);

    $.ajax({
        url: 'ajax/tweets',
        data: {
        'q': e.dataset.query,
        },
        dataType: 'json',
        success: function (data) {
            tweetsArea.empty();
            $("#tweetSpinner").empty();


            let result = data["result"];
            let title = e.dataset.query;
            let searchUrl = e.dataset.url;
            trendTitle.append(`<a class="text-decoration-none text-info" href=${searchUrl}>${title}</a>`);
            console.log(data);

            let i;
            for (i=0; i < data.result.length; i++) {
                tweetsArea.append(`
                <div class="card">${result[i]}</div>
                `);
                
            };
        }
    });
};
// Get the trends for a location when a location button is clicked
$('.locationButton').click(function () {
    console.log($(this).data("woeid"));
    let trendsArea = $("#trendsArea");
    $("#locationTitle").text(`${$(this).data("name")} Trends`);
    trendsArea.empty();
    $("#trendSpinner").append(`
        <div class="spinner-grow text-primary" role="status">
            <span class="sr-only">Loading...</span>
        </div>
    `);
    $.ajax({
        url: 'ajax/trends',
        data: {
        'woeid': $(this).data("woeid"),
        },
        dataType: 'json',
        success: function (data) {
            trendsArea.empty();
            $("#trendSpinner").empty();

            let result = data["result"];
            console.log(data);

            let i;
            for (i=0; i < data.result.length; i++) {
                trendsArea.append(`
                    <button type="button" class="btn btn-info btn-lg m-2 trendButton" onclick='get_tweets(this)' data-query="${result[i][0]}" data-url="${result[i][2]}">
                        ${result[i][0]} <span class="badge badge-secondary">${result[i][1]}</span>
                        <span class="sr-only">unread messages</span>
                    </button>
                `);
            };
        }
    });
});