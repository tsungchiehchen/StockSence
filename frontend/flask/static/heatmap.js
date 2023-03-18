(function () {
    var defaultStartDate = "2022-12-01"
    var defaultEndDate = "2023-02-01"

    var margin = { top: 50, right: 0, bottom: 0, left: 0 },
      width = window.innerWidth,
      height = window.innerHeight - 50,
      formatNumber = d3.format(",d"),
      transitioning;
  
    var x = d3.scale.linear()
      .domain([0, width])
      .range([0, width]);
  
    var y = d3.scale.linear()
      .domain([0, height])
      .range([0, height]);
  
    var color = d3.scale.threshold()
    .domain([-3, -0.25, 0.25, 3])
    .range(["#30CC5A", "#35764E", "#404040", "#8B444E", "#F63538"])
  
    var treemap = d3.layout.treemap()
      .children(function (d, depth) { return depth ? null : d._children; })
      .sort(function (a, b) { return a.value - b.value; })
      .ratio(height / width * 0.5 * (1 + Math.sqrt(5)))
      .round(false);
  
    var svg = d3.select("#heatmap").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.bottom + margin.top)
      .style("margin-left", -margin.left + "px")
      .style("margin-right", -margin.right + "px")
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
      .style("shape-rendering", "crispEdges");
  
    var grandparent = svg.append("g")
      .attr("class", "grandparent")
      .attr("id", "banner");
  
    grandparent.append("rect")
      .attr("y", -margin.top)
      .attr("width", width)
      .attr("height", margin.top)
  
    grandparent.append("text")
       .attr("x", 10)
       .attr("y", -17)
       //.attr("dy", ".75em")
       .attr("class", "title")

    // 工具列
    grandparent.append("foreignObject")
       .attr("id", "dates")
       .attr("x", 180)
       .attr("y", -50)
       .attr("width", window.innerWidth)
       .attr("height", 50)
    
    // 顏色 legends
    var colorLegends = svg.append("g")
    .attr("class", "colorLegends")
    .attr("id", "colorLegends")

    colorLegends.append("rect")  // 3%
      .attr("x", window.innerWidth - 75)
      .attr("y", -37)
      .attr("rx", 5)
      .attr("ry", 5)
      .attr("width", "70px")
      .attr("height", "25px")
      .attr("style", "fill:rgb(5, 102, 54);stroke-width:0;stroke:rgb(0,0,0);border-radius: 25px;")

    colorLegends.append("foreignObject")  // 3%
      .attr("x", window.innerWidth - 75)
      .attr("y", -37)
      .attr("width", "70px")
      .attr("height", "25px")
      .attr("id", "largest")

    colorLegends.append("rect")  // 2%
      .attr("x", window.innerWidth - 150)
      .attr("y", -37)
      .attr("rx", 5)
      .attr("ry", 5)
      .attr("width", "70px")
      .attr("height", "25px")
      .attr("style", "fill:rgb(8, 153, 80);stroke-width:0;stroke:rgb(0,0,0);border-radius: 25px;")

    colorLegends.append("foreignObject")  // 2%
      .attr("x", window.innerWidth - 150)
      .attr("y", -37)
      .attr("width", "70px")
      .attr("height", "25px")
      .attr("id", "secondLargest")

    colorLegends.append("rect")  // 1%
      .attr("x", window.innerWidth - 225)
      .attr("y", -37)
      .attr("rx", 5)
      .attr("ry", 5)
      .attr("width", "70px")
      .attr("height", "25px")
      .attr("style", "fill:rgb(66, 189, 127);stroke-width:0;stroke:rgb(0,0,0);border-radius: 25px;")

    colorLegends.append("foreignObject")  // -1%
      .attr("x", window.innerWidth - 225)
      .attr("y", -37)
      .attr("width", "70px")
      .attr("height", "25px")
      .attr("id", "thirdLargest")

    colorLegends.append("rect")  // 0%
      .attr("x", window.innerWidth - 300)
      .attr("y", -37)
      .attr("rx", 5)
      .attr("ry", 5)
      .attr("width", "70px")
      .attr("height", "25px")
      .attr("style", "fill:rgb(193, 196, 205);stroke-width:0;stroke:rgb(0,0,0);border-radius: 25px;")

    colorLegends.append("foreignObject")  // 0%
      .attr("x", window.innerWidth - 300)
      .attr("y", -37)
      .attr("width", "70px")
      .attr("height", "25px")
      .attr("id", "middle")

    colorLegends.append("rect")  // -1%
      .attr("x", window.innerWidth - 375)
      .attr("y", -37)
      .attr("rx", 5)
      .attr("ry", 5)
      .attr("width", "70px")
      .attr("height", "25px")
      .attr("style", "fill:rgb(247, 124, 128);stroke-width:0;stroke:rgb(0,0,0);border-radius: 25px;")

    colorLegends.append("foreignObject")  // -1%
      .attr("x", window.innerWidth - 375)
      .attr("y", -37)
      .attr("width", "70px")
      .attr("height", "25px")
      .attr("id", "thirdSmallest")
    
    colorLegends.append("rect")  // -2%
      .attr("x", window.innerWidth - 450)
      .attr("y", -37)
      .attr("rx", 5)
      .attr("ry", 5)
      .attr("width", "70px")
      .attr("height", "25px")
      .attr("style", "fill:rgb(242, 54, 69);stroke-width:0;stroke:rgb(0,0,0);border-radius: 25px;")

    colorLegends.append("foreignObject")  // -2%
      .attr("x", window.innerWidth - 450)
      .attr("y", -37)
      .attr("width", "70px")
      .attr("height", "25px")
      .attr("id", "secondSmallest")
    
    colorLegends.append("rect")  // -3%
      .attr("x", window.innerWidth - 525)
      .attr("y", -37)
      .attr("rx", 5)
      .attr("ry", 5)
      .attr("width", "70px")
      .attr("height", "25px")
      .attr("style", "fill:rgb(153, 31, 41);stroke-width:0;stroke:rgb(0,0,0);border-radius: 25px;")

    colorLegends.append("foreignObject")  // -3%
      .attr("x", window.innerWidth - 525)
      .attr("y", -37)
      .attr("width", "70px")
      .attr("height", "25px")
      .attr("id", "smallest")

    var currentURL = new URL(window.location.href);
    if(currentURL.searchParams.get('startDate') != null){
      var filePath = "stockPriceDifference/" + currentURL.searchParams.get('startDate') + "~" + currentURL.searchParams.get('endDate') + ".json";
    } 
    else{
      var filePath = "stockPriceDifference/" + defaultStartDate + "~" + defaultEndDate + ".json";
    }

    d3.queue()
      .defer(d3.json, filePath)
      .await(function (error, root) {
        if (error) throw error;
        jQuery();
        initialize(root);
        accumulate(root);
        layout(root);
        display(root);
  
        function initialize(root) {
          root.x = root.y = 0;
          root.dx = width;
          root.dy = height;
          root.depth = 0;
          d3.select('#dates')
            .html(
            "<div style=\"position: fixed\">" +
            "<div class=\"form-check\" id=\"checkBox\" style=\"float:left;padding-top:14px;margin-left:0px;padding-left:3px\">" +
            "<input class=\"form-check-input\" type=\"checkbox\" value=\"\" id=\"stockPriceOnlyCheckBox\" onclick=\"checkBoxChange(this)\">" +
            "<label class=\"form-check-label\" for=\"stockPriceOnlyCheckBox\" style=\"margin-left:20px\">" +
            "<p style=\"font-weight: normal;font-size: 14px;padding-top:5px;\">Only Check Stock Price</p>"+
            "</label>"+
            "</div>"+
            "<div class=\"input-daterange input-group\" id=\"datepicker\" style=\"padding-top:8px; padding-left: 10px; float:left; display: block; width:230px;\">" +
            "<input type=\"text\" class=\"input-sm form-control\" id=\"startDate\" name=\"stateDate\" placeholder=\"From\" style=\"flex: 0; width:110px;\"/>" +
            "<input type=\"text\" class=\"input-sm form-control\" id=\"endDate\" name=\"endDate\" placeholder=\"To\" style=\"flex: 0; width:110px;float:left;\"/>" + 
            "</div>" +
            "<div class=\"dropdown\" style=\"float:left;padding-top:8px; margin-left:10px\">" +
            "<button class=\"btn btn-outline-dark dropdown-toggle\" id=\"dropDownMenu\" type=\"button\" data-toggle=\"dropdown\" name=\"type\">View macroeconomic data" +
            "<span class=\"caret\"></span></button>" +
            "<ul class=\"dropdown-menu\" id=\"dropdown-menu\">" +
            "<li><a>CPI</a></li>" +
            "<li><a>Federal Funds Rate</a></li>" +
            "<li><a>Retail Price</a></li>" +
            "<li><a>Treasury yield 2 years</a></li>" +
            "<li><a>Treasury yield 10 years</a></li>" +
            "<li><a>Treasury yield 20 years</a></li>" +
            "<li><a>Treasury yield 30 years</a></li>" +
            "<li><a>Unemployment</a></li>" +
            "</ul>" +
            "</div>" +
            "<div class=\"col-auto\" style=\"float:left;padding-top:8px;padding-left:0px; padding-right:0px\" id=\"typeChange\">" +
              "<label class=\"sr-only\" for=\"inlineFormInputGroup\">Username</label>" +
              "<div class=\"input-group mb-2\" style=\"float:left;\">" +
                "<input type=\"text\" class=\"form-control\" id=\"typeValue\" style=\"text-align: center; width:65px; background: #F0F0F4\" readonly=\"readonly\">" +
              "</div>"+
            "</div>" +
            "<div id=\"searchButton\" style=\"float:left;padding-top:8px;padding-left:10px\">" +
            "<button type=\"submit\" form=\"form1\" class=\"btn btn-primary\" style=\"margin-left:0px\" onclick=\"post('/')\">Search</button>" +
            "</div>");
              
            // Legend Text
            // 3%
            d3.select("#largest").html(
              "<div style=\"line-height: 25px;text-align:center;color: white;\">" +
              "<p>" + Math.round(percentiles[6]) + "%</p>" +
              "</div>"
            )
            // 2%
            d3.select("#secondLargest").html(
              "<div style=\"line-height: 25px;text-align:center;color: white;\">" +
              "<p>" + Math.round(percentiles[5]) + "%</p>" +
              "</div>"
            )
            // 1%
            d3.select("#thirdLargest").html(
              "<div style=\"line-height: 25px;text-align:center;color: white;\">" +
              "<p>" + Math.round(percentiles[4]) + "%</p>" +
              "</div>"
            )
            // 0%
            d3.select("#middle").html(
              "<div style=\"line-height: 25px;text-align:center;color: white;\">" +
              "<p>" + Math.round(percentiles[3]) + "%</p>" +
              "</div>"
            )
            // -1%
            d3.select("#thirdSmallest").html(
              "<div style=\"line-height: 25px;text-align:center;color: white;\">" +
              "<p>" + Math.round(percentiles[2]) + "%</p>" +
              "</div>"
            )
            // -2%
            d3.select("#secondSmallest").html(
              "<div style=\"line-height: 25px;text-align:center;color: white;\">" +
              "<p>" + Math.round(percentiles[1]) + "%</p>" +
              "</div>"
            )
            // -3%
            d3.select("#smallest").html(
              "<div style=\"line-height: 25px;text-align:center;color: white;\">" +
              "<p>" + Math.round(percentiles[0]) + "%</p>" +
              "</div>"
            )
        }

        function jQuery(){
          $(document).ready(function(){
            $("#dropDownMenu").on('click', function () {
              // console.log("clicked");
              if ($('#dates').attr('height') == 50) {
                $('#dates').attr('height', 500);
                console.log("test");
                $("#dropdown-menu").attr('class', 'dropdown-menu show');
              }
              else {
                // console.log($("#dropdown-menu").attr('class'));
                $("#dropdown-menu").attr('class', 'dropdown-menu');
                // console.log($("#dropdown-menu").attr('class'));
                //$('#dates').attr('height', 50);
              }
            });
            $(".dropdown-menu").on('click', 'li a', function () {
              $("#dropDownMenu").text($(this).text());
              $("#dropDownMenu").val($(this).text());
              $('#dates').attr('height', 50);
              $("#dropdown-menu").attr('class', 'dropdown-menu');
              changeMacroDisplayValue($(this).text());
            });
            $("#datepicker").datepicker({
              format: "yyyy-mm-dd",
              orientation: "bottom auto",
              startDate: "2017-01-01",
              endDate: "2023-01-31",
              multidate: false,
              daysOfWeekDisabled: "0,6",
              autoclose: true,
              startView: 1,
              minViewMode: 1
            }).datepicker('update', new Date());
          });
        }
  
        function accumulate(d) {
          return (d._children = d.children)
            ? d.value = d.children.reduce(function (p, v) { return p + accumulate(v); }, 0)
            : d.value;
        }
  
        function layout(d) {
          if (d._children) {
            treemap.nodes({ _children: d._children });
            d._children.forEach(function (c) {
              c.x = d.x + c.x * d.dx;
              c.y = d.y + c.y * d.dy;
              c.dx *= d.dx;
              c.dy *= d.dy;
              c.parent = d;
              layout(c);
            });
          }
        }
  
        function getContrast50(hexcolor) {
          return (parseInt(hexcolor.replace('#', ''), 16) > 0xffffff / 3) ? 'black' : 'white';
        }
  
        function display(d) {
          // 從 URL 取值更新到內容中
          const url = new URL(window.location.href);
          if (url.searchParams.get('stockPriceOnly') !== null) {
            if (url.searchParams.get('stockPriceOnly') == "true"){
              document.getElementById("dropDownMenu").innerHTML = "Select macroeconomic type";
              document.getElementById("dropDownMenu").value = "Select macroeconomic type";
              document.getElementById("dropDownMenu").disabled = true;
              document.getElementById("stockPriceOnlyCheckBox").checked = true;
              document.getElementById("dropDownMenu").style.display = 'none';
              setDatePicker(true, true);
            }
            else{
              document.getElementById("dropDownMenu").innerHTML = "Select macroeconomic type";
              document.getElementById("dropDownMenu").value = "Select macroeconomic type";
              document.getElementById("dropDownMenu").style.display = 'block';
              changeMacroDisplayValue(url.searchParams.get('type'));
              document.getElementById("stockPriceOnlyCheckBox").checked = false;
              document.getElementById("checkBox").style="float:left;padding-top:14px;padding-left:0px";
              setDatePicker(false, true);
            }
            //console.log(url.searchParams.get('startDate'));
            document.getElementById("startDate").value = url.searchParams.get('startDate');
            document.getElementById("endDate").value = url.searchParams.get('endDate');
            document.getElementById("typeChange").style.display = 'none';
          }
          else{  // 第一次載入的情況
            document.getElementById("dropDownMenu").innerHTML = "Select macroeconomic type";
            document.getElementById("dropDownMenu").value = "Select macroeconomic type";
            document.getElementById("stockPriceOnlyCheckBox").checked = false;
            document.getElementById("startDate").value = defaultStartDate;
            document.getElementById("endDate").value = defaultEndDate;
            document.getElementById("typeChange").style.display = 'none';
          }
          
          grandparent
            .datum(d.parent)
            .on("click", transition)
            .select("text")
            .text(name(d));
  
          grandparent
            .datum(d.parent)
            .select("rect")
            .attr("fill", function () {
              return color(d['rate'])
            })
  
          var g1 = svg.insert("g", ".grandparent")
            .datum(d)
            .attr("class", "depth")
            .attr("id", "treemap");
  
          var g = g1.selectAll("g")
            .data(d._children)
            .enter().append("g");
  
          g.filter(function (d) { return d._children; })
            .classed("children", true)
            .on("click", transition);
  
          g.selectAll(".child")
            .data(function (d) { return d._children || [d]; })
            .enter().append("rect")
            .attr("class", "child")
            .call(rect);
  
          d3.select("#heatmap").select("#tooltip").remove();
          var div = d3.select("#heatmap").append("div")
            .attr("id", "tooltip")
            .style("opacity", 0);
  
          g.append("svg:a")
            .attr("href", function (d) {
              if (!d._children) {
                let currentURL = window.location.href;
                if(currentURL.includes("stockSymbol")){
                  var postData = currentURL.split('&stockSymbol')[0];
                  postData = postData.split('?')[1];
                  var url = "http://127.0.0.1:3000/api?" + postData + "&stockSymbol=" + d.name + "&startTimestamp=" + startTimestamp + "&endTimestamp=" + endTimestamp + "&fixTimeRange=true" + "&rate=" + d.rate + "&treeType=tree";
                }
                else if (currentURL.includes("?")){
                  var postData = currentURL.split('?')[1];
                  postData = postData.split('#')[0]
                  var url = "http://127.0.0.1:3000/api?" + postData + "&stockSymbol=" + d.name + "&startTimestamp=" + startTimestamp + "&endTimestamp=" + endTimestamp + "&fixTimeRange=true" + "&rate=" + d.rate + "&treeType=tree";
                }
                else{  // 在初始情況下直接進入 page 2
                  var newURL = currentURL.split(':3000')[0];
                  var url = newURL + ":3000/api?&startDate=" + defaultStartDate + "&endDate=" + defaultEndDate + "&stockSymbol=" + d.name + "&startTimestamp=" + startTimestamp + "&endTimestamp=" + endTimestamp + "&fixTimeRange=true" + "&rate=" + d.rate + "&stockPriceOnly=false" + "&treeType=tree";
                }
                return url;
              }
            })
            .append("rect")
            .attr("class", "parent")
            .call(rect)
            .on("mouseover", function (d) {
              if (d.parent.name != "MARKET") {
                let price = Math.round((d.value + Number.EPSILON) * 100) / 100;
                let rate = d.rate;
                d3.select("#tooltip").transition()
                  .duration(200)
                  .style("opacity", 1);
                d3.select("#tooltip").html(
                  "<style=\"width: "+ length + "px></style>" +
                  "<h3 style=\"font-weight: bold;\">" + d.name + "</h3><table>" +
                  "<tr><td>" + price + "</td><td>" + " (" + rate.toString() + "%)" + "</td></tr>" +
                  "</table>")
              }
            })
            .on("mousemove", function (d) {
              var width = document.getElementById('tooltip').getBoundingClientRect().width;
              if(d3.event.pageX + width >= window.innerWidth){  // 滑鼠已經到右邊，tooltip 在左邊顯示
                d3.select("#tooltip").style("left", (d3.event.pageX) - width + "px")
                                     .style("top", (d3.event.pageY - 45) + "px");
              }
              else{
                d3.select("#tooltip").style("left", (d3.event.pageX) + "px")
                                     .style("top", (d3.event.pageY - 45) + "px");
              }
              
            })
            .on("mouseout", function (d) {
              d3.select("#tooltip").transition()
                .duration(200)
                .style("opacity", 0);
            })
            .append("title")
            .text(function (d) { return formatNumber(d.value); });
  
  
          g.append("text")  // 左上角標題 text
            .attr("dy", ".75em")
            .text(function (d) { return d.name; })
            .call(text);
  
          function transition(d) {
            if (transitioning || !d) return;
            transitioning = true;
  
            var g2 = display(d),
              t1 = g1.transition().duration(750),
              t2 = g2.transition().duration(750);
  
            x.domain([d.x, d.x + d.dx]);
            y.domain([d.y, d.y + d.dy]);
  
            svg.style("shape-rendering", null);
  
            svg.selectAll(".depth").sort(function (a, b) { return a.depth - b.depth; });
  
            g2.selectAll("text").style("fill-opacity", 0);
  
            t1.selectAll("text").call(text).style("fill-opacity", 0);
            t2.selectAll("text").call(text).style("fill-opacity", 1);
            t1.selectAll("rect").call(rect);
            t2.selectAll("rect").call(rect);
  
            t1.remove().each("end", function () {
              svg.style("shape-rendering", "crispEdges");
              transitioning = false;
            });
          }
  
          return g;
        }
  
        function text(text) {
          text.attr("x", function (d) { return x(d.x) + (x(d.x + d.dx) - x(d.x)) / 2; })
            .attr("y", function (d) { return y(d.y) + (y(d.y + d.dy) - y(d.y)) / 2; })
            .attr("dy", 0)
            .attr("font-size", function (d) {
              var w = x(d.x + d.dx) - x(d.x),
                h = y(d.y + d.dy) - y(d.y),
                t = (d.name).length / 1.3;
              var tf = Math.min(Math.floor(w / t), h / 3);
              return (tf >= 5) ? Math.min(tf, 30) : 0;
            })
            .attr("fill", "white")
            .attr("text-anchor", "middle");
        }
  
        function rect(rect) {
          rect.attr("x", function (d) { return x(d.x); })
            .attr("y", function (d) { return y(d.y); })
            .attr("width", function (d) { return x(d.x + d.dx) - x(d.x); })
            .attr("height", function (d) { return y(d.y + d.dy) - y(d.y); })
            .attr("fill", function (d) { 
              if(parseFloat(d.rate) >= percentiles[6]){
                return "#056636";
              }
              else if(parseFloat(d.rate) >= percentiles[5]){
                return "#089950";
              }
              else if(parseFloat(d.rate) >= percentiles[4]){
                return "#42BD7F";
              }
              else if(parseFloat(d.rate) >= percentiles[2]){
                return "#C1C4CD";
              }
              else if(parseFloat(d.rate) >= percentiles[1]){
                return "#F77C80";
              }
              else if(parseFloat(d.rate) >= percentiles[0]){
                return "#F23645";
              }
              else{
                return "#991F29";
              }
            });
        }
  
        function name(d) {
          return d.parent
            ? "Back to Overall"
            : "Overall " + d.name;
        }
      });
  }());

function post(path, method = 'post') {
  const params = Object.create(null);
  params["startDate"] = document.getElementById("startDate").value;
  params["endDate"] = document.getElementById("endDate").value;
  if (params["startDate"] != "" | params["endDate"] != ""){
    if(params["startDate"] == params["endDate"]){
      alert("Date can't be the same")
    }
    else{
      const form = document.createElement('form');
      form.method = method;
      form.action = path;
      for (const key in params) {
        const hiddenField = document.createElement('input');
        hiddenField.type = 'hidden';
        hiddenField.name = key;
        hiddenField.value = params[key];
        form.appendChild(hiddenField);
      }
      var url = new URL("http://127.0.0.1:3000");
      if (document.getElementById("stockPriceOnlyCheckBox").checked){
        url.searchParams.set('stockPriceOnly', "true");
      }
      else{
        url.searchParams.set('stockPriceOnly', "false");
      }
      url.searchParams.set('startDate', document.getElementById("startDate").value);
      url.searchParams.set('endDate', document.getElementById("endDate").value);
      window.location.href = url;
    }
  }
  else {
    alert("Please enter all values");
  }
}

function setDatePicker(stockPriceOnly, firstLoad) {
  if (stockPriceOnly == true) {
    var newOptions = {
      format: "yyyy-mm-dd",
      orientation: "bottom auto",
      startDate: "2017-01-01",
      endDate: "2023-02-28",
      multidate: false,
      daysOfWeekDisabled: "0,6",
      autoclose: true,
      startView: 1,
      minViewMode: 0
    }
    if(firstLoad == false)
    {
      $('#datepicker').datepicker('destroy')
      $('#datepicker').datepicker(newOptions);
    }
  }
  else {
    var newOptions = {
      format: "yyyy-mm-dd",
      orientation: "bottom auto",
      startDate: "2017-01-01",
      endDate: "2023-02-28",
      multidate: false,
      daysOfWeekDisabled: "0,6",
      autoclose: true,
      startView: 1,
      minViewMode: 1
    }
    $('#datepicker').datepicker('destroy');
    $('#datepicker').datepicker(newOptions);
  }
}

function checkBoxChange(checkbox){
  if(checkbox.checked)
  {
    //document.getElementById("dropDownMenu").disabled = true;
    setDatePicker(true, false);
    document.getElementById("startDate").value = "";
    document.getElementById("endDate").value = "";
    document.getElementById("typeChange").style.display = 'none';
    document.getElementById("dropDownMenu").style.display = 'none';
  }
  else
  {
    document.getElementById("dropDownMenu").disabled = false;
    setDatePicker(false, false);
    document.getElementById("startDate").value = "";
    document.getElementById("endDate").value = "";
    document.getElementById("typeChange").style.display = 'none';
    document.getElementById("dropDownMenu").style.display = 'block';
  }
}
  

function changeMacroDisplayValue(type){
  document.getElementById("typeChange").style.display = 'block';
  if(type == "CPI"){
    document.getElementById("typeValue").value = macroChange[0];
  }
  else if (type == "Federal Funds Rate"){
    document.getElementById("typeValue").value = macroChange[1];
  }
  else if (type == "Retail Price"){
    document.getElementById("typeValue").value = macroChange[2];
  }
  else if (type == "Treasury yield 2 years"){
    document.getElementById("typeValue").value = macroChange[3];
  }
  else if (type == "Treasury yield 10 years"){
    document.getElementById("typeValue").value = macroChange[4];
  }
  else if (type == "Treasury yield 20 years"){
    document.getElementById("typeValue").value = macroChange[5];
  }
  else if (type == "Treasury yield 30 years"){
    document.getElementById("typeValue").value = macroChange[6];
  }
  else if(type == "Unemployment"){
    document.getElementById("typeValue").value = macroChange[7];
  }
}