<template>
    <div id="priceDisplay">
        
        <trading-vue :data="this.$data" 
                 :titleTxt="this.titleTxt" 
                 :toolbar="false" 
                 :height="this.height"
                 :width="this.width"
                 :color-back="colors.colorBack"
                 :color-grid="colors.colorGrid"
                 :color-text="colors.colorText"
                 ref="tradingVue"
                 id="priceDisplayVue">
        </trading-vue>
        <!-- <span class="fixTimeRangeCheckBox" id="fixTimeRangeCheckBox">
            <input type="checkbox" v-model="fixTimeRange">
            <label>&nbsp;Fix time range</label>
        </span> -->
    </div>
</template>

<script>
import TradingVue from 'trading-vue-js'
import CompanyNames from "../../../backend/dataset/company names.json"

export default {
    name: 'app',
    components: { TradingVue },
    data() {
        const url = new URL(window.location.href);
        return {
            width: window.innerWidth*0.75,
            height: window.innerHeight*0.63,
            ohlcv: null,
            titleTxt: null,
            fixTimeRange: url.searchParams.get('fixTimeRange')
        }
    },
    async created() {
        // 讀取 json 檔案
        const url = new URL(window.location.href);
        var stockSymbol = url.searchParams.get('stockSymbol');
        var startTimestamp = url.searchParams.get('startTimestamp')
        var endTimestamp = url.searchParams.get('endTimestamp')
        var rate = url.searchParams.get('rate')

        var objectData = await import("../../../backend/dataset/price display/" + String(stockSymbol) + ".json");
        var slicedObjectData = Object.fromEntries(Object.entries(objectData).slice(0, -2))

        var arrayData = [];
        
        for (var od in slicedObjectData) {
            // if(this.fixTimeRange == "true"){
            //     if(slicedObjectData[od][0] >= startTimestamp && slicedObjectData[od][0] <= endTimestamp){
            //         arrayData.push(slicedObjectData[od]);
            //     }
            // }
            // else{
            //     arrayData.push(slicedObjectData[od]);
            // }
            if (slicedObjectData[od][0] >= startTimestamp && slicedObjectData[od][0] <= endTimestamp) {
                arrayData.push(slicedObjectData[od]);
            }
        }

        this.ohlcv = arrayData;

        // 讀取 company name 和 rate 加入到 title
        this.titleTxt = CompanyNames[stockSymbol] + " (" +  rate + "%)";
    },
    computed: {
        colors() {
            return{
                colorBack: '#fff',
                colorGrid: '#eee',
                colorText: '#333'
            }
        },
    },
    methods: {
        onResize() {
            this.width = window.innerWidth*0.78
            this.height = window.innerHeight*0.65
            // var fixTimeRangeCheckBox = document.getElementById("fixTimeRangeCheckBox");
            // fixTimeRangeCheckBox.style = "left: " + (this.width-190) + "px";
        }
    },
    watch: {
        // fixTimeRange: function(val) {  // 當改變 fix time range check box 的時候
        //     let currentURL = window.location.href;
        //     if(currentURL.includes("fixTimeRange")){  // true -> false
        //         var postData = currentURL.split('&fixTimeRange=')[0];
        //         window.location.href = postData;
        //     }
        //     else{  // false -> true
        //         postData = currentURL.split('#/')[0];
        //         window.location.href = postData + "&fixTimeRange=true";
        //     }
        // }
    },
    mounted() {
        // 加入 back button
        const div = document.createElement('span');
        div.className = 'pageBack';
        div.style = "margin-right: 5px;"
        let currentURL = window.location.href;
        var postData = currentURL.split('?')[1];
        div.innerHTML = `<a href="http://127.0.0.1:3000/?` + postData + `"+ style="z-index:10000; pointer-events: all; font-size: 20px; color: rgb(0, 0, 0); text-decoration: none; font-weight: 300;">`+ 
            `◀ Back</a>`;
        document.querySelector(".trading-vue-ohlcv").prepend(div);
        //document.getElementsByClassName('pageBack').style = "margin-left: 5px;"
        
        // 設定 title style
        const url = new URL(window.location.href);
        var rate = url.searchParams.get('rate')
        if(rate >= 0){
            document.querySelector(".t-vue-title").setAttribute("style", "font-weight: 800; color: rgb(66, 184, 131);"); 
        }
        else{
            document.querySelector(".t-vue-title").setAttribute("style", "font-weight: 800; color: rgb(229, 64, 80);"); 
        }

        window.addEventListener('resize', this.onResize)
        window.dc = this.chart
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.onResize)
    }
}

</script>