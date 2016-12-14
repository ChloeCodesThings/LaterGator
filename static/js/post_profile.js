$(document).ready(function(){

    $("#userpost").on('input', function() {
        if ($(this).val().length>=140) {
            alert('Oops! Remember- Facebook has a 63,206 character limit!');
         }
         
    $('#remaining_chars').html("Remaining characters : " + (63206 - this.value.length));

     });

    var current_time = moment().format("h:mm a");

    $('#time_right_now').html(current_time);

    function changedTime() {
         // time_from_textbox is whatever they typed in
        var time_from_textbox = $('#time_textbox').val();
        console.log('time_from_textbox', time_from_textbox);

        // Parsed chrono date (chrono.parseDate(x))
        var chrono_time = chrono.parseDate(time_from_textbox);
        console.log('chrono_time', chrono_time);

        // format that to the value we want to actually send to facebook (seconds epoch value)
        var moment_time = moment(chrono_time);
        console.log('moment_time', moment_time);

        var moment_unix = moment_time.format('X');

        var timezone = moment_time.format('zz');

        var current_time_unix = current_time.format('X');

        var value_check = moment_unix - current_time_unix;

        console.log(value_check);

        console.log(timezone);
        console.log(moment_unix);
        console.log(current_time_unix);

        if (value_check <= 600) {
            alert("You must post at least 10 minutes from now!");
        } else if (value_check >= 5184000) {
            alert("You cannot post more than 60 days ahead of time!");
        }

        // setting our final time value (seconds since the epoch) to our hidden input
        $('#hidden_time').val(moment_unix);
        $('#time_example').html(chrono_time);

    }
    $('#time_textbox').on('input', changedTime);
    var current_time = moment();
    console.log(current_time);


    // if (value_check <= 600) {
    //     alert("NOPE!");
    // }

    var hour_of_current_time = parseInt(current_time.format('H'));
    console.log(hour_of_current_time);


    if (hour_of_current_time < 8) {
        $('#time_suggestion').html("Today at 8am");
        $('#time_textbox').val("Today at 8am");
    } else if ( hour_of_current_time>= 8 && hour_of_current_time < 17) {
        $('#time_suggestion').html("Today at 5pm");
        $('#time_textbox').val("Today at 5pm");
    } else if( hour_of_current_time >= 17 && hour_of_current_time < 22) {
        $('#time_suggestion').html("Today at 10pm");
        $('#time_textbox').val("Today at 10pm");

    } else {
        $('#time_suggestion').html("Tomorrow at 8am");
        $('#time_textbox').val("Tomorrow at 8am");
    }


    changedTime();

});
