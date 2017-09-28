/* MIT License

Copyright (c) 2017 Code for Africa - LABS

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. */

// Google Authentication Functionality

var googleUser = {};
var cid = getMetaContent('google-signin-client_id');
var hd = getMetaContent('google-signin-hosted_domain');
var startApp = function () {
  gapi.load('auth2', function (){
    auth2 = gapi.auth2.init({
      client_id: cid,
      cookiepolicy: 'single_host_origin',
      hosted_domain: hd,
    });
    attachSignin(document.getElementById('g-signin-button'));
  });
};



function attachSignin(element) {
  auth2.attachClickHandler(element, {},
      function(googleUser) {

        var profile = googleUser.getBasicProfile();
        var name = profile.getName();
        var email = profile.getEmail();

	var response = googleUser.getAuthResponse();
	var id_token = response['id_token'];
	var access_token = response['access_token'];

	$.ajax({
  type: 'POST',
  url: '/user/login',
  data: {name: name, email: email, id_token: id_token, token: access_token},
  success: function (res, status, xhr) {
    window.location.replace('/dataset');
  },
  error: function(xhr, status, err) {
    alert('Login failure: ' + err);
  }
});
      }, function(error) {
        console.log(console.error());
      });

}



/* get content from meta tag */
function getMetaContent (propName) {
  var metas = document.getElementsByTagName('meta');
  for (i = 0; i < metas.length; i++) {
	if (metas[i].getAttribute('name') == propName) {
		return metas[i].getAttribute('content');
	}
  }
  return '';
}

/* Firebase Setup and Integration with CKAN */

var config = {
  apiKey: 'AIzaSyC0cAtWyUOKioISC2BIiPgws9PBT6lqSl0',
  authDomain: 'ckan-githubauth.firebaseapp.com',
  databaseURL: 'https://ckan-githubauth.firebaseio.com',
  projectId: 'ckan-githubauth',
  storageBucket: '',
  messagingSenderId: '467483203377'
}

firebase.initializeApp(config)

// Github Authentication Functionality

var githubprovider = new firebase.auth.GithubAuthProvider()
// provider.addScope('user')

function login () {
  firebase.auth().signInWithPopup(githubprovider)
  .then(
    function (result) {
    // This gives you a GitHub Access Token. You can use it to access the GitHub API.
      var token = result.credential.accessToken;
    // The signed-in user info.
      var user = result.user;
      var githubuser = firebase.auth().currentUser

      if (githubuser != null) {
        githubuser.providerData.forEach(function (profile) {
          var signedinusername = profile.email.split('@')[0].replace(/\./g, '')
          $.ajax({
            type: 'POST',
            url: '/user/login',
            data: {name: signedinusername, email: profile.email, id_token: profile.uid, token: token},
            success: function(res, status, xhr) {
              window.location.replace('/dataset');
            },
            error: function(xhr, status, err) {
               alert('Login failure: ' + err);
            }
          });

    });
}
  })

  .catch(
    function(error) {
    // Handle Errors here.
    var errorCode = error.code;
    var errorMessage = error.message;
    // The email of the user's account used.
    var email = error.email;
    // The firebase.auth.AuthCredential type that was used.
    var credential = error.credential;
      console.log(errorCode);
      console.log(errorMessage);

  }
  )
}
