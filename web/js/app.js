var apigClient = apigClientFactory.newClient();
var app = angular.module("myApp", ["ngRoute"]);
app.config(function($routeProvider) {
    $routeProvider
    .when("/", {
        templateUrl : "viewPage.html",
        controller: "ViewPageCtrl",
        controllerAs: "app"
    })
    .when("/view/:page", {
        templateUrl : "viewPage.html",
        controller: "ViewPageCtrl",
        controllerAs: "app"
    })
    .when("/login", {
        templateUrl : "login.html",
        controller: "LoginCtrl",
        controllerAs: "app"
    })
    .when("/signup", {
        templateUrl : "signup.html"
    })
    .when("/logout", {
        templateUrl : "logout.html"
    });
})
.controller('ViewPageCtrl', function($scope,$routeParams,$sce) {
  var self = this;
  self.page = $routeParams.page;
  if (self.page===undefined) {
    self.page="Index"
  }
  console.log("page="+self.page)
  $scope.content = "Loading..."
  params={'page':self.page}
  apigClient.v1PagesPageGet(params,null,{}).then(function(result){
    $scope.content = result.data.html
    console.log(result.data);
    $scope.$apply(function () {
      $scope.pageContent = $sce.trustAsHtml(result.data.html);
      $scope.time_get = result.data.time_get;
      $scope.time_render = result.data.time_render;
      $scope.time_sanitize = result.data.time_sanitize;
    });
  }).catch( function(result){
    console.log("Failed");
    console.log(result);
  });
})
.controller('LoginCtrl', function($scope,$rootScope,$location) {
  $scope.onLogin = function() {
    $rootScope.authuser=$scope.formuser;
    $location.path('/');
  };
});
