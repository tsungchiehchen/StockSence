<template>
    <trading-vue :data="this.$data" :titleTxt="this.titleTxt" :width="this.width" :height="this.height" :toolbar="false" ref="tradingVue">
    </trading-vue>
</template>

<script>
import TradingVue from 'trading-vue-js'
import CompanyNames from "../../../backend/dataset/company names.json"

export default {
    name: 'app',
    components: { TradingVue },
    data() {
        return {
            width: window.innerWidth,
            height: window.innerHeight,
            ohlcv: null,
            titleTxt: null,
            changed: false,
        }
    },
    async created() {
        // 讀取 json 檔案
        const url = new URL(window.location.href);
        var stockSymbol = url.searchParams.get('stockSymbol');
        //this.titleTxt = stockSymbol;

        var objectData = await import("../../../backend/dataset/price display/" + String(stockSymbol) + ".json");
        var slicedObjectData = Object.fromEntries(Object.entries(objectData).slice(0, -2))

        var arrayData = [];
        for (var od in slicedObjectData) {
            arrayData.push(objectData[od]);
        }
        this.ohlcv = arrayData;

        // 讀取 company name
        this.titleTxt = CompanyNames[stockSymbol] + " (" +  stockSymbol + ")";

        var startTimestamp = url.searchParams.get('startTimestamp');
        var endTimestamp = url.searchParams.get('endTimestamp');
        this.$nextTick(() =>
            this.$refs.tradingVue.goto(startTimestamp)
        )
    },
    methods: {
        goToTime(){
            // 將顯示時間與 treemap 相同
            const url = new URL(window.location.href);
            var startTimestamp = url.searchParams.get('startTimestamp');
            var endTimestamp = url.searchParams.get('endTimestamp');

            this.$refs.tradingVue.goto(startTimestamp)
        },
        onResize() {
            this.width = window.innerWidth
            this.height = window.innerHeight
            //this.goToTime()
        },
    },
    mounted() {
        // 加入 back button
        const div = document.createElement('span');
        div.className = 'pageBack';
        let currentURL = window.location.href;
        var postData = currentURL.split('?')[1];
        div.innerHTML = `<a href="http://127.0.0.1:3000/?` + postData + `"+ style="z-index:10000; pointer-events: all; font-size: 20px; color: rgb(222, 221, 221); text-decoration: none;">◀ Back&nbsp</a>`;
        document.querySelector(".trading-vue-ohlcv").prepend(div);

        document.querySelector(".t-vue-title").setAttribute("style", "font-weight: bold; color: rgb(66, 184, 131);"); 
        //document.getElementById("t-vue-title").setAttribute("style", "font-weight: bold; color: rgb(66, 184, 131);"); 

        window.addEventListener('resize', this.onResize)
        window.dc = this.chart
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.onResize)
    }
}

</script>