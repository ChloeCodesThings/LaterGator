  function statusChangeCallback(response) {

    $('#post_pages_button').hide();
    $('#post_profile_button').hide();
    console.log('statusChangeCallback');



    if (response.status === 'connected') {
      var params = {'access_token': response['authResponse']['accessToken'],
                    'facebook_user_id': response['authResponse']['userID']};

      $.post('/add_fb_token', params, tokenSuccessHandler);

      testAPI();

    } else if (response.status === 'not_authorized') {
      document.getElementById('status').innerHTML = 'Please login to Facebook';
    } else {
      document.getElementById('status').innerHTML = 'Please log ' +
        'into Facebook.';
    }
  }

  function checkLoginState() {
    FB.getLoginStatus(statusChangeCallback);
  }

  window.fbAsyncInit = function() {
    FB.init({
      appId      : '235439073543334',
      cookie     : true,  // enable cookies to allow the server to access 
                          // the session
      xfbml      : true,  // parse social plugins on this page
      version    : 'v2.5' // use graph api version 2.5
    });

    FB.getLoginStatus(statusChangeCallback);


  };

  function tokenSuccessHandler(data) {
    $('#fb_login_button').hide();
    $('#post_pages_button').show();
    $('#post_profile_button').show();

  }

  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));


  function testAPI() {
    console.log('Welcome!  Fetching your information.... ');
    FB.api('/me', function(response) {
      console.log('Successful login for: ' + response.name);
      document.getElementById('status').innerHTML =
        'You are logged in to Facebook!';
    });
  }