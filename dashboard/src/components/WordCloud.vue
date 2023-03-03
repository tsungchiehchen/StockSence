<template>
  <div class="wordCloud" v-resize="onResize"></div>
</template>

<script lang="ts">
import * as d3 from 'd3'
import * as cloud from 'd3-cloud'
import * as d3ScaleChromatic from 'd3-scale-chromatic'
import resize from 'vue-resize-directive'
import axios from 'axios';
import { server } from '../helper';


export default {
  name: 'wordCloud',
  data () // 定義變數
  {
    return {
      jsonData: [] as string[],
      svgWidth: 0,
      svgHeight: 0,
      margin: {top: 15, bottom: 15, left: 15, right: 15},
      rotate: {from: -60, to: 60, numOfOrientation: 10},
      fontSize: [8, 85],
      color: ['#AB3B3A', '#CB1B45', '#E87A90', '#F8C3CD']
    }
  },
  created() // fetch data from backend
  {
    axios.post(`${server}/fetchExample`)
        .then(resp => {
            var titleData = resp.data.titles;
            var titles = Object.keys(titleData);
            var titlesIndex = 0;
            var resultArray = Object.keys(titleData).map(function(title){
                let titleCount = {
                  "word": titles[titlesIndex],
                  "value": titleData[title]
                }
                titlesIndex++;
                return titleCount;
            });
            this.svgWidth = this.$el.clientWidth
            this.svgHeight = this.$el.clientHeight
            this.jsonData = resultArray
            this.chart = this.createChart()
            this.renderChart()
            return true;
        })
        .catch(error => console.log(error));
  },
  computed: 
  {
    size () // 設定顯示大小
    {
      const { svgWidth, svgHeight } = this
      const { margin } = this
      const width = svgWidth - margin.left - margin.right
      const height = svgHeight - margin.top - margin.bottom
      return { width, height }
    },
    words () // 用降冪排序取得字體大小
    { 
      const { jsonData } = this
      const words = jsonData.sort(function (a, b) {
        return parseFloat(b['value']) - parseFloat(a['value'])
      })
      return words.slice(0, 150)  // 只取前 100 個
    }
  },
  methods: {
    throttle (method, context) 
    {
      clearTimeout(method.tid)
      method.tid = setTimeout(function () {
        method.call(context)
      }, 200)
    },
    onResize ()
    {
      this.svgWidth = this.$el.clientWidth
      this.svgHeight = this.$el.clientHeight
      this.throttle(this.update)
    },
    createChart () 
    {
      const { margin } = this
      const { width, height } = this.size
      const svg = d3.select(this.$el).append('svg')
                      .attr('width', '100%')
                      .attr('height', '100%')
      const chart = svg.append('g')
                         .attr('width', width)
                         .attr('height', height)
                         .attr('class', 'chart')
                         .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
      return chart
    },
    getRotation ()
    {
      const { from: x1, to: x2, numOfOrientation: n } = this.rotate
      const multiplier = ((Math.abs(x1) + Math.abs(x2)) / (n - 1)) || 1
      return { a: n, b: (x1 / multiplier), c: multiplier }
    },
    setFontSizeScale ()
    {
      const { fontSize, words } = this
      this.fontSizeScale = d3.scaleSqrt()
      this.fontSizeScale.range(fontSize)
      if (words.length) {
        this.fontSizeScale.domain([+words[words.length - 1]['value'] || 1, +words[0]['value']])
      }
    },
    renderChart () 
    {
      this.setFontSizeScale()
      const { spiral, wordPadding, fontSizeScale, font, words } = this
      const { width, height } = this.size
      const { a, b, c } = this.getRotation()
      const layout = cloud()
              .size([width, height])
              .words(words)
              .fontSize(d => fontSizeScale(d['value']))
              .text(d => d["word"])
              .font('Impact')
              .padding(1)
              .rotate(() => { return (~~(Math.random() * a) + b) * c })
              .spiral('archimedean')
              .on('end', this.draw)
      this.layout = layout
      layout.start()
    },
    draw (jsonData)
    {
      const { layout, chart, color, showTooltip, wordClick, fontSizeScale } = this
      const centeredChart = chart.append('g')
              .attr('transform', 'translate(' + layout.size()[0] / 2 + ',' + layout.size()[1] / 2 + ')')
      const tooltip = d3.select("body").append("div")
            .attr("class", "wordcloud-tooltip")
            .style("opacity", 0);
      const text = centeredChart.selectAll('text')
              .data(jsonData)
              .enter().append('text')
              .style('font-size', d => d.size + 'px')
              .style('font-family', d => d.font)
              .style('fill', function(d){ // 根據出現頻率自訂文字顏色
                if (d.size > 45){
                  return color[0]
                }
                else if (d.size > 25 && d.size <=45){
                  return color[1]
                }
                else if (d.size > 15 && d.size <= 25){
                  return color[2]
                }
                else{
                  return color[3]
                }
              })
              .attr('class', 'text')
              .attr('text-anchor', 'middle')
      text.transition()
              .duration(500)
              .attr('transform', (d) => { return 'translate(' + [d.x, d.y] + ')rotate(' + d.rotate + ')' })
              .text(d => d.text)
      text.on("mouseover", function(d) {
                // 估計 tooltip 的長度
                var canvas = document.createElement("canvas");
                var context = canvas.getContext("2d");
                context.font = "13px Arial";
                var textWidth = context.measureText(d.srcElement.__data__.word).width + 16;
                var valueWidth = context.measureText(d.srcElement.__data__.value).width + 16;
                if (textWidth > valueWidth){
                  var formattedWidth = Math.ceil(textWidth) + "px;";
                }
                else{
                  var formattedWidth = Math.ceil(valueWidth) + "px;";
                }
                
                tooltip.transition()
                    .duration(200)
                    .style("opacity", .8)
                tooltip.html(
                  "<p style=\"font-weight: bolder; font-size:13px;\">" + d.srcElement.__data__.word + "</p>" + '(' + d.srcElement.__data__.value + ')' +
                  "<style>" + "div.wordcloud--tooltip {width: " + formattedWidth + ";} </style>"
                  )
            })
            .on("mousemove", function(d) {
                tooltip.style("left", d.clientX + 20 + "px") 
                       .style("top", d.clientY - 25 + "px");
            })
            .on("mouseout", function(d) {
                tooltip.transition()
                    .duration(500)
                    .style("opacity", 0)
        });
    },
    update () // 當大小改變時，重新製圖
    {
      const { words, layout, fontSizeScale, chart } = this
      const { width, height } = this.size
      if (words.length) {
        fontSizeScale.domain([+words[words.length - 1]['value'] || 1, +words[0]['value']])
      }
      if (chart != null)  // chart 還沒有畫
      {
        // clear chart
        chart.select('g').remove()
        layout.stop().size([width, height]).words(words).start()
      }
    }
  }
}
</script>


<style scope>
.wordCloud {
  display: inline-block;
  position: relative;
  width: 100%;
  height: 100%;
}
.wordCloud svg {
  display: inline-block;
  position: absolute;
  top: 0;
  left: 0;
}
div.wordcloud-tooltip {
    position: absolute;
    font-family: Arial;
    height: 50px;
    padding: 4px;
    font-size: 12px;
    line-height: 20px;
    color: white;
    background: black;
    border: 0px;
    border-radius: 8px;
    pointer-events: none;
}
div.wordcloud-tooltip:empty {
  padding: 0px !important;
  height: 0px !important;
}
</style>
