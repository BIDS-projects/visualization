  var names = [];
    for (var i = 0; i < nodes.length; i++) {
    names.push(nodes[i].name);
    }
  var center = "";
  var force;
  var app = angular.module('myApp', []);
  var connectsTo = function(category1,category2){
    for(var i = 0; i< edges.length;i++){
      curr = edges[i];
      if((curr.source.name == category1 && curr.target.name==category2) || (curr.source.name == category2 && curr.target.name==category1)) return true;
    }
    return false;
  }
  app.controller('myCtrl', function($scope) {
  $scope.drawD3Document = function(nodes,links) {
    var WIDTH = $(document).width(), HEIGHT = $(document).height();
      force = d3.layout.force().nodes(d3.values(nodes)).links(links).size([ 9*WIDTH/12, HEIGHT ]).linkDistance(50).charge(-3000).on("tick", tick);
      var svg = d3.select("#canvas-svg").append("svg").attr("width", WIDTH).attr("height", HEIGHT);
      svg.append("svg:defs").selectAll("marker").data([ "end" ]).enter().append("svg:marker").attr("id", String).attr("viewBox", "0 -5 10 10").attr("refX", 15).attr("refY", -1.5).attr("markerWidth", 6).attr("markerHeight", 6).attr("orient", "auto").append("svg:path").attr("d", "M0,-5L10,0L0,5");
      var path = svg.append("svg:g").selectAll("path").data(force.links()).enter().append("svg:path").style('stroke-width',function(d){return d.thickness}).attr("class", "link");

      var node = svg.selectAll(".node").data(force.nodes()).enter().append("g").attr("class", "node").call(force.drag);
      node.append("circle").attr("r", 10);
      node.append("p").attr("x", 12).attr("dy", ".35em").text(function(d) {
          return d.name;
      });
      force.start();
      for (var i = 0; i < 100; ++i) force.tick();
      force.stop();
      function tick() {
          path.attr("d", function(d) {
              var dx = d.target.x - d.source.x, dy = d.target.y - d.source.y, dr = Math.sqrt(dx * dx + dy * dy);
              return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
          });
          node.attr("transform", function(d) {
            if(d.name==center){
              d.x = WIDTH/3;
              d.y = HEIGHT/2;
            }
              return "translate(" + d.x + "," + d.y + ")";
          });
      }
    };
    $scope.domainshow = true;
    $scope.closest = [];
    $scope.bestcategories = [];
    $scope.colors = colors;
    $scope.allcategories = [];
    for (var cat in categories) {
        if (categories.hasOwnProperty(cat)) {
          $scope.allcategories.push(cat);
        }
      }

    $scope.generateDegreeList = function(){
      var degrees = [];
      for(var i = 0; i < nodes.length;i++) degrees.push([nodes[i].name,0]);
      edges.forEach(function(curr){
        degrees[curr.source.index][1]+=curr.thickness;
        degrees[curr.target.index][1]+=curr.thickness;
      });
      degrees.sort(function(a,b){
        return b[1]-a[1];
      });
      return degrees;
    }
    $scope.generateCategoryDegreeList = function(category){
      var degrees = [];
      for(var i = 0; i < nodes.length;i++) degrees.push([nodes[i].name,0]);
      edges.forEach(function(curr){
        if(findBestCategory(curr.source.name)==category){
          degrees[curr.source.index][1]+=curr.thickness;
        }
        if(findBestCategory(curr.target.name)==category){
          degrees[curr.target.index][1]+=curr.thickness;
        }   
           });
      degrees.sort(function(a,b){
        return b[1]-a[1];
      });
      return degrees;
    }
    $scope.generateClosestDegreeList = function(closest){
      var degrees = [];
      for(var i = 0; i < nodes.length;i++) degrees.push([nodes[i].name,0]);
      edges.forEach(function(curr){
        if(curr.source.name==closest){
          degrees[curr.target.index][1]+=curr.thickness;
        }
        if(curr.target.name==closest){
          degrees[curr.source.index][1]+=curr.thickness;
        }
      });
      degrees.sort(function(a,b){
        return b[1]-a[1];
      });
      return degrees;
    }

    $scope.catColor = function(focusCategory){
      var rgb = colors[focusCategory]
      var checkVert = function(d){
        if (d.category == focusCategory){
          return "rgb(" + rgb[0] + "," + rgb[1] + "," + rgb[2] + ")"
        return "rgb(230, 230, 230)"
        }
      }
      var checkEdge = function(d){
        if (d.source.category == focusCategory || d.target.category == focusCategory){
          return "rgb(" + rgb[0] + "," + rgb[1] + "," + rgb[2] + ")"
        }
        return "rgb(230, 230, 230)"
          
      }
      focusOn(checkVert, checkEdge);
    }
    var focusOn = function(f1,f2){
      var svg = d3.select("#canvas-svg");
      var node = svg.selectAll(".node");
      node.select('circle').style('fill', f1);
      node.select('p').style('color',f1);
      var edges = svg.selectAll('.link');
      edges.style('stroke',f2);
    }

// Colors vertices and edges based on a specific vertex (non weighted <rgb>)
    var findBestCategory = function(focusNode){
      var bestcategory = "";
      var bestval = 0;
      for (var cat in categories) {
        if (categories.hasOwnProperty(cat)) {
          if(categories[cat][focusNode] > bestval){
            bestcategory = cat;
            bestval = categories[cat][focusNode];
          }
        }
      }
      return bestcategory;
    };

    
    var getSortedCategories = function(focusNode){
      var categorys = [];
      for (var cat in categories) {
        if (categories.hasOwnProperty(cat)) {
          categorys.push(cat);
        }
      }
      categorys.sort(function(a,b){
        return categories[b][focusNode] - categories[a][focusNode];
      });
      return categorys;
    }

    $scope.focusVertex = function(focusCharacter){
      center = focusCharacter;
      var fVertex = function(d){
        if(d.name==focusCharacter){
          force.start();
        $("#focusname").text(d.name);
        $("#focushref").attr("href", "http://"+d.link);
        $("#focushref").text("Link to Main Page");
        $("#focusdesc").text(d.purpose);
        $scope.closest = $scope.generateClosestDegreeList(d.name).slice(0,3);
         $scope.bestcategories = getSortedCategories(focusCharacter).slice(0,2);
        $scope.domainshow = false;

          return findBestColor(d.name,false);
        }; 
        var rgb = findBestColor(d.name,false);
        rgb = rgb.substring(4,rgb.length-1);
        if(connectsTo(d.name,focusCharacter)){
          return "rgba("+rgb+", .5)"
        } 
        return "rgba("+rgb+", .2)";
      };
      var fEdge = function(d){
        if(d.source.name==focusCharacter || d.target.name==focusCharacter){
            return findBestColor(focusCharacter,true);
        };
        return "rgba(0,0,0,0)";
      };
      focusOn(fVertex,fEdge);
      
    };
// Colors vertices and edges based on a category (non weighted <rgb>)
    $scope.focusCategory = function(focusCategory){
      var fVertex = function(d){
        if(d.category==focusCategory){
          return "rgb(0,0,0)";
        };
        return "rgb(230,230,230)";
      };
      var fEdge = function(d){
        if(d.source.category==focusCategory || d.target.category==focusCategory){
            return "rgb(0,0,0)";
        };
        return "rgb(230,230,230)";
      };
      focusOn(fVertex,fEdge);
    }

    //Colors all the nodes based on relationship to category (only one selected) 
    $scope.catColorAlpha = function(focusCategory){
      var dict = categories[focusCategory];
      var rgb = colors[focusCategory];
      var rgbaString = "rgba(" + rgb[0] + "," + rgb[1] + "," + rgb[2];
      var colorCalcVert = function(d){
       // We are going to add alpha in the loop
            return rgbaString + "," + dict[d.name] + ")";  
      }
      var colorCalcEdge = function(d){
        var alpha1 = d.source.name.toString();
        var alpha2 = d.target.name.toString();
        return  rgbaString + "," + Math.max(dict[alpha1], dict[alpha2]);
      }
      focusOn(colorCalcVert,colorCalcEdge);
      $scope.topdegrees = $scope.generateCategoryDegreeList(focusCategory).slice(0,5);

    };
    var findBestColor = function(name,rgba){
      var focusCategory = findBestCategory(name);
      var dict = categories[focusCategory];
      var rgb = colors[focusCategory];
      if(rgba){
          return "rgba(" + rgb[0] + "," + rgb[1] + "," + rgb[2]+","+categories[focusCategory][name]+")";
      }
      return "rgb(" + rgb[0] + "," + rgb[1] + "," + rgb[2]+")";
    };
    $scope.catAllColorAlpha = function(){
      var colorCalcVert = function(d){
       return findBestColor(d.name,true);
      }
      var colorCalcEdge = function(d){
        return findBestColor(d.source.name,true);

      }
      focusOn(colorCalcVert,colorCalcEdge);
      $scope.topdegrees = $scope.generateDegreeList().slice(0,5);
    };


    $("#search").typeahead({ source:names, afterSelect: function(val){$scope.focusVertex(val); $scope.$apply();} });
    $scope.drawD3Document(nodes,edges);
    $scope.catAllColorAlpha();
    $( ".node" ).contextmenu(function() {
      $scope.focusVertex(this.textContent);
      $scope.$apply();
      return false;
    });

});