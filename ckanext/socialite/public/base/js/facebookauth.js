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

  // Check if user is logged in.
  function checkLoginState() {
    FB.getLoginStatus(function(response) {
      if(response.status === 'connected'){
        console.info('API call sucessfull')
        window.location.replace("/dataset"); //This works! but it won't change the header.
      } else {
        console.info('API call not sucessfull')
        window.location.replace("/user/login");
      }
    });
  }

  // FB.getLoginStatus(function(response) {
  //     if(response.status === 'connected'){
  //       console.info('We are connected')
  //     } else if (response.status === 'not_authorized'){
  //       console.info('We are not connected')
  //     } else {
  //       console.info('We are not even logged in')
  //     }
  //   });