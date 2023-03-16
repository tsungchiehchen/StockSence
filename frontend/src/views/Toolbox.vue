<template>
    <div>
        <VueDatePicker 
            v-model="date"
            :min-date="minDate"
            :max-date="maxDate"
            :color="'#42b883'"
            format="YYYY-MM-DD"
            formatHeader="dddd MMM DD"
            id="dateRange"
            range
            validate 
        />
        <div style="margin-top: 10px; text-align: center;">
          <v-btn variant="outlined" color="rgb(66, 184, 131)" style="margin:0 auto 0px auto; display:inline-block; padding-left: 10px; padding-right: 10px; padding-bottom: 5px; color:white;" @click="searchPopup=true" v-on:click="search">Search</v-btn>
          <v-btn variant="outlined" color="rgb(229, 64, 80)" @click="predictionPopup=true" style="margin: 0 auto 0px 10px; display:inline-block; padding-left: 10px; padding-right: 10px; padding-bottom: 5px; color:white;">Price Prediction</v-btn>
        </div>
          <vs-popup class="search"  
            title="Calculating" 
            :active.sync="searchPopup"
            :background-color = "searchPopupcolor"
            :button-close-hidden="true" >
            <div style="margin: 50px auto 50px auto; text-align: center !important;">
              <v-progress-circular
              :size="70"
              color="rgb(66, 184, 131)"
              indeterminate
            ></v-progress-circular>
            </div>
          </vs-popup>
          <vs-popup fullscreen class="pricePrediction"  
            title="Price Prediction"
            :active.sync="predictionPopup"
            :background-color = "predictionPopupcolor" >
            <div style="margin: auto; overflow-y: hidden;">
              <apexchart type="line" height="450%" :options="chartOptions" :series="series"></apexchart>
            </div> 
          </vs-popup>
        </div>
</template>
  
<script>
import { VueDatePicker } from '@mathieustan/vue-datepicker';
import '@mathieustan/vue-datepicker/dist/vue-datepicker.min.css';
import Vue from 'vue'
//import { vsButton, vsPopup } from 'vuesax'
import Vuesax from 'vuesax'
import 'vuesax/dist/vuesax.css'
import 'material-icons/iconfont/material-icons.css';
import VueApexCharts from 'vue-apexcharts'
Vue.use(VueApexCharts)

Vue.component('apexchart', VueApexCharts)

Vue.use(Vuesax)
//Vue.use(vsButton)

export default {
    components: {
    VueDatePicker,
    
  },
  data(){
    return{
    date: new Date(),
    minDate: new Date([2017, 1, 1]),
    maxDate: new Date([2023, 5, 1]),
    predictionPopup: false,
    searchPopup: false,
    alrtPopup: false,
    close: true,
    searchPopupcolor: "rgba(0,0,0,.9)",
    predictionPopupcolor: "rgba(0,0,0,.9)",
    series: [{
      data: [55, 62, 89, 66, 98, 72, 101, 75, 94, 120, 117, 140]
    }],
    chartOptions: {
      chart: {
              type: 'line',
              id: 'areachart-2'
            },
      xaxis: {
        categories: [
         "Jan",
         "Feb",
         "Mar",
         "Apr",
         "May",
         "Jun",
         "Jul",
         "Aug",
         "Sep",
         "Oct",
         "Nov",
         "Dec"
        ],
      },
      annotations: {
        xaxis: [{
          x: "Mar",
          x2: "May",
          fillColor: '#B3F7CA',
          opacity: 0.4,
          label: {
            borderColor: '#B3F7CA',
            style: {
              fontSize: '15px',
              color: '#fff',
              background: '#00E396',
            },
            offsetY: -10,
            text: 'X-axis range',
          }
        }],
      },
    }
  }
},
  mounted(){
    document.getElementById("dateRange").style = "text-align: center; font-weight: bold;";
    document.getElementsByClassName("vd-icon")[0].style = "margin-left: auto; margin-right: auto;"
    document.getElementsByClassName("v-btn__content")[0].style = "margin-right: 0;"
    document.getElementsByClassName("v-btn__content")[1].style = "margin-right: 0;"

    const url = new URL(window.location.href);
    var startDate = url.searchParams.get('startDate')
    var endDate = url.searchParams.get('endDate')
    document.getElementById("dateRange").placeholder = startDate + " ~ " + endDate;
    document.getElementById("dateRange").value = startDate + " ~ " + endDate;
  },
  methods:{
    search: function(event){
      var dateRange = document.getElementById('dateRange').value
      var splitted = dateRange.split(' ~ ');
      var startDate = splitted[0]
      var endDate = splitted[1]
      var endDateSplitted = endDate.split('-')
      var endDateYear = endDateSplitted[0]
      var endDateMonth = endDateSplitted[1]
      var endDateDay = endDateSplitted[2]
      if((endDateYear > 2023) || (endDateYear == 2023 && endDateMonth > 2) || (endDateYear == 2023 && endDateMonth == 2 && endDateDay == 1)){
        alert("Current time range is not available in our data. Please use \"Price Prediction.\"");
        this.searchPopup = false
      }
      else{
        document.getElementsByClassName("vuesax-app-is-ltr")[0].style = "pointer-events: none;";  // 讓 popup 不會被滑鼠關掉
        const url = new URL(window.location.href);
        var stockPriceOnly = url.searchParams.get('stockPriceOnly')
        var stockSymbol = url.searchParams.get('stockSymbol')
        var newURL = "http://127.0.0.1:3000/api?stockPriceOnly=" + stockPriceOnly + "&startDate=" + startDate + "&endDate=" + endDate + "&stockSymbol=" + stockSymbol
        window.location.href = newURL;
      }
    }
  }
}
</script>

<style>
 .apexcharts-pie-label{
    font-size:25px;
    }  

</style>