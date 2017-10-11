  // Initaialize and set up Facebook JS SDK
  window.fbAsyncInit = function() {
    FB.init({
      appId      : '646613148876732',
      cookie     : true,
      xfbml      : true,
      version    : 'v2.10'
    });
    FB.AppEvents.logPageView();   

      FB.getLoginStatus(function(response) {
          console.log(response);
      });
  };

  (function(d, s, id){
     var js, fjs = d.getElementsByTagName(s)[0];
     if (d.getElementById(id)) {return;}
     js = d.createElement(s); js.id = id;
     js.src = "//connect.facebook.net/en_US/sdk.js";
     fjs.parentNode.insertBefore(js, fjs);
   }(document, 'script', 'facebook-jssdk'));

  function fb_login() {
    FB.login(function(response) {
      if (response.status === 'connected') {
        accessToken = response.authResponse.accessToken;
        idToken = response.authResponse.userID;
        FB.api('/me', {locale: 'en_US', fields: 'id,first_name,last_name,email'},
          function (response) {
            console.log(response);
            var fullName = response.first_name + ' ' + response.last_name;
            var email = response.email;
            $.ajax({
              type: 'POST',
              url:'/user/login',
              data: {name: fullName, email: email, id_token: idToken, token: accessToken},
              success: function(res, status, xhr) {
                window.location.replace("/dataset");
             },
            error: function(xhr, status, err) {
              alert("Login failure: " + err);
            }
          });
      });
      } else {
        window.location.replace("/user/login");
      }
    });
  }
  