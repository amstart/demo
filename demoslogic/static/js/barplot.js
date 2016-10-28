function barplot(data)
{
var x = d3.scaleLinear()
    .domain([0, d3.max(data)])
    .range([10, 300]);
d3.select(".barchart")
    .selectAll("div")
        .data(data)
    .enter().append("div")
        .style("width", function(d) { return x(d) + "px"; })
        .text(function(d) { return d; });
}
