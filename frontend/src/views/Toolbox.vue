<template>
    <div>
        <datepicker placeholder="Select Date" style="width:1vw"></datepicker> 
        <button type="submit" form="form1" class="btn btn-primary" style="margin-left:0px" onclick="">Search</button>
    </div>
</template>
  
<script>
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import Datepicker from 'vuejs-datepicker'

import '../components/bootstrap4-1-3.min.css'

export default {
    components: {
        Datepicker
    },
    data() {
        return {
            value: '',
            context: null
        }
    },
    methods: {
        onContext(ctx) {
            this.context = ctx
        }
    }
}
</script>