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
                 ref="tradingVue">
        </trading-vue>
        <span class="fixTimeRangeCheckBox" id="fixTimeRangeCheckBox">
            <input type="checkbox" v-model="fixTimeRange">
            <label>&nbsp;Fix time range</label>
        </span>
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
            width: window.innerWidth*0.8,
            height: window.innerHeight*0.7,
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

        var objectData = await import("../../../backend/dataset/price display/" + String(stockSymbol) + ".json");
        var slicedObjectData = Object.fromEntries(Object.entries(objectData).slice(0, -2))

        var arrayData = [];
        
        for (var od in slicedObjectData) {
            if(this.fixTimeRange == "true"){
                if(slicedObjectData[od][0] >= startTimestamp && slicedObjectData[od][0] <= endTimestamp){
                    arrayData.push(slicedObjectData[od]);
                }
            }
            else{
                arrayData.push(slicedObjectData[od]);
            }
            
        }

        this.ohlcv = arrayData;

        // 讀取 company name
        this.titleTxt = CompanyNames[stockSymbol] + " (" +  stockSymbol + ")";

        var fixTimeRangeCheckBox = document.getElementById("fixTimeRangeCheckBox");
        fixTimeRangeCheckBox.style = "left: " + (this.width-190) + "px";
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
            this.width = window.innerWidth*0.8
            this.height = window.innerHeight*0.7
            var fixTimeRangeCheckBox = document.getElementById("fixTimeRangeCheckBox");
            fixTimeRangeCheckBox.style = "left: " + (this.width-190) + "px";
        }
    },
    watch: {
        fixTimeRange: function(val) {  // 當改變 fix time range check box 的時候
            let currentURL = window.location.href;
            if(currentURL.includes("fixTimeRange")){  // true -> false
                var postData = currentURL.split('&fixTimeRange=')[0];
                window.location.href = postData;
            }
            else{  // false -> true
                postData = currentURL.split('#/')[0];
                window.location.href = postData + "&fixTimeRange=true";
            }
        }
    },
    mounted() {
        // 加入 back button
        const div = document.createElement('span');
        div.className = 'pageBack';
        let currentURL = window.location.href;
        var postData = currentURL.split('?')[1];
        div.innerHTML = `<a href="http://127.0.0.1:3000/?` + postData + `"+ style="z-index:10000; pointer-events: all; font-size: 20px; color: rgb(0, 0, 0); text-decoration: none;">`+ 
            `◀ Back&nbsp</a>`;
        document.querySelector(".trading-vue-ohlcv").prepend(div);
        
        // 設定 title style
        document.querySelector(".t-vue-title").setAttribute("style", "font-weight: bold; color: rgb(66, 184, 131);"); 

        window.addEventListener('resize', this.onResize)
        window.dc = this.chart
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.onResize)
    }
}

</script>