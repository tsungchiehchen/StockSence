<template>
    <div>
        <VueDatePicker 
            v-model="date"
            :min-date="minDate"
            :max-date="maxDate"
            :range-presets="presets"
            format="YYYY-MM-DD"
            formatHeader="dddd MMM DD"
            placeholder="Select a new time range"
            id="dateRange"
            range
            validate 
        />
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
  }),
  mounted(){
    document.getElementById("dateRange").style = "text-align: center;";
    document.getElementsByClassName("vd-icon")[0].style = "margin-left: auto; margin-right: auto;"
  }
}
</script>