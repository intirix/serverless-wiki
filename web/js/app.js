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
    .when("/green", {
        templateUrl : "green.htm"
    })
    .when("/blue", {
        templateUrl : "blue.htm"
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
      //$scope.content = result.data.html;
      $scope.pageContent = $sce.trustAsHtml(result.data.html);
    });
  }).catch( function(result){
    console.log("Failed");
    console.log(result);
  });
});
