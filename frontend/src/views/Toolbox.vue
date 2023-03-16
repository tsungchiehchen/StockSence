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
        <div style="margin-top: 15px; text-align: center;">
          <v-btn variant="outlined" color="rgb(66, 184, 131)" style="margin:0 auto 0px auto; display:inline-block; padding-left: 10px; padding-right: 10px; padding-bottom: 5px;" @click="searchPopup=true" v-on:click="search">Search</v-btn>
          <v-btn variant="outlined" color="rgb(229, 64, 80)" @click="predictionPopup=true" style="margin: 0 auto 0px 10px; display:inline-block; padding-left: 10px; padding-right: 10px; padding-bottom: 5px;">Price Prediction</v-btn>
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
        <vs-popup class="pricePrediction"  
          title="Price Prediction" 
          :active.sync="predictionPopup"
          :background-color = "predictionPopupcolor" >
          <p>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
          </p>
          <p>dqw</p>
          <p>dqw</p>
          <p>dqw</p>
          <p>dqw</p>
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

Vue.use(Vuesax)
//Vue.use(vsButton)

export default {
    components: {
    VueDatePicker,
  },
  data: () => ({
    date: new Date(),
    minDate: new Date([2017, 1, 1]),
    maxDate: new Date([2023, 5, 1]),
    predictionPopup: false,
    searchPopup: false,
    alrtPopup: false,
    close: true,
    searchPopupcolor: "rgba(0,0,0,.9)",
    predictionPopupcolor: "rgba(0,0,0,.9)"
  }),
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