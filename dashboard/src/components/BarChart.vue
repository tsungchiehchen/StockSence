<template>
  <div style="height: 370px; margin-right: 15px; margin-left: 15px;">
    <Bar 
      :data="jsonData"
      :options="chartOptions"
    />
  </div>
</template>


<script lang="ts">
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import axios from 'axios';
import { server } from '../helper';
import { ref, onMounted } from 'vue'
import chartTrendline from 'chartjs-plugin-trendline';


ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, chartTrendline);

export default {
  name: 'BarChart',
  components: { Bar },
  data() {
    return {
      jsonData: {
        labels: [],
        datasets: [
          {
            data: [],
            backgroundColor: '#A5DEE4',
            trendlineLinear:  // trendline 設定
            {
                colorMin: "rgb(203, 27, 69, 0.5)",
                colorMax: "rgb(203, 27, 69, 0.5)",
                lineStyle: "dotted|solid",
                width: 2
            }
          }
        ]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                title: {
                    display: true,
                    text: "Number of papers",
                    font: {size: 15}
                }
            }
        },
        plugins: {
            legend: {
              display: false
            }
        },
      }
    }
  },
  mounted(){
    this.loadData()  // 將資料讀入 chart 中
  },

  methods:
  {
    updateChart(years, yearCount){
      this.jsonData = {
        labels: years,
        datasets: [
          {
            data: yearCount,
            backgroundColor: '#A5DEE4',
            trendlineLinear:  // trendline 設定
            {
                colorMin: "rgb(203, 27, 69, 0.5)",
                colorMax: "rgb(203, 27, 69, 0.5)",
                lineStyle: "dotted|solid",
                width: 2
            }
          }
        ],
      }
    },

    async loadData()  // 從前端取值
    {
      await axios.post(`${server}/fetchExample`)
      .then(resp => {
          var publishTimeData = resp.data.publishTime;
          var publishTimes = Object.keys(publishTimeData);
          var publishTimeDataIndex = 0;
          var years = [];
          var yearCount = []
          var keys = Object.keys(publishTimeData)
          for (var key of keys){
            years.push(key)
            yearCount.push(publishTimeData[key])
          }
          this.updateChart(years, yearCount)
          return true;
      })
      .catch(error => console.log(error));
    }
  },
}
</script>