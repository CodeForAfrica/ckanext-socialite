  // Setup an event listener to make an API call once auth is complete
    function onLinkedInLoad() {
        IN.Event.on(IN, "auth", getProfileData);
    }
    // Handle the successful return from the API call
    function onSuccess(data) {
        console.log(data);
        var fullName = data.firstName + ' ' + data.lastName
        $.ajax({
          type: 'POST',
          url:'/user/login',
          data: {name: fullName, email: data.emailAddress, id_token: data.id},
          success: function(res, status, xhr) {
            window.location.replace("/dataset");
         },
        error: function(xhr, status, err) {
          alert("Login failure: " + err);
        }
      });
    }
    // Handle an error response from the API call
    function onError(error) {
        console.log('hey');
    }
    function liAuth(){
        IN.User.authorize(function(){
        });
    }
    // Use the API call wrapper to request the member's basic profile data
    function getProfileData() {  
      IN.API.Raw("/people/~:(email-address,first-name,last-Name,id)").result(onSuccess).error('didnotwork');
    }
