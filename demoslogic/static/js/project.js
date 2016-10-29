/* Project specific Javascript goes here. */
function barplot(data, labels, choice)
{
function set_bar_text(d, index) {
    if (index+1 == choice)
        return d + " (you)";
    else {
        return d;}
}
var x = d3.scaleLinear()
    .domain([0, d3.max(data)])
    .range([10, 300]);
var bar_labels = d3.select(".chart").selectAll("div")
    .data(labels)
    .enter().append("div")
    .attr("class", "row")
    .text(function(d) { return d + ":"; });
var bar_bars = bar_labels.append("div")
    .data(data)
    .style("width", function(d) { return x(d) + "px"; })
    .attr("class", "bar")
    .text(set_bar_text);
}

/*
Formatting hack to get around crispy-forms unfortunate hardcoding
in helpers.FormHelper:

    if template_pack == 'bootstrap4':
        grid_colum_matcher = re.compile('\w*col-(xs|sm|md|lg|xl)-\d+\w*')
        using_grid_layout = (grid_colum_matcher.match(self.label_class) or
                             grid_colum_matcher.match(self.field_class))
        if using_grid_layout:
            items['using_grid_layout'] = True

Issues with the above approach:

1. Fragile: Assumes Bootstrap 4's API doesn't change (it does)
2. Unforgiving: Doesn't allow for any variation in template design
3. Really Unforgiving: No way to override this behavior
4. Undocumented: No mention in the documentation, or it's too hard for me to find
*/
$('.form-group').removeClass('row');
