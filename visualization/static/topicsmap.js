var drawD3Document = function(nodes,links) {
	var WIDTH = $(document).width()*0.75, HEIGHT = $(document).height();
    var width = WIDTH, height = HEIGHT;
    var force = d3.layout.force().nodes(d3.values(nodes)).links(links).size([ width, height ]).linkDistance(100).charge(-500).linkStrength(0).on("tick", tick);
    var svg = d3.select("#canvas-svg").append("svg").attr("width", width).attr("height", height);
    svg.append("svg:defs").selectAll("marker").data([ "end" ]).enter().append("svg:marker").attr("id", String).attr("viewBox", "0 -5 10 10").attr("refX", 15).attr("refY", -1.5).attr("markerWidth", 6).attr("markerHeight", 6).attr("orient", "auto").append("svg:path").attr("d", "M0,-5L10,0L0,5");
    var path = svg.append("svg:g").selectAll("path").data(force.links()).enter().append("svg:path").style('stroke-width',function(d){return d.thickness}).attr("class", "link");

    var node = svg.selectAll(".node")
      .data(force.nodes())
      .enter()
      .append("g")
      .attr("class", "node")
      .on('click', function(d) { focusVertex(d.name) })
      .call(force.drag);

    node.append("circle").attr("r", 10);
    node.append("text").attr("x", "-.25em").attr("dy", ".35em").text(function(d) {
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
            return "translate(" + d.x + "," + d.y + ")";
        });
    }
};

var focusOn = function(f1,f2){
	var svg = d3.select("#canvas-svg");
	var node = svg.selectAll(".node");
	node.select('circle').style('fill', f1);
	node.select('text').style('color',f1);
	var edges = svg.selectAll('.link');
	edges.style('stroke',f2);
}

var focusVertex = function(focusCharacter){
	var fVertex = function(d){
		if(d.name==focusCharacter){
			return "rgb(0,0,0)";
		}
		return "rgb(230,230,230)";
	};
	var fEdge = function(d){
		if(d.source.name==focusCharacter || d.target.name==focusCharacter){
				return "rgb(0,0,0)";
		}
		return "rgb(230,230,230)";
	};
	focusOn(fVertex,fEdge);

};
var focusCategory = function(focusCategory){
	var fVertex = function(d){
		if(d.category==focusCategory){
			return "rgb(0,0,0)";
		}
		return "rgb(230,230,230)";
	};
	var fEdge = function(d){
		if(d.source.category==focusCategory || d.target.category==focusCategory){
				return "rgb(0,0,0)";
		}
		return "rgb(230,230,230)";
	};
	focusOn(fVertex,fEdge);
};