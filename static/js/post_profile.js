$(document).ready(function(){

    $("#userpost").on('input', function() {
        if ($(this).val().length>=63206) {
            alert('Oops! Remember- Facebook has a 63,206 character limit!');
         }
         
    $('#remaining_chars').html("Remaining characters : " + (63206 - this.value.length));

     });

    var current_time = moment().format("h:mm a");

    $('#time_right_now').html(current_time);

    function changedTime() {
        var time_from_textbox = $('#time_textbox').val();

        var chrono_time = chrono.parseDate(time_from_textbox);

        var moment_time = moment(chrono_time);

        var moment_unix = moment_time.format('X');

        var timezone = moment_time.format('zz');

        var current_time_unix = current_time.format('X');

        var value_check = moment_unix - current_time_unix;

        if (value_check <= 600) {
            alert("You must post at least 10 minutes from now!");
        } else if (value_check >= 5184000) {
            alert("You cannot post more than 60 days ahead of time!");
        }

        $('#hidden_time').val(moment_unix);
        $('#time_example').html(chrono_time);

    }
    $('#time_textbox').on('input', changedTime);
    var current_time = moment();

    var hour_of_current_time = parseInt(current_time.format('H'));

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
