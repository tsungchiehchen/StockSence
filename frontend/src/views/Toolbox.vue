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
          <v-btn variant="outlined" color="rgb(66, 184, 131)" style="margin:0 auto; display:inline-block;" v-on:click="search">Search</v-btn>
          <v-btn variant="outlined" color="rgb(229, 64, 80)" style="margin: 0 auto auto 5px; display:inline-block;">Price Prediction</v-btn>
        </div>
    </div>
</template>
  
<script>
import { VueDatePicker } from '@mathieustan/vue-datepicker';
import '@mathieustan/vue-datepicker/dist/vue-datepicker.min.css';

export default {
    components: {
    VueDatePicker
  },
  data: () => ({
    date: new Date(),
    minDate: new Date([2017, 1, 1]),
    maxDate: new Date([2023, 5, 1])
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
      }
      else{
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