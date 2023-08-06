//Glasseye chart super class: sets up the svg and the chart area
var GlasseyeChart = function(div, size, margin, custom_height) {

  var self = this;

  self.div = div;
  self.size = size;
  self.margin = margin;
  self.custom_height = custom_height;

  //Set the size of the chart
  self.set_size();

};

GlasseyeChart.prototype.set_size = function() {

  var self = this;

  //Get dimension of the div
  var rect = d3.select(self.div).node().getBoundingClientRect();

  //Set chart dimensions according to whether the chart is placed in the margin or the main page

  if (self.margin === undefined) {
    self.margin = {
      top: 20,
      bottom: 20,
      right: 20,
      left: 20
    };
  }


  if (self.size === "full_page") {
    self.svg_width = (rect.width < 500 & rect.width > 0) ? rect.width : 500;
    self.svg_height = (self.custom_height === undefined) ? 300 : self.custom_height;
  } else if (self.size === "margin") {
    //self.svg_width = (rect.width < 300) ? rect.width : 300;
    self.svg_width = 300;
    self.svg_height = (self.custom_height === undefined) ? 250 : self.custom_height;
  } else if (self.size === "double_plot_wide") {
    self.svg_width = (rect.width < 600) ? rect.width : 600;
    self.svg_height = (self.custom_height === undefined) ? 360 : self.custom_height;
    //self.margin.bottom = 50;
  } else if (self.size === "double_plot_narrow"){
    self.svg_width = (rect.width < 300) ? rect.width : 300;
    self.svg_height = (self.custom_height === undefined) ? 360 : self.custom_height;
    //self.margin.bottom = 50;
  }
    else {
    self.svg_width = 300;
    self.svg_height = (self.custom_height === undefined) ? 360 : self.custom_height;
  }


  //Work out the dimensions of the chart
  self.width = self.svg_width - self.margin.left - self.margin.right;
  self.height = self.svg_height - self.margin.top - self.margin.bottom;

  //Define color scales



  return self;

};

GlasseyeChart.prototype.add_svg = function() {

  var self = this;

  //Add the svg to the div
  self.svg = d3.select(self.div).append("svg")
    .attr("class", "glasseye_chart")
    .attr("width", self.svg_width)
    .attr("height", self.svg_height);

  //Add the chart area to the svg
  self.chart_area = self.svg.append("g")
    .attr("class", "chart_area")
    .attr("transform", "translate(" + self.margin.left + "," + self.margin.top + ")");

  return self;
};


/**
 * Adds a label to the TimeSeries object
 * @method
 * @param {string} title The title to be placed at the top of the chart
 * @returns {object} The modified TimeSeries object
 */

GlasseyeChart.prototype.add_title = function(title, subtitle) {

  var self = this;
  self.title = title;
  self.svg.append('text').attr("class", "title")
      .text(title)
      .attr("transform", "translate(" + self.margin.left + ",20)");

  if (subtitle != undefined) {

    self.subtitle = subtitle;
    self.svg.append('text').attr("class", "subtitle")
        .text(subtitle)
        .attr("transform", "translate(" + self.margin.left + ",35)");

  }

  return self;

};


GlasseyeChart.prototype.set_tooltip_text = function (commentary_strings, variable_names, formats) {

  var self = this;

  self.tooltip_text = function (d) {
    var embedded_vars = variable_names.map(function(e){
      return (e==="filter")? self.current_variable : d[e];
    })
    var text = create_commentary(commentary_strings, embedded_vars, formats)
    return text;
  }

  self.tip = d3.tip()
      .attr('class', 'd3-tip')
      .offset([-10, 0])
      .html(self.tooltip_text);

  return self;

}
var GridChart = function (div, size, labels, scales, margin, height) {

    var self = this;
    self.scales = scales;
    self.labels = labels;

    GlasseyeChart.call(self, div, size, margin, height);

    if (scales[0].scale_type === "ordinal") {
        self.x = self.scales[0].scale_func.rangePoints([0, self.width], 1);
    } else {
        self.x = self.scales[0].scale_func.range([0, self.width]);
    }

    if (scales[1].scale_type === "ordinal") {
        self.y = self.scales[1].scale_func.rangePoints([self.height, 0], 1);
    } else {
        self.y = self.scales[1].scale_func.range([self.height, 0]);
    }


    self.x_axis = d3.svg.axis()
        .scale(self.x)
        .orient("bottom")
        .tickSize(-self.height, 0, 0)
        .tickPadding(10);

    self.y_axis = d3.svg.axis()
        .scale(self.y)
        .orient("left")
        .tickSize(-self.width, 0, 0);

    //If the scale is not ordinal apply the universal format
    if (scales[1].scale_type != "ordinal") {self.y_axis .tickFormat(uni_format_axis)};

    self.tooltip_formtter = uni_format;

};

GridChart.prototype = Object.create(GlasseyeChart.prototype);

GridChart.prototype.set_y_axis_format = function (format) {

    var self = this;

    self.y_axis.tickFormat(format);
    self.tooltip_formtter = format;
    return self;

}



GridChart.prototype.add_grid = function () {

    var self = this;

    var x_axis_g = self.chart_area.append("g")
        .attr("class", "chart_grid x_axis")
        .attr("transform", "translate(0," + self.height + ")")
        .call(self.x_axis);

    if (self.scales[0].scale_type === "nonlinear") {
        x_axis_g.selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", "rotate(-90)");
    }

    self.chart_area.append("g")
        .attr("class", "chart_grid y_axis")
        .call(self.y_axis);

    //Add labels if they have been provided

    if (typeof self.labels !== "undefined") {
        self.svg.append("g")
            .attr("class", "axis_label axis_label_x")
            .attr("transform", "translate(" + (self.margin.left + self.width + 15) + ", " + (self.height + self.margin.top) + ") rotate(-90)")
            .append("text")
            .text(self.labels[0]);

        self.svg.append("g")
            .attr("class", "axis_label axis_label_y")
            .attr("transform", "translate(" + self.margin.left + ", " + (self.margin.top - 8) + ")")
            .append("text")
            .text(self.labels[1]);
    }

    return self;

};
/**
 * Builds a BarChart object
 * @constructor
 * @param {array} processed_data Data that has been given a structure appropriate to the chart
 * @param {string} div The div in which the chart will be placed
 * @param {string} size The size (one of several preset sizes)
 * @param {array} [labels] An array of the axis labels
 * @param {array} scales Scales for the x and y axes
 * @param {object} [margin] Optional argument in case the default margin settings need to be overridden
 */

var BarChart = function (processed_data, div, size, labels, scales, margin) {

    var self = this;

    self.processed_data = processed_data;

    self.type = (self.processed_data[0].group === undefined) ? "simple" : "group";

    //Work out if there is a need for label rotation

    var x_scale_labels = scales[0].scale_func.domain();
    var max_string = d3.max(x_scale_labels.map(function (d) {
        return d.length;
    }));
    var num_points = x_scale_labels.length;

    self.rotate_labels = (max_string > 60 / num_points)? true: false;

    if (margin === undefined) {
        margin = {
            top: 20,
            bottom: 30,
            right: 20,
            left: 40
        };
    }

    if (self.rotate_labels === true) {margin.bottom = max_string*5};

    if (self.type === "group") {
        margin.right = 80;

        self.loose_bars = self.processed_data.map(function (d) {

            return (d.values.map(function (e) {
                return {
                    value: e.value,
                    group: d.group,
                    label: e.label,
                    y0: e.y0,
                    y1: e.y1
                };
            }));
        });


        self.loose_bars = [].concat.apply([], self.loose_bars).filter(function (d) {
            return d !== undefined;
        });


        //Section to work out the number of labels
        self.legend_labels = [];

        self.loose_bars.forEach(function (d) {
            if (self.legend_labels.indexOf(d.label) === -1) {
                self.legend_labels.push(d.label);
            }
        });

        self.num_labels = self.legend_labels.length;

        self.color = d3.scale.ordinal()
            .range(colorbrewer.RdBu[self.num_labels]);
    }

    GridChart.call(self, div, size, labels, scales, margin);

    //Some customisations
    //self.margin.left = 4;
    //self.y_axis.tickFormat("");

    self.tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function (d) {
            var text = (self.type === "simple") ? uni_format(d.value) : d.label + "<br> size: " + uni_format(d.value);
            return text;
        });

    self.bar_width = self.width / processed_data.length;

};

BarChart.prototype = Object.create(GridChart.prototype);


/**
 * Adds the SVGs corresponding to the BarChart object
 *
 * @method
 * @returns {object} The modified BarChart object
 */

BarChart.prototype.add_bars = function () {

    var self = this;

    self.chart_area.call(self.tip);

    if (self.type === "simple") {

        self.chart_area.selectAll(".bar")
            .data(self.processed_data)
            .enter()
            .append("rect")
            .attr("class", "bar")
            .attr("x", function (d) {
                return self.x(d.label) - self.bar_width / 4;
            })
            .attr("y", function (d) {
                return self.y(d.value);
            })
            .attr("width", self.bar_width / 2)
            .attr("height", function (d) {
                return self.height - self.y(d.value);
            })
            .on('mouseover', self.tip.show)
            .on('mouseout', self.tip.hide);

    } else {

        self.chart_area.selectAll(".bar")
            .data(self.loose_bars)
            .enter()
            .append("rect")
            .attr("class", "bar")
            .attr("x", function (d) {
                return self.x(d.group) - self.bar_width / 4;
            })
            .attr("y", function (d) {
                return self.y(d.y1);
            })
            .attr("width", self.bar_width / 2)
            .attr("height", function (d) {
                return self.y(d.y0) - self.y(d.y1);
            })
            .on('mouseover', self.tip.show)
            .on('mouseout', self.tip.hide)
            .on('click', function () {
                self.change_layout("to_side");
            })
            .style("fill", function (d) {
                return self.color(d.label);
            });

        //Add the legend
        add_legend(self.svg, self.margin.left + self.width + 20, self.margin.top, self.legend_labels.map(function (v, i) {
            return {
                "label": v,
                "colour": self.color(v),
                "class": "d_" + i
            };
        }).reverse());

    }

    //Rotate labels if necessary

    if (self.rotate_labels === true) {
        self.chart_area.selectAll(".x_axis").selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-1em")
            .attr("dy", "-0.8em")
            .attr("transform", "rotate(-90)");
    }

    //Prune the y axis tick labels

    var tick_labels = self.chart_area.selectAll(".y_axis").selectAll("text");
    var ticks_even = +(tick_labels[0].length % 2 === 0);
    tick_labels.style("opacity", function (d, i) {
        return (i % 2 === ticks_even) ? 1 : 0;
    });

    return self;

};

/**
 * Changes a grouped barchart from stacked to side by side and vice versa.
 *
 * @method
 * @returns {object} The modified BarChart object
 */

BarChart.prototype.change_layout = function (direction) {

    var self = this;

    if (direction === "to_side") {

        //Adjust the y axis

        self.preserved_domain = self.y.domain();
        var max_to_side = 0;
        self.processed_data.forEach(function (d) {
            d.values.forEach(function (e) {
                max_to_side = (e.value > max_to_side) ? e.value : max_to_side;
            })
        });
        self.y.domain([self.preserved_domain[0], max_to_side]);
        self.chart_area.selectAll(".y_axis").transition()
            .duration(1000)
            .call(self.y_axis);

        //Prune the y axis tick labels
        var tick_labels = self.chart_area.selectAll(".y_axis").selectAll("text");
        var ticks_even = +(tick_labels[0].length % 2 === 0);
        tick_labels.style("opacity", function (d, i) {
            return (i % 2 === ticks_even) ? 1 : 0;
        });


        self.chart_area.selectAll(".bar")
            .on('click', function () {
                self.change_layout("to_stack");
            })
            .transition()
            .duration(1000)
            .attr("width", self.bar_width * 0.8 / self.num_labels)
            .attr("y", function (d) {
                return self.y(d.value);
            })
            .attr("height", function (d) {
                return self.y(d.y0) - self.y(d.y1);
            })
            .attr("x", function (d) {
                var j = self.legend_labels.indexOf(d.label);
                return self.x(d.group) + j * (self.bar_width * 0.8 / self.num_labels) - self.bar_width * 0.5 + self.bar_width * 0.1;
            });


    } else {

        self.y.domain(self.preserved_domain);
        self.chart_area.selectAll(".y_axis").transition()
            .duration(1000)
            .call(self.y_axis);

        //Prune the y axis tick labels
        var tick_labels = self.chart_area.selectAll(".y_axis").selectAll("text");
        var ticks_even = +(tick_labels[0].length % 2 === 0);
        tick_labels.style("opacity", function (d, i) {
            return (i % 2 === ticks_even) ? 1 : 0;
        });

        self.chart_area.selectAll(".bar")
            .on('click', function () {
                self.change_layout("to_side");
            })
            .transition()
            .duration(1000)
            .attr("x", function (d) {
                return self.x(d.group) - self.bar_width / 4;
            })
            .attr("y", function (d) {
                return self.y(d.y1);
            })
            .attr("width", self.bar_width / 2)
            .attr("height", function (d) {
                return self.y(d.y0) - self.y(d.y1);
            });


    }


};

/**
 * Allows the used to see which differences are significant
 *
 * @method
 * @returns {object} The modified BarChart object
 */

BarChart.prototype.grumpy = function (method) {

    var self = this;

    if (self.type === "simple") {

        //Add the commentary div;

        d3.selectAll(self.div).append("div").attr("id", "commentary").style("width", self.width + "px").style("margin-left", self.margin.left + "px");

        var bar_values = self.processed_data.map(function (d) {
            return d.value
        });
        var bar_labels = self.processed_data.map(function (d) {
            return d.label
        });
        var sum_values = d3.sum(bar_values);

        if (method === "bayesian") {

            var alphas = bar_values.map(function (d) {
                return d + 1
            });

            //Work out shrunk means
            var sum_alphas = d3.sum(alphas);

            var shrunk_means = alphas.map(function (d) {
                return sum_values * d / sum_alphas;
            });

            //Generate draws from the posterior distribution
            var draw = random_dirichlet(alphas);
            var sample = [];

            for (var i = 0; i < 5000; i = i + 1) {
                sample.push(draw())
            }
            ;

            var comparisons = [];

            bar_labels.forEach(function (d, i) {
                bar_labels.forEach(function (e, j) {
                    comparisons.push(
                        {
                            A: i, B: j, A_label: d, B_label: e,
                            diff_dist: sample.map(function (f) {
                                return f[i] - f[j];
                            }),
                        })
                })

            });

            self.comparisons = comparisons.map(function (d) {
                return {
                    A: d.A, B: d.B, A_label: d.A_label, B_label: d.B_label,
                    diff_dist: d.diff_dist,
                    less_than_zero: d3.sum(d.diff_dist.map(function (e) {
                        return (e < 0) ? 1 : 0;
                    })) / 5000,
                    more_than_zero: d3.sum(d.diff_dist.map(function (e) {
                        return (e < 0) ? 0 : 1;
                    })) / 5000
                }
            })


            //Shadows for shrunken means
            shrunk_means = shrunk_means.map(function (d, i) {
                return {
                    label: bar_labels[i],
                    value: d
                };
            });


            self.chart_area.insert("g", "rect").selectAll(".bar_shrunk")
                .data(shrunk_means)
                .enter()
                .append("rect")
                .attr("class", "bar_shrunk")
                .attr("x", function (d) {
                    return self.x(d.label) - self.bar_width / 4 + 15;
                })
                .attr("y", function (d) {
                    return self.y(d.value);
                })
                .attr("width", self.bar_width / 2)
                .attr("height", function (d) {
                    return self.height - self.y(d.value);
                })
                .style("fill", "steelblue")
                .style("opacity", 0.2);


            //Click to show differences

            self.select_mode = 0;

            self.posterior_diff = function (d, i) {


                if (self.select_mode === 0) {
                    self.select_mode = 1;
                    self.A = i;
                }

                else if (self.select_mode === 1) {
                    self.select_mode = 2;
                    self.B = i;
                    console.log(self.comparisons);
                    var diff = self.comparisons.filter(function (f) {
                        return f.A === self.A & f.B === self.B;
                    })[0];


                    d3.selectAll(self.div).selectAll("#commentary").html("Assuming that data sampling was random, there is a " + d3.format("%")(diff.more_than_zero) + " probability that the number of " + diff.A_label + " in the population is greater that the number of " + diff.B_label);
                }

                else {
                    console.log("ok");
                }

            };


            self.chart_area.selectAll(".bar")
                .on('click', function (d, i) {
                    if (self.select_mode === 2) {
                        self.chart_area.selectAll(".bar").style("fill", 'steelblue');
                        self.select_mode = 0;
                    }
                    d3.select(this).style("fill", '#2b506e');
                    self.posterior_diff(d, i);
                })


            /*
             .on('mouseover', function(d){
             self.tip.show(d);
             d3.selectAll(".bar_shrunk").style("opacity", 0.2);
             })
             .on('mouseout', function(d){
             self.tip.show(d);
             d3.selectAll(".bar_shrunk").style("opacity", 0);
             });
             */


        }

    }


}


/**
 * Creates a barchart within a div
 *
 * @param {array} data Either the path to a csv file or inline data in glasseye
 * @param {string} div The div in which the chart will be placed
 * @param {string} size The size (one of several preset sizes)
 * @param {array} labels An array containing the labels of the x and y axes
 */


function barchart(data, div, size) {

    var inline_parser = function (data) {

        processed_data = [];

        for (i = 0; i < data.value.length; i++) {
            data_item = {
                "label": data.label[i],
                "value": +data.value[i]
            };
            processed_data.push(data_item);

        }
        return processed_data;

    };

    var draw = function (processed_data, div, size) {

        var x_values = [],
            y_values = [];

        if (processed_data[0].group === undefined) {

            x_values = processed_data.map(function (d) {
                return d.label;
            });
            y_values = processed_data.map(function (d) {
                return d.value;
            });

        } else {

            x_values = processed_data.map(function (d) {
                return d.group;
            });

            y_values = processed_data.map(function (d) {
                return (d.values.map(function (e) {
                    return e.y1;
                }));
            });
            y_values = [].concat.apply([], y_values);

        }


        var scales = [create_scale(x_values, d3.scale.ordinal()), create_scale(y_values, d3.scale.linear())];


        var glasseye_chart = new BarChart(processed_data, div, size, ["label", "value"], scales);

        glasseye_chart.add_svg().add_grid().add_bars().grumpy("bayesian");


    };

    build_chart(data, div, size, undefined, group_label_value_parser, inline_parser, draw);


}
var heatmap_parser = function (data) {

        var processed_data;

        processed_data = data.map(function (d) {
            return {
                category_x: d.category_x,
                category_y: d.category_y,
                group: d.group,
                value: +d.value,
                nat_avg: +d.nat_avg,
                raw_value: +d.segment
            };
        });


        //Insert undefined for all combinations that don't appear

        //Get all groups
        var group = [];
        processed_data.map(function (d) {
            if (group.indexOf(d.group) === -1) {
                group.push(d.group);
            }
        });

        //Get all category_x
        var category_x = [];
        processed_data.map(function (d) {
            if (category_x.indexOf(d.category_x) === -1) {
                category_x.push(d.category_x);
            }
        });

        //Get all category_y
        var category_y = [];
        processed_data.map(function (d) {
            if (category_y.indexOf(d.category_y) === -1) {
                category_y.push(d.category_y);
            }
        });


        var augmented_data = []

        group.forEach(function (d) {
                category_x.forEach(function (e) {
                    category_y.forEach(function (f) {
                        var i = processed_data.filter(function (g) {
                            return g.group === d & g.category_x === e & g.category_y === f;
                        });

                        if (i.length === 0) {
                            augmented_data.push(
                                {
                                    category_x: e,
                                    category_y: f,
                                    group: d,
                                    value: undefined,
                                    nat_avg: undefined,
                                    raw_value: undefined
                                }
                        );
                        }
                        else {

                            augmented_data.push(i[0]);
                        }
                    })
                    ;
                })

            }
        )
        ;

        return (augmented_data);

    }
    ;


var polygon_map_parser = function (data) {

    var ireland = topojson.feature(data, data.objects.Ireland).features[0];
    var ulster = topojson.feature(data, data.objects.Ulster).features[0];
    var tv_regions = topojson.feature(data, data.objects.TVRegions).features;
    ireland.properties['name'] = "Ireland";
    ulster.properties['name'] = "Ulster";
    tv_regions.push(ireland);
    tv_regions.push(ulster);
    return (tv_regions);

};


var time_linked_venn_parser = function (data) {

    //Get all the dates

    var times = [];
    data.map(function (d) {
        if (times.indexOf(d.time) === -1) {
            times.push(d.time);
        }
    });

    var parse_date = d3.time.format("%d/%m/%Y").parse;

    //Create the json data from the csv data
    var processed_data = times.map(function (g) {

        return {
            time: parse_date(g),
            venns: data.filter(function (d) {
                return d.time === g;
            }).map(function (e) {
                return {
                    size: +e.value,
                    sets: e.group.split("_")

                };
            })
        };
    });

    return processed_data;

};

var drillable_venn_parser = function (data) {



    //Get all the parents

    var parents = [];
    data.map(function (d) {
        if (parents.indexOf(d.parent) === -1) {
            parents.push(d.parent);
        }
    });

    //Create the json data from the csv data
    var processed_data = parents.map(function (g) {

        return {
            parent: g,
            venns: data.filter(function (d) {
                return d.parent === g;
            }).map(function (e) {
                return {
                    size: +e.value,
                    sets: e.group.split("_")

                };
            })
        };
    });


    return processed_data;

};

var timeseries_parser = function (data) {

    var groups = [];
    data.map(function (d) {
        if (groups.indexOf(d.group) === -1) {
            groups.push(d.group);
        }
    });


    var parse_date = d3.time.format("%d/%m/%Y").parse;

    //Create the json data from the csv data
    var processed_data = groups.map(function (g) {

        return {
            group: g,
            values: data.filter(function (d) {
                return d.group === g;
            }).map(function (e) {
                return {
                    value: +e.value,
                    time: parse_date(e.time),
                    variable: e.variable
                };
            }).sort(function (a, b) {
                return (a.time - b.time);
            })
        };
    });

    return processed_data;

};

var time_linked_parser = function (data) {


    var categories = [];
    data.map(function (d) {
        if (categories.indexOf(d.category) === -1) {
            categories.push(d.category);
        }
    });

    //Try some date formats
    var parse_date = d3.time.format("%d/%m/%Y").parse;

    //Create the json data from the csv data
    var processed_data = categories.map(function (g) {

        return {
            category: g,
            values: data.filter(function (d) {
                return d.category === g;
            }).map(function (e) {
                return {
                    value: +e.value,
                    time: parse_date(e.time),
                    variable: e.variable
                };
            }).sort(function (a, b) {
                return (a.time - b.time);
            })
        };
    });

    return processed_data;

};

var dial_parser = function (data) {

    //Get all the groups

    //Get all the dates

    var groups = [];
    data.map(function (d) {
        if (groups.indexOf(d.group) === -1) {
            groups.push(d.group);
        }
    });

    //Create the json data from the csv data
    var processed_data = groups.map(function (g) {

        return {
            group: g,
            values: data.filter(function (d) {
                return d.group === g;
            }).map(function (e) {
                return {
                    value: +e.value,
                    variable: e.variable,
                    label: e.label
                };
            })
        };
    });

    return processed_data;

};

var group_label_value_parser = function (data) {

    var processed_data;

    if (data[0].group === undefined) {

        processed_data = data.map(function (d) {
            return {label: d.label, value: +d.value};

        });

    } else {

        var groups = [];
        data.map(function (d) {
            if (groups.indexOf(d.group) === -1) {
                groups.push(d.group);
            }
        });

        //Create the json data from the csv data
        processed_data = groups.map(function (g) {
            var y0 = 0;
            return {
                group: g,
                values: data.filter(function (d) {
                    return d.group === g;
                }).map(function (e) {
                    return {
                        value: +e.value,
                        label: e.label,
                        y0: y0,
                        y1: y0 += +e.value
                    };
                })
            };
        });


    }

    return processed_data;

};
//Global formatting functions

//Add span around text for highlighting
function highlight(d){
  return   "<span class = 'highlighted'>" + d + "</span>";
};

//Get max string length in an array of strings

function max_string_length(strings){

  var lengths = strings.map(function(d){return d.length})

  return Math.max.apply(null, lengths);

}


var uni_format = function(d){
  var return_val;

  if (d > 999) {
    return_val = d3.format(".3s")(d);
  }
  else if (d > 100) {
    return_val = d3.format(".3r")(d);
  }
  else if (d >= 10) {
    if (Math.round(d) === d) {
      return_val = d3.format(".0f")(d);
    }
    else {
      return_val = d3.format(".1f")(d);
    }
  }
  else if (d > 1) {
    return_val = d3.format(".1f")(d);
  }
  else
  {
    return_val = d3.format(".1f")(d);
  }
  return return_val;

};


var uni_format_range = function(d){

  var min = d[0], max = d[1];
  console.log(min);
  console.log(max);

  if (min > - 1000 & max < 1000) {return d3.format(",.0f");}
  else {return d3.format(",.0f");}

}


var uni_format_axis = function(d){
  var return_val;
  if (d >= 1) {
    return_val = d3.format("s")(d);
  }
  else
  {
    return_val = d3.format("")(d);
  }
  return return_val;

};

var format_millions = function(d) {
  return Math.round(d / 1000) + "m";
};

var format_millions_2d = function(d) {
  return d3.format(".3r")(d / 1000) + "m";
};


var quarter_year = function(d) {

  var month = d3.time.format("%m")(d);
  var year = d3.time.format("%Y")(d);
  var quarter = parseInt(month) / 3;

  return "Q" + quarter + " " + year;

};


//Commentary function to be used in tool tips and on side bars

function cap_first_letter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

function lower_case(string) {
  return string.toLowerCase();
}

function unchanged(string) {
  return string;
}

function create_commentary(commentary_strings, embedded_vars, formats){


  var string_parts = commentary_strings.split("$");

  var text = "";

  embedded_vars.forEach(function(d, i){
    var formatter = (formats===undefined)? uni_format:formats[i];
    text = text + string_parts[i] + formatter(d);
  });

  return text;

}


function create_scale(data, d3_scale, padding) {

  var min = d3.min(data),
    max = d3.max(data);
  var range = max - min;
  var range_max_ratio = range / max;

  var scale = d3_scale;

  if (typeof d3_scale.rangePoints === "function") {
    scale.domain(data);
    var scale_type = "ordinal";
  } else {

    if (typeof data[0] === "number") {

      if (range_max_ratio < 0.25 || min < 0) {
        scale.domain([min - 0.1 * range, max + 0.1 * range]).nice;
      } else {
        scale.domain([0, max + 0.1 * range]).nice;
      }

      var scale_type = "linear";

    } else {

      scale.domain([min, max]).nice;

      if (data[0].constructor.name === "Date") {
        var scale_type = "datetime";
      } else {
        var scale_type = "nonlinear";
      }
    }

  }



  return {
    scale_func: scale,
    scale_type: scale_type
  };

}

//Data processing function

function build_chart(data, div, size, labels, csv_parser, inline_parser, draw) {


  if (typeof data === "object")

  {

    var processed_data = inline_parser(data);

    draw(processed_data, div, size, labels);

  } else

  {


    d3.csv(data, function(error, data) {

      var processed_data = csv_parser(data);
      draw(processed_data, div, size, labels);

    });

  }

}


function add_legend(svg, x, y, legend_data) {

  var legend_groups = svg.selectAll('.legend_item')
    .data(legend_data)
    .enter()
    .append('g')
    .attr('class', 'legend_item')
    .attr("transform", "translate(" + x + "," + y + ")");


  legend_groups.append("rect")
    .attr("width", 10)
    .attr("height", 10)
    .attr('class', function(d) {
      return ('legend_block ' + d.class);
    })
    .attr("x", 10)
    .attr("y", function(d, i) {
      return i * 20;
    })
    .attr("fill", function(d, i) {
      return d.colour;
    });

  legend_groups.append("text")
    .attr("x", 27)
    .attr("y", function(d, i) {
      return 8 + i * 20;
    })
    .text(function(d) {
      return d.label;
    });

}


function wrap(text, width) {
  text.each(function() {
    var text = d3.select(this),
        words = text.text().split(/\s+/).reverse(),
        word,
        line = [],
        lineNumber = 0,
        lineHeight = 1.1, // ems
        y = text.attr("y"),
        dy = parseFloat(text.attr("dy")),
        tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");
    while (word = words.pop()) {
      line.push(word);
      tspan.text(line.join(" "));
      if (tspan.node().getComputedTextLength() > width) {
        line.pop();
        tspan.text(line.join(" "));
        line = [word];
        tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
      }
    }
  });
}


function abbrev(text, max) {

  if (text.length > max) {
    text = text.substring(0, max - 3) + "...";
  }

  return text;

}

function minmax_across_groups(processed_data, variable) {

  y_values = processed_data.map(function(d) {
    return (d.values.map(function(e) {
      if (e.variable === variable) {
        return e.value;
      }
    }));
  });
  y_values = [].concat.apply([], y_values);

  return ([d3.min(y_values), d3.max(y_values)]);

}

function create_class_label(prefix, x){

  return prefix + "_" + x.replace(/[.,\/#!$%\^&\*;:{}=+\-_`~()]/g,"").replace(" ","");

}var AnimatedBarChart = function (processed_data, div, size, labels, scales) {

    var self = this;

    var margin = {
        top: 50,
        bottom: 80,
        right: 50,
        left: 60
    };

    BarChart.call(self, processed_data, div, size, labels, scales, margin);
    self.bar_width = self.width / self.processed_data.length;
    self.y_axis.tickFormat(d3.format(",%")).ticks(6);
    this.x_axis.tickSize(0);

    self.current_variable = "";

    self.tooltip_text = function (d) {
        return d3.format(".1%")(d.value) + " of " + d.category + " have access to a " + self.current_variable;
    }

    self.tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(self.tooltip_text);

};

AnimatedBarChart.prototype = Object.create(BarChart.prototype);

AnimatedBarChart.prototype.add_bars = function () {

    var self = this;

    self.chart_area.call(self.tip);

    //Customisations
    self.svg.attr("class", "glasseye_chart animated_barchart");

    //Get first Date
    var start_date = d3.min(self.processed_data[0].values.map(function(d) {
        return d.time;
    }));

    //Get first variable
    var start_variable = d3.min(self.processed_data[0].values.map(function(d) {
        return d.variable;
    }));

    var bars = self.chart_area.selectAll(".bar")
        .data(self.processed_data)
        .enter()
        .append("g")
        .attr("transform", function (d) {
            return "translate(" + (self.x(d.category) - self.bar_width * 0.4) + ", " + 0 + ")";
        });

    bars.append("rect")
        .attr("class", "bar")
        .attr("x", 0)
        .attr("y", function (d) {
            return self.y(d.values[0].value);
        })
        .attr("width", self.bar_width * 0.8)
        .attr("height", function (d) {
            return self.height - self.y(d.values[0].value);
        })
        .on('mouseover', self.tip.show)
        .on('mouseout', self.tip.hide);
    ;

    self.svg.append("text").attr("class", "context")
        .attr("y", self.height + self.margin.top + 60)
        .attr("x", self.margin.left + self.width / 2)
        .style("text-anchor", "middle")
        .text("At " + quarter_year(self.processed_data[0].values[0].time) + " for " + self.processed_data[0].values[0].variable);

    var max_string = d3.max(self.x.domain().map(function (d) {
        return d.length;
    }));
    var num_points = self.x.domain().length;

    if ((max_string * 5) > (1.5 * self.bar_width)) {
        self.chart_area.selectAll(".x_axis").selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-1em")
            .attr("dy", "-0.8em")
            .attr("transform", "rotate(-90)");
    }


    self.update_bars(start_date, start_variable);

    return this;

};


AnimatedBarChart.prototype.update_bars = function (time, variable) {

    var self = this;


    //Set variable so that it can be accessed by the tooltip
    self.current_variable = variable.toLowerCase();

    var filtered_bars = self.processed_data.map(function(d) {
        return {

            category: d.category,
            value: d.values.filter(function(e) {
                return (e.time.getTime() === time.getTime() & e.variable === variable);
            })[0].value
        };
    });

    self.chart_area.selectAll(".bar").data(filtered_bars)
     .transition()
     .duration(500)
     .attr("y", function (d){return self.y(d.value);})
     .attr("height", function (d){return self.height - self.y(d.value);});


    self.svg.selectAll(".context").text("In " + quarter_year(time) + " for " + variable);


};

AnimatedBarChart.prototype.add_title = function (title, subtitle) {

    var self = this;
    self.title = title;
    self.svg.append('text').attr("class", "title")
        .text(title)
        .attr("transform", "translate(" + (self.margin.left - 10) + ",20)");

    if (subtitle != undefined) {

        self.subtitle = subtitle;
        self.svg.append('text').attr("class", "subtitle")
            .text(subtitle)
            .attr("transform", "translate(" + (self.margin.left - 10) + ",35)");

    } else {
        self.subtitle = "";
    }

    return this;

};

AnimatedBarChart.prototype.redraw_barchart = function (title) {

    var self = this;

    //Delete the existing svg and commentary
    d3.select(self.div).selectAll("svg").remove();


    //Reset the size
    self.set_size();
    self.bar_width = self.width / self.processed_data.length;
    self.x = self.scales[0].scale_func.rangePoints([0, self.width], 1);
    self.y_axis = d3.svg.axis()
        .scale(self.y)
        .orient("left")
        .tickSize(-self.width, 0, 0)
        .tickFormat(d3.format("%")).ticks(6);


    //Redraw the chart
    self.add_svg().add_grid().add_bars().add_title(self.title, self.subtitle);

};


var AnimatedDonut = function(processed_data, div, size) {

  var self = this;

  margin = {
    top: 80,
    bottom: 130,
    left: 30,
    right: 30
  };

  GlasseyeChart.call(self, div, size, margin, 400);

  self.processed_data = processed_data;

  var total_value = d3.sum(processed_data.map(function(d) {
    return d.values[0].value;
  }));

  self.current_total = 1;

  self.tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
      return   uni_format(d.data.value) + " households"  + "<br>" + d3.format(".1%")(d.data.value/self.current_total) + " of the total";
    });

  var radius = self.width / 2;

  self.arc = d3.svg.arc()
    .outerRadius(radius - 10)
    .innerRadius(radius - 70);

  self.pie = d3.layout.pie()
    .sort(null)
    .value(function(d) {
      return d.value;
    });

};


AnimatedDonut.prototype = Object.create(GlasseyeChart.prototype);


AnimatedDonut.prototype.add_donut = function() {

  var self = this;

  var svg_donut = self.chart_area.append("g")
    .attr("transform", "translate(" + self.width / 2 + "," + self.height / 2 + ")");

  var color = d3.scale.ordinal()
    .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

  //Get first Date

  var start_date = d3.min(self.processed_data[0].values.map(function(d) {
    return d.time;
  }));

  //Create filtered data Set

  var filtered_donut = self.processed_data.map(function(d) {
    return {
      category: d.category,
      value: d.values[0].value
    };
  });

  svg_donut.call(self.tip);

  self.donut_arc = svg_donut.selectAll(".arc")
    .data(self.pie(filtered_donut))
    .enter().append("g")
    .attr("class", "arc");

  var existing_text;

  self.donut_path = self.donut_arc.append("path")
    .attr("d", self.arc)
    .attr("class", function(d, i) {
      return ("d_" + i + " " + create_class_label("d", d.data.category));
    })
    .attr("fill", function(d) {
      return color(d.data.category);
    })
    .on('mouseover', function(d, i) {
      /*existing_text  = self.svg.selectAll(".context").text();
      var text_line_1 = existing_text.substring(0, 11) + d3.format("%")(d.data.value/self.current_total) + " of households";
      var text_line_2  = "with " + existing_text.substring(15, existing_text.length);
      var text_line_3  = "are at lifestage " + d.data.group;
      self.svg.selectAll(".context").text(text_line_1);
      self.svg.selectAll(".context_2").text(text_line_2);
      self.svg.selectAll(".context_3").text(text_line_3);
      */
      self.tip.show(d);
    })
    .on('mouseout', function(d, i) {
      //self.svg.selectAll(".context").text(existing_text);
      self.tip.hide(d);
    });


  self.donut_text = self.donut_arc.append("text")
    .attr("transform", function(d) {
      return "translate(" + self.arc.centroid(d) + ")";
    })
    .attr("dy", ".35em")
    .style("text-anchor", "middle")
    .text(function(d) {
      if (d.endAngle - d.startAngle > 0.35) {
        return d.data.category;
      } else {
        return "";
      }
    });

  self.donut_path.transition()
    .duration(500)
    .attr("fill", function(d, i) {
      return color(d.data.category);
    })
    .attr("d", self.arc)
    .each(function(d) {
      this._current = d;
    });

  self.svg.append("text").attr("class", "context")
    .attr("y", self.height + self.margin.top + 70)
    .attr("x", self.margin.left + self.width / 2)
    .style("text-anchor", "middle");

  /*self.svg.append("text").attr("class", "context_2")
      .attr("y", self.height + self.margin.top + 75)
      .attr("x", self.margin.left + self.width / 2)
      .style("text-anchor", "middle");

  self.svg.append("text").attr("class", "context_3")
      .attr("y", self.height + self.margin.top + 90)
      .attr("x", self.margin.left + self.width / 2)
      .style("text-anchor", "middle");
  */

  self.update_donut(start_date, "No TV");


  return this;

};


AnimatedDonut.prototype.update_donut = function(time, variable) {

  var self = this;

  var color = d3.scale.ordinal()
    .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);


  var filtered_donut = self.processed_data.map(function(d) {

    return {

      category: d.category,
      value: d.values.filter(function(e) {
        return (e.time.getTime() === time.getTime() & e.variable === variable);
      })[0].value
    };
  });


  //Update tooltip

  self.current_total = d3.sum(filtered_donut.map(function(d){return d.value}));

  self.donut_path.data(self.pie(filtered_donut)).transition().duration(200).attrTween("d", arcTween);


  self.donut_text.data(self.pie(filtered_donut)).transition().duration(200).attr("transform", function(d) {
      return "translate(" + self.arc.centroid(d) + ")";
    })
    .attr("dy", ".35em")
    .style("text-anchor", "middle")
    .text(function(d) {
      return d.data.category;
    });

  function arcTween(a) {
    var i = d3.interpolate(this._current, a);
    this._current = i(0);
    return function(t) {
      return self.arc(i(t));
    };
  }

  self.svg.selectAll(".context").text("In " + quarter_year(time) + " for " + variable);




};

AnimatedDonut.prototype.add_title = function(title, subtitle) {

  var self = this;
  self.title = title;
  self.svg.append('text').attr("class", "title")
    .text(title)
    .attr("y", 20)
    .attr("x", self.margin.left + self.width / 2)
    .style("text-anchor", "middle");

  if (subtitle != undefined) {

    self.subtitle = subtitle;
    self.svg.append('text').attr("class", "subtitle")
        .text(subtitle)
        .attr("y", 35)
        .attr("x", self.margin.left + self.width / 2)
        .style("text-anchor", "middle");

  } else {
    self.subtitle = "";
  }

  return this;

};

AnimatedDonut.prototype.redraw_donut = function(title) {

  var self = this;

  //Delete the existing svg and commentary
  d3.select(self.div).selectAll("svg").remove();
  d3.select(self.div).selectAll("#venn_context").remove();

  //Reset the size
  self.set_size();

  var radius = self.width / 2;

  self.arc = d3.svg.arc()
    .outerRadius(radius - 10)
    .innerRadius(radius - 70);


  //Redraw the chart
  self.add_svg().add_donut().add_title(self.title, self.subtitle);

};
/**
 * Builds an AnimatedVenn object
 * @constructor
 * @param {array} processed_data Data that has been given a structure appropriate to the chart
 * @param {string} div The div in which the chart will be placed
 * @param {string} size The size (one of several preset sizes)
 */

var AnimatedVenn = function(processed_data, div, size) {

  var self = this;

  margin = {
    top: 60,
    bottom: 0,
    left: 5,
    right: 5
  };

  GlasseyeChart.call(self, div, size, margin, 250);

  self.processed_data = processed_data;

  self.venn_chart = venn.VennDiagram()
    .width(self.width)
    .height(self.height);

  self.tip = d3.select(self.div).append('div')
      .attr('class', 'hidden tooltip');

  self.interactive_text = function(d, existing_text) {

    var text, set_name = d.sets[0],
      set_size = d.size;

    //Get total number
    var all_sets = self.chart_area.selectAll("g")[0];
    var signed = all_sets.map(function(e) {
      if (e.__data__.sets.length == 2) {
        return -e.__data__.size;
      } else {
        return e.__data__.size;
      }
    });

    var total = signed.reduce(add, 0);

    if (d.sets.length == 1) {

      text = set_name + " was in " + uni_format(set_size * 1000) + " households making up " + d3.format(",.1%")(set_size / total) + " of all VOD subscribing households.";

      //$ was in $ households making up $ of all VOD subscribing households

    } else if (d.sets.length == 2) {

      var sub_1 = d.sets[0];
      var sub_2 = d.sets[1];

      //Work out set sizes
      var set_1_size = all_sets.filter(function(d) {
        return d.__data__.sets.length === 1 & d.__data__.sets[0] === sub_1;
      })[0].__data__.size;
      var set_2_size = all_sets.filter(function(d) {
        return d.__data__.sets.length === 1 & d.__data__.sets[0] === sub_2;
      })[0].__data__.size;

      text = "There were " + uni_format(set_size * 1000) + " households that subscribe to both " + sub_1 + " and " + sub_2 + " (" + d3.format(",.1%")(set_size / total) + " of all VOD subscribing households.)";
      //There were $ households that subscribe to both $ and $ ($ of all VOD subscribing households)
    } else {

      text = "There were " + uni_format(set_size * 1000) + " households that subscribe to all three. That's " + d3.format(",.1%")(set_size / total) + " of all VOD subscribing households.";
      //There were $ households that subscribe to all three. That's $ of all VOD subscribing households
    }

    function add(a, b) {
      return a + b;
    }

    return text;

  };

};

AnimatedVenn.prototype = Object.create(GlasseyeChart.prototype);

/**
 * Adds the SVGs corresponding to the AnimatedVenn object
 *
 * @method
 * @returns {object} The modified AnimatedVenn object
 */

AnimatedVenn.prototype.set_commentary = function(commentary_strings) {

  var self = this;

  self.interactive_text = function(d, existing_text) {

    var text, string_parts, set_name = d.sets[0],
        set_size = d.size;

    //Get total number
    var all_sets = self.chart_area.selectAll("g")[0];
    var signed = all_sets.map(function(e) {
      if (e.__data__.sets.length == 2) {
        return -e.__data__.size;
      } else {
        return e.__data__.size;
      }
    });

    var total = signed.reduce(add, 0);

    if (d.sets.length == 1) {

      string_parts = commentary_strings[0].split("$");

      text = string_parts[0] + set_name + string_parts[1] + uni_format(set_size * 1000) + string_parts[2] + d3.format(",.1%")(set_size / total) + string_parts[3];

      //$ was in $ households making up $ of all VOD subscribing households

    } else if (d.sets.length == 2) {

      var sub_1 = d.sets[0];
      var sub_2 = d.sets[1];

      //Work out set sizes
      var set_1_size = all_sets.filter(function(d) {
        return d.__data__.sets.length === 1 & d.__data__.sets[0] === sub_1;
      })[0].__data__.size;
      var set_2_size = all_sets.filter(function(d) {
        return d.__data__.sets.length === 1 & d.__data__.sets[0] === sub_2;
      })[0].__data__.size;

      string_parts = commentary_strings[1].split("$");
      text = string_parts[0] + uni_format(set_size * 1000) + string_parts[1] + sub_1 + string_parts[2] + sub_2 + string_parts[3] + d3.format(",.1%")(set_size / total) + string_parts[4];
      //There were $ households that subscribe to both $ and $ ($ of all VOD subscribing households)
    } else {

      string_parts = commentary_strings[2].split("$");
      text = string_parts[0] + uni_format(set_size * 1000) + string_parts[1] + d3.format(",.1%")(set_size / total) + string_parts[2];
      //There were $ households that subscribe to all three. That's $ of all VOD subscribing households
    }

    function add(a, b) {
      return a + b;
    }

    return text;

  };

  return self;

};

/**
 * Adds the SVGs corresponding to the AnimatedVenn object
 *
 * @method
 * @returns {object} The modified AnimatedVenn object
 */

AnimatedVenn.prototype.add_venn = function() {

  var self = this;


  //var start_date = new Date("March 31, 2014 00:00:00"); //Hardcoded at the moment - change later

  var start_date =  d3.max(self.processed_data.map(function(d){ return d.time}));

  var filtered_data = self.processed_data.filter(function(d) {
    return d.time.getTime() === start_date.getTime();
  })[0].venns;

  self.chart_area.datum(filtered_data).call(self.venn_chart);

  //Remove the labels

  self.chart_area.selectAll(".venn-area").selectAll("text").remove();

  self.svg.append("text").attr("class", "context")
    .attr("y", 40)
    .attr("x", self.margin.left + self.width / 2)
    .style("text-anchor", "middle")
      .text("In " + quarter_year(start_date) + " ");

  //Add the div for the commentary
  var div = d3.select(self.div).append("div").attr("id", "venn_context");
  div.append("div").attr("id", "commentary").style("font-size", "11px").html("Hover over the parts of the Venn diagram for information about the sizes of the groups.");

  //Add interactivity
  self.chart_area.selectAll("g")
    .on("mouseover", function(d, i) {

      //Set all charts back to no border-box
      self.chart_area.selectAll(".venn-area")
        .selectAll("path")
        .style("stroke-opacity", 0);

      // sort all the areas relative to the current item
      venn.sortAreas(self.chart_area, d);
      var selection = d3.select(this);
      selection.select("path").transition().duration(500)
        .style("stroke-opacity", 1);

      //update the text
      var existing_text = d3.selectAll("#commentary").html();
      d3.selectAll("#commentary").html(self.interactive_text(d, existing_text));

      //Add the tooltip

      var mouse = d3.mouse(self.chart_area.node()).map(function (d) {
        return parseInt(d);
      });

      self.tip.classed('hidden', false)
          .attr('style', 'left:' + (mouse[0]) +
              'px; top:' + (mouse[1] + 30) + 'px')
          .html(d.sets.join("<br>"));

    })
    .on("mouseout", function(d, i) {
      var selection = d3.select(this);
      selection.select("path").transition().duration(500)
        //  .style("fill-opacity", d.sets.length == 1 ? 0.5 : 0)
        .style("stroke-opacity", 0);

      self.tip.classed('hidden', true);

    });

  return this;

};

/**
 * Updates the Venn to show the overlaps at a specific time and with a spectific set highlighted. Also changes the commentary.
 * @method
 * @param {date} time The time for which the overlaps should be calculated
 * @param {string} variable The set which should be highlighted
 * @returns {object} The modified AnimatedVenn object
 */

AnimatedVenn.prototype.update_venn = function(time, variable) {

  var self = this;

  //Hide labels when set size = 0
  //self.chart_area.selectAll(".venn-area").selectAll("text").style("opacity", function(d){ return d.size>0?1:0;});

  var filtered_data = self.processed_data.filter(function(d) {
    return d.time.getTime() === time.getTime();
  })[0].venns;

  self.chart_area.datum(filtered_data).call(self.venn_chart);

  self.chart_area.selectAll(".venn-area")
    .selectAll("path")
    .style("stroke-opacity", 0);

  self.chart_area.selectAll(".venn-sets-" + variable)
    .selectAll("path")
    .style("stroke-opacity", 1);

  d3.selectAll("#commentary").html("Hover over the parts of the Venn diagram for information about the sizes of the groups.");
  self.svg.selectAll(".context").text("In " + quarter_year(time) + " ");

  return this;

};

/**
 * Adds a title to the Venn
 * @method
 * @param {string} title The title to be placed at the top of the Venn
 * @returns {object} The modified AnimatedVenn object
 */

AnimatedVenn.prototype.add_title = function(title) {

  var self = this;
  self.title = title;
  self.svg.append('text').attr("class", "title")
    .text(title)
    .attr("y", 20)
    .attr("x", self.margin.left + self.width / 2)
    .style("text-anchor", "middle");

  return this;

  if (subtitle != undefined) {

    self.subtitle = subtitle;
    self.svg.append('text').attr("class", "subtitle")
        .text(subtitle)
        .attr("y", 35)
        .attr("x", self.margin.left + self.width / 2)
        .style("text-anchor", "middle");

  } else {
    self.subtitle = "";
  }

};

/**
 * Redraws the Venn (for example after a resize of the div)
 * @method
 * @returns {object} The modified AnimatedVenn object
 */

AnimatedVenn.prototype.redraw_venn = function(title) {

  var self = this;

  //Delete the existing svg and commentary
  d3.select(self.div).selectAll("svg").remove();
  d3.select(self.div).selectAll("#venn_context").remove();

  //Reset the size
  self.set_size();
  self.venn_chart = venn.VennDiagram()
    .width(self.width)
    .height(self.height);

  //Redraw the chart
  self = self.add_svg().add_venn().add_title(self.title, self.subtitle);

};
/**
 * Builds an DrillableVenn object
 * @constructor
 * @param {array} processed_data Data that has been given a structure appropriate to the chart
 * @param {string} div The div in which the chart will be placed
 * @param {string} size The size (one of several preset sizes)
 */

var DrillableVenn = function (processed_data, div, size) {

    var self = this;

    margin = {
        top: 40,
        bottom: 0,
        left: 5,
        right: 5
    };

    GlasseyeChart.call(self, div, size, margin, 350);

    self.processed_data = processed_data;

    self.venn_chart = venn.VennDiagram()
        .width(self.width)
        .height(self.height);

    self.tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function (d) {
            return d3.format(".3n")(d.size);
        });

    self.current_level = "none";

    self.interactive_text = function (d, existing_text) {

        var text, set_name = d.sets[0],
            set_size = d.size;

        var qualifier = +(self.current_level === "none") ? "" : self.current_level;

        //Get total number
        var all_sets = self.chart_area.selectAll("g")[0].filter(function(d){return d.__data__.sets[0] != "500k"});
        console.log(all_sets);
        var signed = all_sets.map(function (e) {
            if (e.__data__.sets.length == 2) {
                return -e.__data__.size;
            } else {
                return e.__data__.size;
            }
        });

        var total = signed.reduce(add, 0);

        if (set_name === "500k") {

            text = "This circle represents 500k households and can be used as reference point when the Venn diagrams change in scale.";

        }

        else if (d.sets.length == 1) {

            text = set_name + " consoles are in " + uni_format(set_size) + " households, making up " + d3.format(",.1%")(set_size / total) + " of all households with " + qualifier + " games consoles.";

        } else if (d.sets.length == 2) {

            var sub_1 = d.sets[0];
            var sub_2 = d.sets[1];

            //Work out set sizes
            var set_1_size = all_sets.filter(function (d) {
                return d.__data__.sets.length === 1 & d.__data__.sets[0] === sub_1;
            })[0].__data__.size;
            var set_2_size = all_sets.filter(function (d) {
                return d.__data__.sets.length === 1 & d.__data__.sets[0] === sub_2;
            })[0].__data__.size;

            text = "There are " + uni_format(set_size) + " households that have both " + sub_1 + " and " + sub_2 + " consoles (" + d3.format(",.1%")(set_size / total) + " of all households with " + qualifier + " games consoles.)";
        } else {

            text = "There are " + uni_format(set_size) + " households that own all three types of consoles. That's " + d3.format(",.1%")(set_size / total) + " of all households with " + qualifier + " games consoles.";

        }

        function add(a, b) {
            return a + b;
        }

        return text;

    };

};

DrillableVenn.prototype = Object.create(GlasseyeChart.prototype);

/**
 * Adds the SVGs corresponding to the DrillableVenn object
 *
 * @method
 * @returns {object} The modified DrillableVenn object
 */

DrillableVenn.prototype.add_venn = function (parent) {

    var self = this;

    self.current_level = parent;

    var filtered_data = self.processed_data.filter(function (d) {
        return d.parent === parent;
    })[0].venns;


    self.chart_area.datum(filtered_data).call(self.venn_chart);

    d3.selectAll(".venn-area text").style("fill", "white");

    //Add the div for the commentary
    var parent_div = d3.selectAll("#chart_container");
    parent_div.selectAll("#venn_context_side").remove();

    var div = parent_div.append("div").attr("id", "venn_context_side");
    div.append("div").attr("id", "venn_instructions").html("<h1> Instructions </h1><ul><li>Click on each circle in the Venn diagram to drill a level further into the data.</li><li>Click again on a circle to return to  the top level.</li><li>The scale of the diagram is adjusted as you drill into the data however there is always a circle showing 500k households as a point of reference.</li></ul><h1>Commentary</h1>");
    div.append("div").attr("id", "commentary").html("Hover over a circle and commentary will appear here.");

    //Add interactivity
    self.chart_area.selectAll("g")
        .on("mouseover", function (d, i) {

            //Set all charts back to no border-box
            self.chart_area.selectAll(".venn-area")
                .selectAll("path")
                .style("stroke-opacity", 0);

            // sort all the areas relative to the current item
            venn.sortAreas(self.chart_area, d);
            var selection = d3.select(this);
            selection.select("path").transition().duration(500)
                .style("stroke-opacity", 1);

            //update the text
            var existing_text = d3.selectAll("#commentary").html();
            d3.selectAll("#commentary").html(self.interactive_text(d, existing_text));

        })
        .on("mouseout", function (d, i) {
            var selection = d3.select(this);
            selection.select("path").transition().duration(500)
                //  .style("fill-opacity", d.sets.length == 1 ? 0.5 : 0)
                .style("stroke-opacity", 0);

        })
        .on("click", function (d, i) {
            var selection = d3.select(this);

            if (parent == "none") {

                if (d.sets.length > 1) {
                    console.log("Cannot click on intersections");
                }
                else {
                    self.add_venn(d.sets[0]);
                }
            }
            else {
                self.add_venn("none");
            }
        });


    //}

    return self;

};


/**
 * Adds a title to the Venn
 * @method
 * @param {string} title The title to be placed at the top of the Venn
 * @returns {object} The modified AnimatedVenn object
 */

DrillableVenn.prototype.add_title = function (title) {

    var self = this;
    self.title = title;
    self.svg.append('text').attr("class", "title")
        .text(title)
        .attr("y", 20)
        .attr("x", self.margin.left + self.width / 2)
        .style("text-anchor", "middle");

    return this;

    if (subtitle != undefined) {

        self.subtitle = subtitle;
        self.svg.append('text').attr("class", "subtitle")
            .text(subtitle)
            .attr("y", 35)
            .attr("x", self.margin.left + self.width / 2)
            .style("text-anchor", "middle");

    } else {
        self.subtitle = "";
    }

};

/**
 * Redraws the Venn (for example after a resize of the div)
 * @method
 * @returns {object} The modified AnimatedVenn object
 */

DrillableVenn.prototype.redraw_venn = function (title) {

    var self = this;

    //Delete the existing svg and commentary
    d3.select(self.div).selectAll("svg").remove();
    d3.select(self.div).selectAll("#venn_context_side").remove();

    //Reset the size
    self.set_size();


    self.venn_chart = venn.VennDiagram()
        .width(self.width)
        .height(self.height);

    //Redraw the chart
    self = self.add_svg().add_venn(self.current_level).add_title(self.title, self.subtitle);

};
var Donut = function(processed_data, div, size) {

  margin = {
    top: 5,
    bottom: 5,
    left: 5,
    right: 5
  };

  GlasseyeChart.call(this, div, size, margin);

  this.processed_data = processed_data;

  var total_value = d3.sum(processed_data.map(function(d) {
    return d.value;
  }));

  this.tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
      return d.data.label + "<br><br>" + d.data.value + "<br><br>" + d3.format("%")(d.data.value / total_value);
    });

  var radius = this.height / 2;

  this.arc = d3.svg.arc()
    .outerRadius(radius - 10)
    .innerRadius(radius - 70);

  this.pie = d3.layout.pie()
    .sort(null)
    .value(function(d) {
      return d.value;
    });

};


Donut.prototype = Object.create(GlasseyeChart.prototype);

Donut.prototype.add_donut = function() {

  var svg_donut = this.chart_area.append("g")
    .attr("transform", "translate(" + this.width / 2 + "," + this.height / 2 + ")");

  var color = d3.scale.ordinal()
    .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

  svg_donut.call(this.tip);

  var g = svg_donut.selectAll(".arc")
    .data(this.pie(this.processed_data))
    .enter().append("g")
    .attr("class", "arc");

  g.append("path")
    .attr("d", this.arc)
    .style("fill", function(d) {
      return color(d.data.label);
    })
    .on('mouseover', this.tip.show)
    .on('mouseout', this.tip.hide);

  var arc = this.arc;

  g.append("text")
    .attr("transform", function(d) {
      return "translate(" + arc.centroid(d) + ")";
    })
    .attr("dy", ".35em")
    .style("text-anchor", "middle")
    .text(function(d) {
      if (d.endAngle - d.startAngle > 0.35) {
        return d.data.label;
      } else {
        return "";
      }
    });

};

function donut(data, div, size) {

  var inline_parser = function(data) {

    processed_data = [];

    for (i = 0; i < data.values.length; i++) {
      data_item = {
        "label": data.labels[i],
        "value": +data.values[i]
      };
      processed_data.push(data_item);

    }

    return processed_data;

  };

  var csv_parser = function(data) {
    return data;
  };

  var draw = function(processed_data, div, size) {

    var glasseye_chart = new Donut(processed_data, div, size);

    glasseye_chart.add_svg().add_donut();

  };

  build_chart(data, div, size, undefined, csv_parser, inline_parser, draw);

}
var Force = function(processed_data, div, size) {

  var margin = (size === "full_page") ? {
    top: 5,
    bottom: 5,
    left: 100,
    right: 100
  } : {
    top: 5,
    bottom: 5,
    left: 50,
    right: 50
  };

  GlasseyeChart.call(this, div, size, margin, 300);

  this.processed_data = processed_data;

  //Set up the force layout
  this.force = d3.layout.force()
    .charge(-120)
    .linkDistance(30)
    .size([this.width, this.height]);

  this.tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
      return d.name;
    });

};


Force.prototype = Object.create(GlasseyeChart.prototype);

Force.prototype.add_force = function() {

  var color = d3.scale.category20();

  this.chart_area.call(this.tip);

  //Creates the graph data structure out of the json data
  this.force.nodes(this.processed_data.nodes)
    .links(this.processed_data.links)
    .start();

  //Create all the line svgs but without locations yet
  var link = this.chart_area.selectAll(".forcelink")
    .data(this.processed_data.links)
    .enter().append("line")
    .attr("class", "forcelink")
    .style("stroke-width", function(d) {
      return Math.sqrt(d.value);
    });

  //Do the same with the circles for the nodes - no
  var node = this.chart_area.selectAll(".forcenode")
    .data(this.processed_data.nodes)
    .enter().append("circle")
    .attr("class", "forcenode")
    .attr("r", 8)
    .style("fill", function(d) {
      return color(d.group);
    })
    .call(this.force.drag)
    .on('mouseover', this.tip.show)
    .on('mouseout', this.tip.hide);

  //Now we are giving the SVGs co-ordinates - the force layout is generating the co-ordinates which this code is using to update the attributes of the SVG elements
  this.force.on("tick", function() {
    link.attr("x1", function(d) {
        return d.source.x;
      })
      .attr("y1", function(d) {
        return d.source.y;
      })
      .attr("x2", function(d) {
        return d.target.x;
      })
      .attr("y2", function(d) {
        return d.target.y;
      });

    node.attr("cx", function(d) {
        return d.x;
      })
      .attr("cy", function(d) {
        return d.y;
      });
  });

};

function force(data, div, size) {

  var inline_parser = function(data) {
    return data;
  };

  var csv_parser = function(data) {
    return data;
  };

  var draw = function(processed_data, div, size) {

    var glasseye_chart = new Force(processed_data, div, size);

    glasseye_chart.add_svg().add_force();

  };

  build_chart(data, div, size, undefined, csv_parser, inline_parser, draw);


}
var Gantt = function(processed_data, div, size, scales) {

  this.div = div;
  this.processed_data = processed_data;

  GridChart.call(this, div, size, ["Time", "Tasks"], scales, {
    top: 20,
    bottom: 80,
    left: 80,
    right: 20
  });

  this.tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
      return Math.floor((d.end - d.start) / (1000 * 60 * 60 * 24)) + " days";
    });

  this.bar_width = this.width / processed_data.length;

};

Gantt.prototype = Object.create(GridChart.prototype);

Gantt.prototype.add_tasks = function() {

  var x_scale = this.x,
    y_scale = this.y,
    bar_width = this.bar_width;

  this.chart_area.call(this.tip);
  this.chart_area.selectAll(".task")
    .data(this.processed_data)
    .enter()
    .append("rect")
    .attr("class", "task")
    .attr("y", function(d) {
      return y_scale(d.task) - bar_width / 6;
    })
    .attr("x", function(d) {
      return x_scale(d.start);
    })
    .attr("height", this.bar_width / 3)
    .attr("width", function(d) {
      return x_scale(d.end) - x_scale(d.start);
    })
    .on('mouseover', this.tip.show)
    .on('mouseout', this.tip.hide);

  return this;

};

function gantt(data, div, size) {

  var inline_parser = function(data) {

    var parse_date = d3.time.format("%d/%m/%Y").parse;

    //Parse the dates
    data.forEach(function(d) {
      d.start = parse_date(d.start);
      d.end = parse_date(d.end);
    });


    data.sort(function(a, b) {
      return b.start - a.start;
    });

    return data;

  };


  var csv_parser = function(data) {

    //To be written

  };

  var draw = function(processed_data, div, size) {

    var starts = processed_data.map(function(d) {
      return d.start;
    });

    var ends = processed_data.map(function(d) {
      return d.end;
    });

    var x_values = starts.concat(ends);

    var y_values = processed_data.map(function(d) {
      return d.task;
    });

    var scales = [create_scale(x_values, d3.time.scale()), create_scale(y_values, d3.scale.ordinal())];


    var glasseye_chart = new Gantt(processed_data, div, size, scales);
    glasseye_chart.add_svg().add_grid().add_tasks();

  };

  build_chart(data, div, size, undefined, csv_parser, inline_parser, draw);

}
var LinePlot = function(processed_data, div, size, labels, scales) {

  GridChart.call(this, div, size, labels, scales);

  this.processed_data = processed_data;

  //Some customisations
  this.margin.left = 4;
  this.y_axis.tickFormat("");

  this.tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
      return d3.format(".3n")(d.y);
    });

  var x_scale = this.x,
    y_scale = this.y;

  this.line = d3.svg.line()
    .x(function(d) {
      return x_scale(d.x);
    })
    .y(function(d) {
      return y_scale(d.y);
    });

};

LinePlot.prototype = Object.create(GridChart.prototype);

LinePlot.prototype.add_line = function() {

  this.chart_area.call(this.tip);

  this.chart_area.append("path")
    .datum(this.processed_data)
    .attr("class", "line")
    .attr("d", this.line);

  var x_scale = this.x,
    y_scale = this.y;

  this.chart_area.selectAll("line_points")
    .data(this.processed_data)
    .enter()
    .append("circle")
    .attr("class", "line_points")
    .attr("cx", function(d) {
      return x_scale(d.x);
    })
    .attr("cy", function(d) {
      return y_scale(d.y);
    })
    .attr("r", 10)
    .attr("opacity", 0)
    .on('mouseover', this.tip.show)
    .on('mouseout', this.tip.hide);

  return this;

};

function lineplot(data, div, size, labels) {


  var inline_parser = function(data) {

    var processed_data = [];

    for (i = 0; i < data.x.length; i++) {
      data_item = {
        "x": +data.x[i],
        "y": +data.y[i]
      };
      processed_data.push(data_item);
    }

    return processed_data;
  };

  var csv_parser = function(data) {

    var processed_data = data.map(function(d) {
      return {
        x: +d.x,
        y: +d.y
      };
    });

    return processed_data;

  };

  var draw = function draw_lineplot(processed_data, div, size, labels) {

    var x_values = processed_data.map(function(d) {
      return d.x;
    });
    var y_values = processed_data.map(function(d) {
      return d.y;
    });
    var scales = [create_scale(x_values, d3.scale.linear()), create_scale(y_values, d3.scale.linear())];
    var glasseye_chart = new LinePlot(processed_data, div, size, labels, scales);
    glasseye_chart.add_svg().add_grid().add_line();

  };

  build_chart(data, div, size, labels, csv_parser, inline_parser, draw);

}


function lineplot(data, div, size, labels) {


  var inline_parser = function(data) {

    var processed_data = [];

    for (i = 0; i < data.x.length; i++) {
      data_item = {
        "x": +data.x[i],
        "y": +data.y[i]
      };
      processed_data.push(data_item);
    }

    return processed_data;
  };

  var csv_parser = function(data) {

    var processed_data = data.map(function(d) {
      return {
        x: +d.x,
        y: +d.y
      };
    });

    return processed_data;

  };

  var draw = function draw_lineplot(processed_data, div, size, labels) {

    var x_values = processed_data.map(function(d) {
      return d.x;
    });
    var y_values = processed_data.map(function(d) {
      return d.y;
    });
    var scales = [create_scale(x_values, d3.scale.linear()), create_scale(y_values, d3.scale.linear())];
    var glasseye_chart = new LinePlot(processed_data, div, size, labels, scales);
    glasseye_chart.add_svg().add_grid().add_line();

  };

  build_chart(data, div, size, labels, csv_parser, inline_parser, draw);

}
function treemap(data, div, size) {

  var inline_parser = function(data) {
    return data;
  }

  var csv_parser = function(data) {
    //Needs to be written
  }

  var draw = function(processed_data, div, size) {

    var w = 300,
      h = 400,
      x = d3.scale.linear().range([0, w]),
      y = d3.scale.linear().range([0, h]),
      color = d3.scale.category20c(),
      root,
      node;

    var treemap = d3.layout.treemap()
      .round(false)
      .size([w, h])
      .sticky(true)
      .value(function(d) {
        return d.size;
      });

    var svg = d3.select(div)
      .append("svg:svg")
      .attr("width", w)
      .attr("height", h)
      .append("svg:g")
      .attr("transform", "translate(.5,.5)");

    var node = root = data;

    var nodes = treemap.nodes(root)
      .filter(function(d) {
        return !d.children;
      });

    var cell = svg.selectAll("g")
      .data(nodes)
      .enter().append("svg:g")
      .attr("class", "cell")
      .attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")";
      })
      .on("click", function(d) {
        return zoom(node == d.parent ? root : d.parent);
      });


    cell.append("svg:rect")
      .attr("width", function(d) {
        return d.dx - 1;
      })
      .attr("height", function(d) {
        return d.dy - 1;
      })
      .style("fill", function(d) {
        return color(d.parent.name);
      });

    cell.append("svg:text")
      .attr("x", function(d) {
        return d.dx / 2;
      })
      .attr("y", function(d) {
        return d.dy / 2;
      })
      .attr("dy", ".35em")
      .attr("text-anchor", "middle")
      .text(function(d) {
        return d.name;
      });
      //.style("opacity", function(d) { d.w = this.getComputedTextLength(); return d.dx > d.w ? 1 : 0; })
      //.call(wrap, 80);


    d3.select(window).on("click", function() {
      zoom(root);
    });

    d3.select("select").on("change", function() {
      treemap.value(this.value == "size" ? size : count).nodes(root);
      zoom(node);
    });

    function size(d) {
      return d.size;
    }

    function count(d) {
      return 1;
    }

    function zoom(d) {
      var kx = w / d.dx,
        ky = h / d.dy;
      x.domain([d.x, d.x + d.dx]);
      y.domain([d.y, d.y + d.dy]);

      var t = svg.selectAll("g.cell").transition()
        .duration(d3.event.altKey ? 7500 : 750)
        .attr("transform", function(d) {
          return "translate(" + x(d.x) + "," + y(d.y) + ")";
        });

      t.select("rect")
        .attr("width", function(d) {
          return kx * d.dx - 1;
        })
        .attr("height", function(d) {
          return ky * d.dy - 1;
        })

      t.select("text")
        .attr("x", function(d) {
          return kx * d.dx / 2;
        })
        .attr("y", function(d) {
          return ky * d.dy / 2;
        });
      //.style("opacity", function(d) { return kx * d.dx > d.w ? 1 : 0; });

      node = d;
      d3.event.stopPropagation();
    }

  }

  build_chart(data, div, size, undefined, csv_parser, inline_parser, draw);

}


function simplot(data, div, size) {

  var inline_parser = function(data) {
    //To be written
  }

  var csv_parser = function(data) {

    //Read in the different varaiations and simulations
    var variations = [];
    data.map(function(d) {
      if (variations.indexOf(d.variation) === -1) {
        variations.push(d.variation)
      }
    });

    var simulations = [];
    data.map(function(d) {
      if (simulations.indexOf(d.sim_num) === -1) {
        simulations.push(d.sim_num)
      }
    });

    //Create the json data from the csv data
    var processed_data = variations.map(function(v) {

      return {
        variation: v,
        simulations: simulations.map(function(s) {
          return {
            simulation: +s,
            values: data.filter(function(d) {
              return d.variation === v && d.sim_num === s
            }).map(function(e) {
              return {
                value: +e.value,
                iter: +e.day
              }
            })
          }
        })
      }

    });

    var comp_data = {
      original_data: data,
      grouped_data: processed_data,
      variations: variations,
      simulations: simulations
    };

    return comp_data;

  }

  var draw = function(processed_data, div, size) {

    var glasseye_chart = new GlasseyeChart(div, size, {
      top: 20,
      bottom: 20,
      right: 100,
      left: 20
    });
    glasseye_chart.add_svg();

    var color = d3.scale.category20();

    //Set up the scales
    var x = d3.scale.linear()
      .range([0, glasseye_chart.width])
      .domain([d3.min(processed_data.original_data, function(d) {
        return +d["day"]
      }) - 10, d3.max(processed_data.original_data, function(d) {
        return +d["day"]
      })]);

    var y = d3.scale.linear()
      .range([glasseye_chart.height, 0])
      .domain([d3.min(processed_data.original_data, function(d) {
        return +d['value']
      }), d3.max(processed_data.original_data, function(d) {
        return +d['value']
      })]);

    //Set up the axes
    var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom")
      .tickSize(-glasseye_chart.height, 0, 0);

    var yAxis = d3.svg.axis()
      .scale(y)
      .tickSize(-glasseye_chart.width, 0, 0)
      .orient("left");

    var svg = glasseye_chart.chart_area;

    //Add the axes
    svg.append("g")
      .attr("class", "chart_grid")
      .attr("transform", "translate(0," + glasseye_chart.height + ")")
      .call(xAxis);

    svg.append("g")
      .attr("class", "chart_grid")
      .call(yAxis);

    //Create a path function
    var line = d3.svg.line()
      .interpolate("linear")
      .x(function(d) {
        return x(d.iter);
      })
      .y(function(d) {
        return y(d.value);
      });

    //var totalLength = width + 200; //At some point base this on path length

    //Add the simulation paths for each variation

    processed_data.grouped_data.forEach(function(v, j) {

      var path = svg.selectAll(".variations")
        .data(v.simulations)
        .enter()
        .append("g")
        .append("path")
        .attr("class", "line")
        .attr("d", function(d) {
          return line(d.values);
        })
        .style("stroke", function(d) {
          return color(v.variation);
        })
        .attr("opacity", function(d) {
          if (d.simulation === -1) {
            return 1
          } else {
            return 0.1
          }
        });


      path.each(function(d) {
          d.totalLength = this.getTotalLength();
        })
        .attr("stroke-dasharray", function(d) {
          return d.totalLength + " " + d.totalLength;
        })
        .attr("stroke-dashoffset", function(d) {
          return d.totalLength;
        })
        .transition()
        .delay(j * 7000)
        .duration(7000)
        .ease("linear")
        .attr("stroke-dashoffset", 0)
        .transition()
        .duration((processed_data.variations.length - 1 - j) * 7000)
        .attr("stroke-dashoffset", 0)
        .each("end", repeat);


      function repeat() {
        var path = d3.select(this);
        path.attr("stroke-dasharray", function(d) {
            return d.totalLength + " " + d.totalLength;
          })
          .attr("stroke-dashoffset", function(d) {
            return d.totalLength;
          })
          .transition()
          .delay(j * 7000)
          .duration(7000)
          .ease("linear")
          .attr("stroke-dashoffset", 0)
          .transition()
          .duration((processed_data.variations.length - 1 - j) * 7000)
          .attr("stroke-dashoffset", 0)
          .each("end", repeat);
      }


    });


    if (processed_data.variations.length > 1) {

      add_legend(svg, glasseye_chart.width + glasseye_chart.margin.left, glasseye_chart.margin.top, processed_data.variations.map(function(v) {
        return {
          "label": v,
          "colour": color(v)
        }
      }));
    }
  }

  build_chart(data, div, size, undefined, csv_parser, inline_parser, draw);

}

function dot_plot(file, div, size) {

  //Set up the layout variables

  var svg_width = 650,
    svg_height = 400;

  var margin = {
      top: 20,
      right: 250,
      bottom: 110,
      left: 30
    },
    width = svg_width - margin.left - margin.right,
    height = svg_height - margin.top - margin.bottom;

  var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
      return d.value;
    })


  d3.csv(file, function(error, data) {


    //Set up color scales
    var color = d3.scale.category10()

    //Read in the different varaiations and simulations
    var groups = [];
    data.map(function(d) {
      if (groups.indexOf(d.group) === -1) {
        groups.push(d.group)
      }
    });


    //Read in the different varaiations and simulations
    var variables = [];
    data.map(function(d) {
      if (variables.indexOf(d.variable) === -1) {
        variables.push(d.variable)
      }
    });


    //Create the json data from the csv data
    var processed_data = groups.map(function(g) {

      return {
        group: g,
        values: data.filter(function(d) {
          return d.group === g
        }).map(function(e) {
          return {
            value: +e.value,
            variable: e.variable
          }
        })
      }
    });


    //This where we add the ordinal scales

    var min_y = d3.min(data, function(d) {
        return +d['value']
      }),
      max_y = d3.max(data, function(d) {
        return +d['value']
      }),
      range_y = max_y - min_y;

    //Work out the ratio of the range of y to max_y

    var range_max_ratio = range_y / max_y;

    var y = d3.scale.linear()
      .range([height, 0]);

    if (range_max_ratio < 0.3) {
      y.domain([min_y - 0.1 * range_y, max_y + 0.1 * range_y]).nice;
    } else {
      y.domain([0, max_y]).nice;
    }


    //Set up the scales
    var x = d3.scale.ordinal()
      .rangePoints([0, width], 1)
      .domain(variables);

    //Set up the axes
    var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom")
      .tickSize(-height, 0, 0)
      .tickFormat(function(d) {
        if (d.length > 15) {
          return d.substring(0, 15) + "..";
        } else {
          return d;
        }
      });

    var yAxis = d3.svg.axis()
      .scale(y)
      .tickSize(-width, 0, 0)
      .orient("left");

    //Add the svg
    var svg = d3.select(div).append("svg")
      .attr("width", svg_width)
      .attr("height", svg_height)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.call(tip);

    //Add the axes
    svg.append("g")
      .attr("class", "chart_grid")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
      .selectAll("text")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", ".15em")
      .attr("transform", "rotate(-90)");

    svg.append("g")
      .attr("class", "chart_grid")
      .call(yAxis);


    //Add the simulation paths for each variation
    processed_data.forEach(function(v, j) {


      svg.selectAll(".dot")
        .data(v.values)
        .enter()
        .append("circle")
        .attr("cx", function(d) {
          return x(d.variable)
        })
        .attr("cy", function(d) {
          return y(d.value)
        })
        .attr("r", 6)
        .attr("fill", function(d) {
          return color(v.group)
        })
        .attr("opacity", 0.5)
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);



    });

    if (groups.length > 1) {
      add_legend(svg, width + margin.left, margin.top, groups.map(function(v) {
        return {
          "label": v,
          "colour": color(v)
        }
      }));
    }
  });

  //Put

  //ordinal.rangePoints(interval[, padding])

}
var ScatterPlot = function(processed_data, div, size, labels, scales) {

  GridChart.call(this, div, size, labels, scales);

  this.processed_data = processed_data;


  this.tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
      return d3.format(".3n")(d.y);
    });

  var x_scale = this.x,
    y_scale = this.y;

};

ScatterPlot.prototype = Object.create(GridChart.prototype);

ScatterPlot.prototype.add_points = function() {

  this.chart_area.call(this.tip);

  this.chart_area.append("path")
    .datum(this.processed_data)
    .attr("class", "line")
    .attr("d", this.line);

  var x_scale = this.x,
    y_scale = this.y;

  this.chart_area.selectAll("points")
    .data(this.processed_data)
    .enter()
    .append("circle")
    .attr("class", "points")
    .attr("cx", function(d) {
      return x_scale(d.x);
    })
    .attr("cy", function(d) {
      return y_scale(d.y);
    })
    .attr("r", 3)
    .on('mouseover', this.tip.show)
    .on('mouseout', this.tip.hide);

  return this;

};

function scatterplot(data, div, size, labels) {


  var inline_parser = function(data) {

    var processed_data = [];

    for (i = 0; i < data.x.length; i++) {
      data_item = {
        "x": +data.x[i],
        "y": +data.y[i]
      };
      processed_data.push(data_item);
    }

    return processed_data;
  };

  var csv_parser = function(data) {

    var processed_data = data.map(function(d) {
      return {
        x: +d.x,
        y: +d.y,
        point_label: d.label
      };
    });

    return processed_data;

  };

  var draw = function draw_scatterplot(processed_data, div, size, labels) {

    var x_values = processed_data.map(function(d) {
      return d.x;
    });
    var y_values = processed_data.map(function(d) {
      return d.y;
    });
    var scales = [create_scale(x_values, d3.scale.linear()), create_scale(y_values, d3.scale.linear())];
    var glasseye_chart = new ScatterPlot(processed_data, div, size, labels, scales);
    glasseye_chart.add_svg().add_grid().add_points();

  };

  build_chart(data, div, size, labels, csv_parser, inline_parser, draw);

}
var Thermometers = function(processed_data, div, size, labels, scales) {

  var self = this;

  var margin = {
    top: 50,
    bottom: 80,
    right: 50,
    left: 50
  };

  BarChart.call(self, processed_data, div, size, labels, scales, margin);
  self.bar_width = self.width/7;
  self.y_axis.tickFormat(d3.format("0%")).ticks(6).tickSize(6);

};

Thermometers.prototype = Object.create(BarChart.prototype);

Thermometers.prototype.add_thermometers = function() {

  var self = this;

  self.chart_area.call(self.tip);

  //Customisations
  self.svg.attr("class", "glasseye_chart thermometers");


  var therm = self.chart_area.selectAll(".thermometer")
    .data(self.processed_data)
    .enter()
    .append("g")
    .attr("class", "thermometer")
    .attr("transform", function(d) {
      return "translate(" + (self.x(d.category) - self.bar_width / 4) + ", " + 0 + ")";
    });


  var therm_width = self.bar_width / 2;
  var merc_prop = 0.8;

  therm.append("rect")
    .attr("class", "glass")
    .attr("width", therm_width)
    .attr("height", self.height);

  therm.append("rect")
    .attr("class", "glass-gap")
    .attr("x", therm_width * (1 - merc_prop) / 2)
    .attr("width", therm_width * merc_prop)
    .attr("height", self.height);

  therm.append("text")
    .attr("class", "therm_reading")
    .text(d3.format("%")(0))
    .attr("transform", "translate(" + (self.bar_width) + ", " + self.height / 2 + ")");

  therm.append("rect")
    .attr("class", "mercury")
    .attr("x", self.bar_width / 8)
    .attr("y", self.y(0))
    .attr("width", self.bar_width / 4)
    .attr("height", self.height - self.y(0));
  self.svg.append("text").attr("class", "context")
    .attr("y", self.height + self.margin.top + 60)
    .attr("x", self.margin.left + self.width / 2)
    .style("text-anchor", "middle");

  return this;

};

Thermometers.prototype.update_thermometers = function(time, variable) {

  var self = this;
  self.chart_area.selectAll(".mercury")
    //.attr("class", function(d,i){return("mercury d_"+ i)})
    .transition()
    .duration(500)
    .attr("y", function(d) {
      var filtered = d.values.filter(function(e) {
        return e.time.getTime() === time.getTime() & e.variable === variable;
      });
      return self.y(filtered[0].value);
    })
    .attr("height", function(d) {
      var filtered = d.values.filter(function(e) {
        return e.time.getTime() === time.getTime() & e.variable === variable;
      });

      return self.height - self.y(filtered[0].value);
    });

  self.chart_area.selectAll(".therm_reading")
    .text(function(d) {
      var filtered = d.values.filter(function(e) {
        return e.time.getTime() === time.getTime() & e.variable === variable;
      });
      return d3.format("%")(filtered[0].value);
    });

  self.svg.selectAll(".context").text("In " + quarter_year(time) + " for " + variable + " households");



};

Thermometers.prototype.add_title = function(title, subtitle) {

  var self = this;
  self.title = title;
  self.svg.append('text').attr("class", "title")
    .text(title)
      .attr("y", 20)
      .attr("x", self.margin.left + self.width / 2)
      .style("text-anchor", "middle");

  if (subtitle != undefined) {

    self.subtitle = subtitle;
    self.svg.append('text').attr("class", "subtitle")
        .text(subtitle)
        .attr("y", 35)
        .attr("x", self.margin.left + self.width / 2)
        .style("text-anchor", "middle");

  } else {
    self.subtitle = "";
  }

  return this;

};


Thermometers.prototype.redraw_thermometer = function(title) {

  //Note no longer uses argument!

  var self = this;

  //Delete the existing svg and commentary
  d3.select(self.div).selectAll("svg").remove();

  //Reset the size
  self.set_size();
  self.bar_width = self.width /7;
  self.x = self.scales[0].scale_func.rangePoints([0, self.width], 1);

  //Redraw the chart
  self.add_svg().add_grid().add_thermometers().add_title(self.title, self.subtitle);

};

function thermometers(data, div, size) {

  var inline_parser = function(data) {

    processed_data = [];

    for (i = 0; i < data.value.length; i++) {
      data_item = {
        "category": data.category[i],
        "value": +data.value[i]
      };
      processed_data.push(data_item);

    }

    return processed_data;

  };

  var csv_parser = function(data) {

    var parse_date = d3.time.format("%d/%m/%Y").parse;
    var processed_data = data.map(function(d) {
      return {
        category: d.category,
        filter: d.filter,
        value: d.value,
        time: parse_date(d.time)
      };
    });

    return processed_data;

  };

  var draw = function(processed_data, div, size) {

    var x_values = processed_data.map(function(d) {
      return d.category;
    });
    var y_values = processed_data.map(function(d) {
      return d.value;
    });

    var scales = [create_scale(x_values, d3.scale.ordinal()), create_scale(y_values, d3.scale.linear())];

    var glasseye_chart = new Thermometers(processed_data, div, size, ["category", "value"], scales);

    glasseye_chart.add_svg().add_grid().add_thermometers();

  };

  build_chart(data, div, size, undefined, csv_parser, inline_parser, draw);


}
/**
 * Builds an TimeSeries object
 * @constructor
 * @param {array} processed_data Data that has been given a structure appropriate to the chart
 * @param {string} div The div in which the chart will be placed
 * @param {string} size The size (one of several preset sizes)
 * @param {array} labels An array containing the labels of the x and y axes
 * @param {object} scales An object describing the x and y scales
 * @param {function} tooltip_function A function that is called when the tooltip is on any of the points on the time series charts)
 */

var TimeSeries = function(processed_data, div, size, labels, scales, tooltip_function) {

  var self = this;

  var margin = {
    top: 50,
    bottom: 80,
    right: 30,
    left: 130
  };

  GridChart.call(self, div, size, undefined, scales, margin);

  self.processed_data = processed_data;
  self.tooltip_function = (tooltip_function===undefined)?function(time, variable){}:tooltip_function;

  //Some customisations
  self.y_axis.ticks(4).tickFormat(uni_format_axis).tickSize(0);
  self.x_axis.tickFormat(d3.time.format("%Y")).ticks(d3.time.month, 1).tickSize(6, 0).tickPadding(10);

  self.tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
      return quarter_year(d.time) + "<br>" + d.group + "<br>" + ((d.variable==="share")? d3.format(".1%")(d.value): self.tooltip_formtter(d.value));
    });

  //Reorder processed data in order of max value
  //self.processed_data =  self.processed_data.sort(function(a,b){return a.group < b.group});


  //Function to create line path
  self.line = d3.svg.line()
    .x(function(d) {
      return self.x(d.time);
    })
    .y(function(d) {
      return self.y(d.value);
    });

  //Function to create areas
  self.area = d3.svg.area()
    .x(function(d) {
      return self.x(d.time);
    })
    .y0(self.height)
    .y1(function(d) {
      return self.y(d.value);
    });

  //Function to create stacked areas
  self.area_stacked = d3.svg.area()
    .x(function(d) {
      return self.x(d.time);
    })
    .y0(function(d) {
      return self.y(d.y0);
    })
    .y1(function(d) {
      return self.y(d.y0 + d.y);
    });

  //Stacked layout
  self.stack = d3.layout.stack()
    .x(function(d) {
      return d.time;
    })
    .y(function(d) {
      return d.value;
    })
    .values(function(d) {
      return d.values;
    }).order("reverse");



  self.color = d3.scale.ordinal()
      .range(colorbrewer.RdYlBu[self.processed_data.length]);

};

TimeSeries.prototype = Object.create(GridChart.prototype);

/**
 * Adds the SVGs that create the times series graph
 * @method
 * @returns {object} The modified TimeSeries object
 */

TimeSeries.prototype.add_timeseries = function() {

  var self = this;

  self.chart_area.call(self.tip);

  //Filter the data
  self.filtered_data = self.processed_data.map(function(g) {
    return {
      group: g.group,
      values: g.values.filter(function(e) {
        return e.variable === "absolute";
      })
    };
  });


  self.chart_area.selectAll(".groups")
    .data(self.filtered_data)
    .enter()
    .append("path")
    .attr("stroke", function(d) {
      return (self.color(d.group));
    })
    .attr("class", function(d, i) {
      return ("timeseries_line c_" + i + " " + create_class_label("c", d.group));
    })
    .attr("d", function(d) {
      return self.line(d.values);
    });


  //Add the areas
  self.chart_area.selectAll(".timeseries_area")
    .data(self.filtered_data)
    .enter()
    .append("path")
    .attr("class", function(d, i) {
      return ("timeseries_area d_" + i + " " +create_class_label("d", d.group));
    })
    .attr("d", function(d) {
      return self.area(d.values);
    })
    .style("opacity", 0);

  self.create_linepoints("absolute");

  //Structure the x axis
  self.chart_area.selectAll("g.x_axis g.tick line")
    .attr("y2", function(d) {
      var month_no = d.getMonth();
      if (month_no % 12 === 0)
        return 6;
      else if (month_no % 3 === 0)
        return 2;
      else
        return 0;
    });


  var domain_in_days = (self.x.domain()[1] - self.x.domain()[0]) / (24 * 60 * 60 * 1000);

   self.chart_area.selectAll("g.x_axis g.tick text")
    .text(function(d, i) {
      var month_no = d.getMonth();
      if (month_no % 12 === 0) {
        return d3.time.format("%Y")(d);
      }
      else if (month_no % 3 === 0) {

        if (domain_in_days > 1200) {
          return "";
        } else {
          console.log(month_no/3);
          return "Q" + Math.floor(month_no/3);
        }
      } else {
        return "";
      }
    });


    if (typeof self.labels !== "undefined") {
      self.chart_area.append("g")
        .attr("class", "axis_label")
        .attr("transform", "translate(0, " + (self.height + self.margin.top) + ") rotate(-90)")
        .append("text")
        .text(self.labels[0]);
      }

  return this;

};

/**
 * Places transparent circles on the points of the time series so that they can trigger the tooltip
 * @method
 * @param {string} to_variable The variable that will be represented on the y axis
 * @returns {object} The modified TimeSeries object
 */

TimeSeries.prototype.create_linepoints = function(to_variable) {

  var self = this;

  //Create the line point data
  var line_points = self.filtered_data.map(function(d) {

    return (d.values.map(function(e) {
      return {
        time: e.time,
        value: e.value,
        group: d.group,
        variable: e.variable,
        y: e.y,
        y0: e.y0
      };
    }));
  });


  line_points = [].concat.apply([], line_points).filter(function(d) {
    return d !== undefined;
  });

  self.chart_area.selectAll(".line_points")
    .data(line_points)
    .enter()
    .append("g")
    .attr("class", "line_point_group")
    .append("circle")
    .attr("class", "line_points")
    .attr("cx", function(d) {
      return self.x(d.time);
    })
    .attr("cy", function(d) {
      if (to_variable === "share") {
        return self.y(d.y0 + d.y);
      } else {
        return self.y(d.value);
      }
    })
    .attr("r", 10)
    .on('mouseover', function(d) {
      self.tooltip_function(d.time, d.group);
      self.tip.show(d);
    })
    .on('mouseout', self.tip.hide);

};


/**
 * Changes the variable mapped to the y axis
 * @method
 * @param {string} to_variable The variable that will be represented on the y axis
 * @param {int} duration Duration of the transformation in milliseconds
 * @returns {object} The modified TimeSeries object
 */

TimeSeries.prototype.flip_variable = function(to_variable, duration) {

  var self = this;
  self.current_y_axis = to_variable;

  duration = (duration === undefined)? 1000: duration;

  //Filter the data
  self.filtered_data = self.processed_data.map(function(g) {
    return {
      group: g.group,
      values: g.values.filter(function(e) {
        return e.variable === to_variable;
      })
    };
  });

  //Update y axis
  self.y.domain(minmax_across_groups(self.processed_data, to_variable));

  //Some defaults
  var select_area = self.area;
  var area_opacity = 0;

  if (to_variable === "absolute") {

    self.y_axis.tickFormat(uni_format_axis).ticks(6);


  } else if (to_variable === "share") {

    self.y_axis.tickFormat(d3.format("0%")).ticks(6);
    self.filtered_data = self.stack(self.filtered_data);
    self.y.domain([0, 1]);
    select_area = self.area_stacked;
    area_opacity = 1;

  } else {
    self.y_axis.tickFormat(d3.format(".2n")).ticks(6);
  }

  self.chart_area.selectAll(".y_axis")
    .call(self.y_axis);

  //Update paths
  self.chart_area.selectAll(".timeseries_line")
    .data(self.filtered_data)
    .transition()
    .duration(duration)
    .attr("d", function(d) {
      if (to_variable === "share") {
        return self.line(d.values.map(function(e) {
            return {
              time: e.time,
              value: (e.y + e.y0)
            };
        }));
      } else {
        return self.line(d.values);
      }
    });

  self.chart_area.selectAll(".timeseries_area")
    .data(self.filtered_data)
    .transition()
    .duration(duration)
    .attr("d", function(d) {
      return select_area(d.values);
    })
    .style("opacity", area_opacity);


  //Update points
  self.chart_area.selectAll('.line_points').remove();

  //Create the line point data
  self.create_linepoints(to_variable);

  self.update_line_labels(to_variable);

  return this;

};

/**
 * Adds a legend to the TimeSeries object
 * @method
 * @returns {object} The modified TimeSeries object
 */

TimeSeries.prototype.add_legend = function() {

  var self = this;


  if (self.processed_data.length > 1) {
    add_legend(self.svg, 0, self.margin.top, self.processed_data.map(function(v, i) {
      return {
        "label": v.group,
        "colour": self.color(v.group),
        "class": create_class_label("d", v.group)
      };
    }));
  }

  return this;

};

/**
 * Adds a label to the TimeSeries object
 * @method
 * @param {string} title The title to be placed at the top of the chart
 * @returns {object} The modified TimeSeries object
 */

TimeSeries.prototype.add_title = function(title, subtitle) {

  var self = this;
  self.title = title;
  self.svg.append('text').attr("class", "title")
    .text(title)
    .attr("transform", "translate(" + (self.margin.left - 10) + ",20)");

  if (subtitle != undefined) {

    self.subtitle = subtitle;
    self.svg.append('text').attr("class", "subtitle")
        .text(subtitle)
        .attr("transform", "translate(" + (self.margin.left - 10) + ",35)");

  }

  return this;

};

/**
 * Adds labels at the end of each line (as an alretantive to having a legend)
 * @method
 * @returns {object} The modified TimeSeries object
 */

TimeSeries.prototype.add_line_labels = function() {

  var self = this;

  self.chart_area.attr("transform", "translate(50,50)");

  var end_point = self.x.domain()[1].getTime();

  var end_point_data = self.processed_data.map(function(d){
    return {
      group: d.group,
      value: d.values.filter(function(e) { return e.time.getTime()===end_point && e.variable==="absolute";})[0].value
    };
  });

  self.chart_area.selectAll(".line_labels")
  .data(end_point_data)
  .enter()
  .append("text")
  .attr("class", "line_labels")
  .attr("x", self.width+10)
  .attr("y", function(d){return self.y(d.value);})
  .text(function(d){return d.group;});

  return this;

};

/**
 * Updates the labels of the lines as they move
 * @method
 * @returns {object} The modified TimeSeries object
 */

TimeSeries.prototype.update_line_labels = function(variable) {

  var self = this;

  var end_point = self.x.domain()[1].getTime();

  var end_point_data = self.processed_data.map(function(d){
    return {
      group: d.group,
      value: d.values.filter(function(e) { return e.time.getTime()===end_point && e.variable===variable;})[0].value
    };
  });


  self.chart_area.selectAll(".line_labels")
  .transition()
  .duration(1000)
  .attr("y", function(d, i){return self.y(end_point_data[i].value);});

};

/**
 * Redraws the time series (for example after a resize of the div)
 * @method
 * @returns {object} The modified TimeSeries object
 */

TimeSeries.prototype.redraw_timeseries = function(title) {

  var self = this;

  //Delete the existing svg and commentary
  d3.select(self.div).selectAll("svg").remove();

  //Reset the size
  self.set_size();

  if (self.scales[0].scale_type === "ordinal") {
    self.x = self.scales[0].scale_func.rangePoints([0, self.width], 1);
  } else {
    self.x = self.scales[0].scale_func.range([0, self.width]);
  }

    //Commented out as it seemed to be affecting the tick marks and I con't remember what it does!
    //self.x_axis = d3.svg.axis()
    //  .scale(self.x);


  var current_y_axis = (self.current_y_axis === undefined) ? "absolute": self.current_y_axis;

  self.y.domain(minmax_across_groups(self.processed_data, current_y_axis));

  //Redraw the chart
  self.add_svg().add_grid().add_timeseries().add_legend().add_title(self.title, self.subtitle).flip_variable(current_y_axis, 0);

};


/**
 * Builds a TimeSeries object
 * @param {array} data Either the path to a csv file or inline data in glasseye
 * @param {string} div The div in which the chart will be placed
 * @param {string} size The size (one of several preset sizes)
 * @param {array} labels An array containing the labels of the x and y axes
 */


function timeseries(data, div, size, labels) {


  var inline_parser = function(data) {

    return data;

  };

  var csv_parser = function(data) {

    //Read in the different groups
    var groups = [];
    data.map(function(d) {
      if (groups.indexOf(d.group) === -1) {
        groups.push(d.group);
      }
    });


    //Try some date formats
    var parse_date= d3.time.format("%d/%m/%Y").parse;

    //Create the json data from the csv data
    var processed_data = groups.map(function(g) {

      return {
        group: g,
        values: data.filter(function(d) {
          return d.group === g;
        }).map(function(e) {
          return {
            value: +e.value,
            time: parse_date(e.time),
            variable: e.variable
          };
        })
      };
    });

    return processed_data;

  };

  var draw = function draw_timeseries(processed_data, div, size, labels) {

    var x_values = [],
      y_values = [];

    x_values = processed_data.map(function(d) {
      return (d.values.map(function(e) {
        return e.time;
      }));
    });
    x_values = [].concat.apply([], x_values);

    y_values = processed_data.map(function(d) {
      return (d.values.map(function(e) {
        return e.value;
      }));
    });
    y_values = [].concat.apply([], y_values);

    var tooltip_function = function(time, variable) {

    }

    var scales = [create_scale(x_values, d3.time.scale()), create_scale(y_values, d3.scale.linear())];
    var glasseye_chart = new TimeSeries(processed_data, div, size, labels, scales, tooltip_function);

    glasseye_chart.add_svg().add_grid().add_timeseries().add_legend();

  };

  build_chart(data, div, size, labels, csv_parser, inline_parser, draw);

}
var Tree = function(processed_data, div, size) {

  var margin = (size === "full_page") ? {
    top: 5,
    bottom: 5,
    left: 100,
    right: 100
  } : {
    top: 5,
    bottom: 5,
    left: 50,
    right: 50
  };

  GlasseyeChart.call(this, div, size, margin, 300);

  this.processed_data = processed_data;

  var cluster = d3.layout.tree()
    .size([this.height, this.width]);

  this.nodes = cluster.nodes(processed_data),
    this.links = cluster.links(this.nodes);

  this.diagonal = d3.svg.diagonal()
    .projection(function(d) {
      return [d.y, d.x];
    });

};

Tree.prototype = Object.create(GlasseyeChart.prototype);

Tree.prototype.add_tree = function() {

  var link = this.chart_area.selectAll(".treelink")
    .data(this.links)
    .enter().append("path")
    .attr("class", "treelink")
    .attr("d", this.diagonal);

  var node = this.chart_area.selectAll(".treenode")
    .data(this.nodes)
    .enter().append("g")
    .attr("class", "treenode")
    .attr("transform", function(d) {
      return "translate(" + d.y + "," + d.x + ")";
    });

  node.append("circle")
    .attr("r", 4.5);

  var abbr_len = (this.size === "full_page") ? 20 : 10;

  node.append("text")
    .attr("dx", function(d) {
      return d.children ? -8 : 8;
    })
    .attr("dy", 3)
    .style("text-anchor", function(d) {
      return d.children ? "end" : "start";
    })
    .text(function(d) {
      return abbrev(d.name, abbr_len);
    });

};


function tree(data, div, size) {

  var inline_parser = function(data) {
    return data;
  };

  var csv_parser = function(data) {
    return data;
  };

  var draw = function(processed_data, div, size) {

    var glasseye_chart = new Tree(processed_data, div, size);

    glasseye_chart.add_svg().add_tree();

  };

  build_chart(data, div, size, undefined, csv_parser, inline_parser, draw);


}
var Venn = function(processed_data, div, size) {

  margin = {
    top: 5,
    bottom: 5,
    left: 5,
    right: 5
  };

  GlasseyeChart.call(this, div, size, margin);

  this.processed_data = processed_data;

  this.venn_chart = venn.VennDiagram()
    .width(this.width)
    .height(this.height);



};

Venn.prototype = Object.create(GlasseyeChart.prototype);

Venn.prototype.add_venn = function() {

  this.chart_area.datum(this.processed_data).call(this.venn_chart);

};


function venn(data, div, size) {

  var inline_parser = function(data) {
    return data;
  };

  var csv_parser = function(data) {
    return data;
  };

  var draw = function(processed_data, div, size) {


    var glasseye_chart = new Venn(processed_data, div, size);

    glasseye_chart.add_svg().add_venn();

  };

  build_chart(data, div, size, undefined, csv_parser, inline_parser, draw);

}
var Dial = function(processed_data, div, size, scales) {

  //Store arguments
  this.processed_data = processed_data;

  //Default parameters
  var pct_of_width = 0.55;

  //Inherit any attributes or functions of a parent class
  GlasseyeChart.call(this, div, size);

  //Any overides of parent attributes

  //Derive further attributes
  var dial_domain = scales[0].scale_func.domain();
  this.dial_radius = pct_of_width * this.width / 2;

  //Create functions or closures to be used in methods
  this.dial_scale = scales[0].scale_func.range([0, 359]);

  //Temp overide of range
  this.dial_scale.domain([-0.3, 0.1]).clamp(true);

  this.current_angle = this.dial_scale(-0.123);

  //Create the dial face data

  var angles = d3.range(0, 360, 30);

  var local_scale = this.dial_scale;

  this.dial_face_data = angles.map(function(d) {
    return {
      angle: d,
      value: local_scale.invert((d+180) % 360)
    };
  });

};

//Methods for the class. This is where svgs are created

//Inherit methods from parent
Dial.prototype = Object.create(GlasseyeChart.prototype);

//Method for adding svgs
Dial.prototype.add_dial = function() {

  //Store this locally so that it can reference in further functions
  var self = this;

  //Draw the chart
  var face = self.chart_area.append("g")
    .attr("transform", "translate(" + (self.width / 2) + ", " + (self.height / 2.5) + ")");

  face.append("svg").attr("width", self.dial_radius).attr("height", self.dial_radius).append("circle").attr("r", self.dial_radius).style("fill", "#990000");

  face.append("circle")
    .attr("class", "dial_face")
    .attr("r", self.dial_radius);

  face.append("circle")
      .attr("class", "dial_seg")
      .attr("r", self.dial_radius * 0.4)
      .attr("fill", "black");

  face.append("circle")
    .attr("class", "dial_centre")
    .attr("r", self.dial_radius * 0.05);

  function rotate_tween() {
    var i = d3.interpolate(0, self.current_angle);
    return function(t) {
      return "rotate(" + i(t) + ")";
    };
  }

  face.append("line")
    .attr("class", "dial_hand")
    .attr("x2", self.dial_radius * 0.7)
    .transition()
    .duration(this.current_angle / 360 * 5000)
    .attrTween("transform", rotate_tween);

  //Add ticks
  var dial_ticks = face.selectAll(".dial_ticks")
    .data(self.dial_face_data)
    .enter().append("g")
    .attr("transform", function(d) {
      return "rotate(" + d.angle + ") translate(" + -self.dial_radius + ", 0) ";
    });

  dial_ticks.append("line")
    .attr("x2", 7);

  dial_ticks.append("text")
  .style("text-anchor", "middle")
  .attr("class", "dial_tick_labels")
    .attr("dy", ".35em")
    .attr("transform", function(d) {
      return d.angle < 270 && d.angle > 90 ? "translate(20,0) rotate(-90) " : "translate(20,0) rotate(-90) ";
    })
    .text(function(d) {
      return d3.format(",.0f")(d.value*100);
    });

  //Add the counter

  self.chart_area.append("text")
  .attr("class", "dial_counter")
  .attr("transform", "translate(250," + (self.height / 2.5 +7) + ")")
  .text("")
  .style("text-anchor", "end")
  .transition()
  .delay(this.current_angle / 360 * 5000)
  .text("0%");


  //Return the object so that we can use chaining
  return self;

};


//Method for updating svgs
Dial.prototype.update_dial = function(group, variable) {

  //Store this locally so that it can reference in further functions
  var self = this;

  //If necessary filter the data
  var filtered_data = self.processed_data.filter(function(d) {
      return d.group === group;
    })[0].values
    .filter(function(e) {
      return e.variable === variable;
    })[0];

  //Update the chart
  var angle = self.dial_scale(filtered_data.value);
  var local_angle = self.current_angle;

  function rotate_tween() {
    var i = d3.interpolate(local_angle, angle);
    return function(t) {
      return "rotate(" + i(t) + ")";
    };
  }

  self.chart_area.selectAll(".dial_hand")
    .transition()
    .duration(1000)
    .attrTween("transform", rotate_tween);

  //Update the counter

  self.chart_area.selectAll(".dial_counter")
  .transition()
  .delay(1000)
  .text(d3.format("%")(filtered_data.value));

  //Return the object so that we can use chaining
  self.current_angle = angle;
  return self;

};


Dial.prototype.add_title = function(title) {

  var self = this;
  self.svg.append('text').attr("class", "title")
    .text(title)
    .style("text-anchor", "middle")
    .attr("transform", "translate(" + (self.margin.left + self.width/2) + ",20)");

  return this;

};


Dial.prototype.add_subtitle = function(subtitle) {

  var self = this;
  self.svg.append('text').attr("class", "subtitle")
    .text(subtitle)
    .style("text-anchor", "middle")
    .attr("transform", "translate(" + (self.margin.left + self.width/2) + ",40)");

  return this;

};

//wrapper function to process the data and draw the chart

/*

function x_chart(data, div, size) {

  //Define data parsers
  var inline_parser = function(data) {

    return processed_data;

  };

  var csv_parser = function(data) {

    return processed_data;

  };

  //Create draw function
  var draw = function(processed_data, div, size) {

    //Calculate values for scales

    //Create scales

    //Create new chart and chain methods

    var glasseye_chart = new XChart(processed_data, div, size);

    glasseye_chart.add_svg();

  };

  //Function that builds the chart based on whether the data is inline or from a file
  build_chart(data, div, size, undefined, csv_parser, inline_parser, draw);

}
*/
//A template for glasseye charts

/*
The chart object class.
Contains functions (including closures) and variables that describe the chart in the abstract.
No svg elements are created here.
Even where the chart can be implemented almost entirely by a closure, the closure is constructed
in the object and then executed (and modified) in the methods. This way we have framework that is flexible
enough fpr both techniques.
*/

var LogisticCurve = function(formula) {

  //Store arguments
  this.formula = formula.replace(/ /g, '');

  //Parse the formula
  var right_left = this.formula.split("=");

  var response = right_left[0];
  var explanatory = right_left[1].split("+");

  var parsed_formula = {
    response: response,
    explanatory: explanatory.map(function(d) {
      var coef_split = d.split("*");
      var coef = parseFloat(coef_split[0]);
      var range_split = coef_split[1].split("[");
      var variable = range_split[0];
      var variable_range = range_split[1].slice(0, -1).split(",").map(function(d){return parseFloat(d);});
      return {
        coef: coef,
        variable: variable,
        variable_range: variable_range
      };
    })
  };

  console.log(parsed_formula);

  //Logistic Function
  function logistic(linear_pred) {

    return linear_pred;

  }

  //Default parameters

  //Inherit any attributes or functions of a parent class
  //GlasseyeChart.call(this, x, y);

  //Any overides of parent attributes

  //Derive further attributes

  //Create functions or closures to be used in methods

  //Function to create logistic curve

  var line = d3.svg.line()
    .x(function(d) {
      return d.x;
    })
    .y(function(d) {
      return d.y;
    })
    .interpolate("basis");

};

//Methods for the class. This is where svgs are created

/*
//Inherit methods from parent
XChart.prototype = Object.create(YParent.prototype);

//Method for adding svgs
XChart.prototype.add_svg = function() {

  //Store this locally so that it can reference in further functions
  var self = this;

  //If necessary filter the data
  var filtered_data = function(){};

  //Draw the chart

  //Return the object so that we can use chaining
  return self;

};


//Method for updating svgs
XChart.prototype.update_svg = function() {

  //Store this locally so that it can reference in further functions
  var self = this;

  //If necessary filter the data
  var filtered_data = function(){};

  //Update the chart

  //Return the object so that we can use chaining
  return self;

};


//wrapper function to process the data and draw the chart

//

function x_chart(data, div, size) {

  //Define data parsers
  var inline_parser = function(data) {

    return processed_data;

  };

  var csv_parser = function(data) {

    return processed_data;

  };

  //Create draw function
  var draw = function(processed_data, div, size) {

    //Calculate values for scales

    //Create scales

    //Create new chart and chain methods

    var glasseye_chart = new XChart(processed_data, div, size);

    glasseye_chart.add_svg();

  };

  //Function that builds the chart based on whether the data is inline or from a file
  build_chart(data, div, size, undefined, csv_parser, inline_parser, draw);

}
*/
function random_gamma(alpha, beta){

    //Create d3 random number generator functions

    var random_normal = d3.random.normal()

    var d = alpha - 1/3;
    var c = 1/Math.sqrt(9*d);

    var closure = function() {

        while (!(con_1 & con_2)) {

            var z = random_normal();
            var u = Math.random();
            var v = Math.pow(1 + c * z, 3);

            //Conditions

            var con_1 = z > -1 / c;
            var con_2 = Math.log(u) < (0.5 * Math.pow(z, 2) + d - d * v + d * Math.log(v));
        }

        return (d * v) / beta;

    }

    return closure;
}


function random_dirichlet(alphas){

    //Create gamma distributions

    var gammas = alphas.map(function(d){
        return random_gamma(d,1);
    })

    var closure = function() {

        var k = gammas.map(function(g) {
            return g();
        });

        var k_sum  =  d3.sum(k);

        var x = k.map(function(d) {return d/k_sum;})


    return x;

    }

    return closure;

}/**
 * Builds a AnimatedDensity object
 * @constructor
 * @param {array} processed_data Data that has been given a structure appropriate to the chart
 * @param {string} div The div in which the chart will be placed
 * @param {string} size The size (one of several preset sizes)
 * @param {array} [labels] An array of the axis labels
 * @param {array} scales Scales for the x and y axes
 * @param {object} [margin] Optional argument in case the default margin settings need to be overridden
 */

var AnimatedDensity = function (processed_data, div, size, labels, scales, margin) {

    var self = this;

    self.processed_data = processed_data;


    GridChart.call(self, div, size, labels, scales, margin);

};

AnimatedDensity.prototype = Object.create(GridChart.prototype);


/**
 * Adds the SVGs corresponding to the AnimatedDensity object
 *
 * @method
 * @returns {object} The modified AnimatedDensity object
 */

AnimatedDensity.prototype.add_density = function () {

    var self = this;

    /*self.chart_area.selectAll("rect").data(self.processed_data)
        .enter()
        .append("rect").attr("class", "block").attr("width", self.width / (10 * self.x.domain()[1])).attr("height", self.height / (self.y.domain()[1])).attr("x", function (d) {
        return self.x(d.value)
    }).attr("y", 0).attr("opacity", 0).transition()
        .duration(2500)
        .delay(function (d, i) {
            return i * 40;
        })
        .attr("y", function (d) {
            return self.height - d.position * self.height / (self.y.domain()[1]);
        })
        .attr("opacity", 1);
        */

     var radius = d3.max([self.width / (10 * self.x.domain()[1]), self.height / (self.y.domain()[1])]) + 2;

     self.chart_area.selectAll("rect").data(self.processed_data)
     .enter()
     .append("circle").attr("class", "block").attr("r", radius).attr("cx", function (d) {
     return self.x(d.value)
     }).attr("cy", 0).attr("opacity", 0).transition()
     .duration(2500)
     .delay(function (d, i) {
     return i * 40;
     })
     .attr("cy", function (d) {
     return self.height - d.position * self.height / (self.y.domain()[1]);
     })
     .attr("opacity", 1);

};


/**
 * Creates a animated density chart within a div
 *
 * @param {array} data Either the path to a csv file or inline data in glasseye
 * @param {string} div The div in which the chart will be placed
 * @param {string} size The size (one of several preset sizes)
 * @param {array} labels An array containing the labels of the x and y axes
 */


function animated_density(div, size) {

    var processed_data = []
    var cl = random_gamma(5, 1);
    for (i = 0; i < 5000; i++) {
        processed_data.push(cl());
    }

    processed_data = processed_data.map(function (d) {
        return Math.round(d * 10) / 10;
    })


    var density_array = Array.apply(null, Array(500)).map(Number.prototype.valueOf, 0);

    processed_data = processed_data.map(function (d) {
        density_array[d * 10] = density_array[d * 10] + 1;
        return {
            value: d,
            position: density_array[d * 10]
        };

    });


    var draw = function (processed_data, div, size) {

        var x_vals = processed_data.map(function (d) {
            return d.value
        });
        var y_vals = processed_data.map(function (d) {
            return d.position
        });

        var scales = [create_scale(d3.extent(x_vals), d3.scale.linear()), create_scale([0, d3.max(y_vals) + 5], d3.scale.linear())];

        var glasseye_chart = new AnimatedDensity(processed_data, div, size, ["Random Variable with Gamma Distribution", "Occurrences"], scales);

        glasseye_chart.add_svg().add_grid().add_density();


    };

    draw(processed_data, div, size);


}
/**
 * Builds an PolygonMap object
 * @constructor
 * @param {array} processed_data Data that has been given a structure appropriate to the chart
 * @param {string} div The div in which the chart will be placed
 * @param {string} size The size (one of several preset sizes)
 */

var PolygonMap = function (processed_data, div, size, tooltip_function) {

    var self = this;

    margin = {
        top: 5,
        bottom: 0,
        left: 5,
        right: 5
    };

    GlasseyeChart.call(self, div, size, margin, 700);

    self.processed_data = processed_data;

    self.tooltip_function = tooltip_function;

    self.projection = d3.geo.albers()
        .center([0, 55.4])
        .rotate([4.4, 0])
        .parallels([50, 60])
        .scale(self.width*300/46)
        .translate([self.width / 2, self.height / 2.4]);

    self.path = d3.geo.path()
        .projection(self.projection);

    self.tip = d3.select(self.div).append('div')
        .attr('class', 'hidden tooltip');


};

PolygonMap.prototype = Object.create(GlasseyeChart.prototype);

/**
 * Adds the SVGs corresponding to the PolygonMap object
 *
 * @method
 * @returns {object} The modified PolygonMap object
 */

PolygonMap.prototype.add_map = function () {

    var self = this;

    self.chart_area.selectAll(".map_region")
        .data(self.processed_data)
        .enter().append("path")
        .attr("class", function (d) {
            return "map_region " + d.properties["name"].split(' ').join('_');
        })
        .attr("d", self.path)
        .on('mouseenter', function (d) {
            self.tooltip_function(d.properties["name"]);
            var mouse = d3.mouse(self.chart_area.node()).map(function (d) {
                return parseInt(d);
            });
            self.tip.classed('hidden', false)
                .attr('style', 'left:' + (mouse[0]) +
                    'px; top:' + (mouse[1] - 0) + 'px')
                .html(d.properties["name"]);
        })
        .on('mouseleave', function () {
            self.tip.classed('hidden', true)
        });

    return this;

};


/**
 * Redraws the PolygonMap (for example after a resize of the div)
 * @method
 * @returns {object} The modified PolygonMap object
 */

PolygonMap.prototype.redraw_map = function (title) {

    var self = this;

    //Delete the existing svg and commentary
    d3.select(self.div).selectAll("svg").remove();

    //Reset the size
    self.set_size();

    self.projection = d3.geo.albers()
        .center([0, 55.4])
        .rotate([4.4, 0])
        .parallels([50, 60])
        .scale(self.width*300/46)
        .translate([self.width / 2, self.height / 2.4]);

    self.path = d3.geo.path()
        .projection(self.projection);

    //Redraw the chart
    self = self.add_svg().add_map().add_title(self.title, self.subtitle);

    return self;

};
/**
 * Builds a Heatmap object
 * @constructor
 * @param {array} processed_data Data that has been given a structure appropriate to the chart
 * @param {string} div The div in which the chart will be placed
 * @param {string} size The size (one of several preset sizes)
 * @param {array} [labels] An array of the axis labels
 * @param {array} scales Scales for the x and y axes
 * @param {object} [margin] Optional argument in case the default margin settings need to be overridden
 */

var Heatmap = function (processed_data, div, size, labels, scales, margin) {

    var self = this;

    self.processed_data = processed_data;

    //Work out if there is a need for label rotation
    var x_scale_labels = scales[0].scale_func.domain();
    var max_string = d3.max(x_scale_labels.map(function (d) {
        return d.length;
    }));
    self.num_points = x_scale_labels.length;

    self.rotate_labels = (max_string > 60 / self.num_points) ? true : false;

    if (margin === undefined) {
        margin = {
            top: 50,
            bottom: 20,
            right: 20,
            left: 120
        };
    }

    if (self.rotate_labels === true) {
        margin.bottom = max_string * 5
    }
    ;

    //Creates color scale based on the value field
    color_domain = d3.extent(processed_data.map(function (d) {
        return d.value
    }));

    self.heat_scale = d3.scale.quantile()
        .domain(processed_data.map(function (d) {
            return d.value
        }))
        .range(colorbrewer.RdBu[9].reverse());

    //Create a list of groupspw
    self.groups = [];
    processed_data.map(function (d) {
        if (self.groups.indexOf(d.group) === -1) {
            self.groups.push(d.group);
        }
    });


    GridChart.call(self, div, size, labels, scales, margin);

    //Customise grid
    self.x_axis.tickSize(0);
    self.y_axis.tickSize(0).tickPadding(12);


    //Work out rect dimensions
    self.rect_height = self.height / scales[1].scale_func.domain().length;

    //Redo the x axis so we always get squares
    if (self.width > self.height){
        self.width = self.num_points * self.rect_height;
        self.x = self.scales[0].scale_func.rangePoints([0, self.width], 1);
    }


    self.tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function (d) {
            var text;
            if (d.value> 1){ text = d.group + " penetration is " + d3.format(",.1%")(d.raw_value/100) + "<br>That's " + d3.format(",.1%")(d.value/100) + " up on a national<br>average of " +  d3.format(",.1%")(d.nat_avg/100);}
        else
    {
        text = d.group + " penetration is " + d3.format(",.1%")(d.raw_value/100) + "<br>That's " +d3.format(",.1%")(-1*d.value/100) + " down on a national<br>average of " +  d3.format(",.1%")(d.nat_avg/100);
    }
            return text;
        });

};

Heatmap.prototype = Object.create(GridChart.prototype);


/**
 * Adds the SVGs corresponding to the BarChart object
 *
 * @method
 * @returns {object} The modified BarChart object
 */

Heatmap.prototype.add_heatmap = function () {


    var self = this;
    self.parent_div = d3.select(self.svg.node().parentNode.parentNode);

    self.chart_area.call(self.tip);

    //Get first variable
    var start_variable = self.processed_data[0].group;
    self.store_clicked = start_variable;

    //Filter the data
    var filtered_heatmap = self.processed_data.filter(function (d) {
            return d.group === start_variable
        }
    );

    //Check if we can fit in squares

    self.rect_width = (self.width > self.height)? self.rect_height : (self.width/self.num_points);

    //Add squares
    self.chart_area.selectAll(".heatmap_square")
        .data(filtered_heatmap)
        .enter()
        .append("rect")
        .attr("class", "heatmap_square")
        .attr("x", function (d) {
            return self.x(d.category_x) - self.rect_width / 2;
        })
        .attr("y", function (d) {
            return self.y(d.category_y) - self.rect_height / 2;
        })
        .attr("width", self.rect_width - 5)
        .attr("height", self.rect_height - 5)
        .attr("rx", 5)
        .attr("ry", 5)
        .attr("fill", function (d) {
            return self.heat_scale(d.value)
        })
        .on("mouseover", function(d, i) {

            //update the text
            self.parent_div.selectAll("#commentary").html(self.interactive_text(d));
            self.tip.show(d);

        })
        .on('mouseout', self.tip.hide);


    //Rotate labels if necessary
    if (self.rotate_labels === true) {
        self.chart_area.selectAll(".x_axis").selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-1em")
            .attr("dy", "-0.8em")
            .attr("transform", "rotate(-90)");
    }

    //Add the controls
    self.svg.selectAll('.control_label')
        .data(self.groups)
        .enter()
        .append("text")
        .attr("class", "control_label")
        .attr("transform", function (d, i) {
            return "translate(0," + (i * 22 + self.margin.top + 15) + ")"
        })
        .text(function (d) {
            return d;
        })
        .attr("class", function(d) { return (d===start_variable)? "control_label selected":"control_label unselected"})
        .on('mouseover', function (d) {
            self.svg.selectAll('.control_label').attr("class", "control_label unselected");
            d3.select(this).attr("class", "control_label selected");
            self.update_heatmap(d);
        })
        .on('mouseout', function (d) {
            self.svg.selectAll('.control_label').attr("class", function(d) {return (d===self.store_clicked)?"control_label selected":"control_label unselected";});
            self.update_heatmap(self.store_clicked);
        })
        .on('click', function (d) {
            self.svg.selectAll('.control_label').attr("class", "control_label unselected");
            d3.select(this).attr("class", "control_label selected");
            self.update_heatmap(d);
            self.store_clicked = d;
        });

    //Add the div for the commentary
    self.parent_div.selectAll("#heatmap_context_side").remove();
    var div = self.parent_div.append("div").attr("id", "heatmap_context_side");
    div.append("div").attr("id", "venn_instructions").html("<h1> Instructions </h1><ul><li>Hover over the platform providers on the left hand side to change the heatmap.</li><li>Hover over the cells to see a full commentary in space below.</li></ul><h1>Commentary</h1>");
    div.append("div").attr("id", "commentary").html("Hover over a circle and commentary will appear here.");

    //Adjust the x axis label

    self.svg.selectAll(".axis_label_x")
        .attr("class", "axis_label axis_label_x")
        .attr("transform", "translate(" + (self.margin.left + self.num_points * self.rect_height + 10) + ", " + (self.height + self.margin.top - 3) + ") rotate(-90)");

    return self;

};


Heatmap.prototype.add_legend = function () {

    var self = this;

    var square_dim = self.height / 9;

    //Add legend
    var legend = self.svg.append("g")
        .attr("class", "legend")
        .attr("width", 180)
        .attr("height", 400)
        .attr("transform", "translate(" + (self.margin.left + self.height * 1.1) + "," + self.margin.top + ")");

    //Add label

    legend
        .append("text")
        .attr("transform", "translate(-5," + self.height/2 +  ") rotate(-90)")
        .text("% Gain on National Average")
        .attr("text-anchor", "middle")
        .attr("class", "subtitle");

    legend_item = legend.selectAll("legend_item")
        .data(self.heat_scale.range())
        .enter()
        .append("g")
        .attr("class", "legend_item")
        .attr("transform", function (d, i) {
            return ("translate(" + 4 + "," + (self.height - (i + 1) * square_dim) + ")")
        });

    /*legend_item.append("line")
     .attr("x1", square_dim/2+2)
     .attr("x2", square_dim/2 + 6)
     .attr("y1", 0)
     .attr("y2", 0)
     .attr("stroke", "white")
     .style("opacity", function(d, i) {return (i===block)?0:1;});
     */

    legend_item.append("rect")
        .attr("x", 0)
        .attr("y", 0)
        .attr("height", square_dim)
        .attr("width", square_dim / 2)
        .attr("fill", function (d) {
            return d
        });

    //var formatter = uni_format_range(self.heat_scale.domain());
    var formatter =  d3.format(".0f");

    legend_item.append("text")
        .attr("class", "legend_text")
        .attr("x", square_dim * 1.7)
        .attr("y", 17)
        .attr("text-anchor", "middle")
        .text(function (d) {
            var r = self.heat_scale.invertExtent(d);
            return formatter(r[0]) + " to " + formatter(r[1]);
        });


    return self;

}


Heatmap.prototype.update_heatmap = function (group) {

    var self = this;


    //Set variable so that it can be accessed by the tooltip
    //self.current_variable = variable.toLowerCase();

    //Filter the data
    var filtered_heatmap = self.processed_data.filter(function (d) {
            return d.group === group
        }
    );

    self.chart_area.selectAll(".heatmap_square").data(filtered_heatmap)
        .transition()
        .duration(1000)
        .attr("fill", function (d) {
            return (d.value === undefined) ? "black" : self.heat_scale(d.value)
        });


    //self.svg.selectAll(".context").text("In " + quarter_year(time) + " for " + variable);


};

Heatmap.prototype.set_commentary = function(commentary_strings) {

    var self = this;

    self.interactive_text = function(d) {

        function highlight(text){
            return "<span style='font-weight: bold; font-size: 1.2em;color:" + self.heat_scale(d.value) + "'>" + text + "</span>";
        }

        var string_parts = commentary_strings.split("$");
        var text =string_parts[0] + highlight(d3.format(",.1%")(d.raw_value/100)) + string_parts[1] + highlight(d.category_x) + string_parts[2] + highlight(d.category_y) + string_parts[3]+ highlight(d.group) + string_parts[4] + highlight(d3.format(",.1%")(d.value/100)) + string_parts[5] + highlight(d.group) +  string_parts[6] + highlight(d3.format(",.1%")(d.nat_avg/100))
        return text;

    };

    return self;
};

//In Q2 2016 $ of households with $ occupant(s) and a $ social grade had $. That's a % difference from the national average penetration for $ which is $"

/**
 * Redraws the Heatmap (for example after a resize of the div)
 * @method
 * @returns {object} The modified Heatmap object
 */

Heatmap.prototype.redraw_heatmap = function (title) {

    var self = this;

    //Delete the existing svg and commentary
    d3.select(self.div).selectAll("svg").remove();
    self.parent_div.selectAll("#heatmap_context_side").remove();

    //Redo the x axis so we always get squares
    if (self.width > self.height){
        self.width = self.num_points * self.rect_height;

    }
    self.x = self.scales[0].scale_func.rangePoints([0, self.width], 1);

    //Redraw the chart
    self = self.set_size().add_svg().add_grid().add_heatmap().add_legend();

};


/**
 * Creates a heatmap within a div
 *
 * @param {array} data Either the path to a csv file or inline data in glasseye
 * @param {string} div The div in which the chart will be placed
 * @param {string} size The size (one of several preset sizes)
 * @param {array} labels An array containing the labels of the x and y axes
 */


function heatmap(data, div, size) {

    var inline_parser = function (data) {

    };

    var draw = function (processed_data, div, size) {

        var x_values = [],
            y_values = [];


        x_values = processed_data.map(function (d) {
            return d.category_x;
        });

        y_values = processed_data.map(function (d) {
            return d.category_y;
        });

        x_values = [].concat.apply([], y_values);
        y_values = [].concat.apply([], y_values);


        var scales = [create_scale(x_values, d3.scale.ordinal()), create_scale(y_values, d3.scale.ordinal())];


        var glasseye_chart = new Heatmap(processed_data, div, size, ["label", "value"], scales);

        glasseye_chart.add_svg().add_grid().add_heatmap();


    };

    build_chart(data, div, size, undefined, group_label_value_parser, inline_parser, draw);


}
