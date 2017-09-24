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
    .when("/edit/:page", {
        templateUrl : "editPage.html",
        controller: "EditPageCtrl",
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
.controller('ViewPageCtrl', function($scope,$rootScope,$routeParams,$sce) {
  var self = this;
  self.page = $routeParams.page;
  if (self.page===undefined) {
    self.page="Index"
  }
  console.log("page="+self.page)
  $rootScope.pageState = 'loading';
  $scope.page = self.page;
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
      $rootScope.pageState = 'loaded';
    });
  }).catch( function(result){
    $rootScope.pageState = 'error';
    console.log("Failed");
    console.log(result);
  });
})
.controller('EditPageCtrl', function($scope,$rootScope,$routeParams,$sce) {
  var self = this;
  self.page = $routeParams.page;
  if (self.page===undefined) {
    self.page="Index"
  }
  $rootScope.pageState = 'loading';
  $scope.content = "Loading..."
  $scope.contentTypes = [ "mediawiki" ];
  $scope.page = self.page;
  console.log("page="+self.page)
  params={'page':self.page}
  apigClient.v1PagesPageGet(params,null,{}).then(function(result){
    $scope.content = result.data.html
    console.log(result.data);
    $scope.$apply(function () {
      $scope.content = $sce.trustAsHtml(result.data.content);
      $rootScope.pageState = 'loaded';
    });
  }).catch( function(result){
    $rootScope.pageState = 'error';
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
