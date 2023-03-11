<template>
    <trading-vue :data="this.$data" :titleTxt="this.titleTxt" :width="this.width" :height="this.height" :toolbar="false" ref="tradingVue">
    </trading-vue>
</template>

<script>
import TradingVue from 'trading-vue-js'

export default {
    name: 'app',
    components: { TradingVue },
    data() {
        return {
            width: window.innerWidth,
            height: window.innerHeight,
            ohlcv: null,
            titleTxt: null,
        }
    },
    async created() {
        const url = new URL(window.location.href);
        var stockSymbol = url.searchParams.get('stockSymbol');
        this.titleTxt = stockSymbol;

        const objectData = await import("../../../backend/dataset/price display/" + String(stockSymbol) + ".json");
        const slicedObjectData = Object.fromEntries(Object.entries(objectData).slice(0, -2))

        var arrayData = [];
        for (var od in slicedObjectData) {
            arrayData.push(objectData[od]);
        }
        this.ohlcv = arrayData;
    },
    methods: {
        onResize() {
            this.width = window.innerWidth
            this.height = window.innerHeight
        }
    },
    mounted() {
        window.addEventListener('resize', this.onResize)
        window.dc = this.chart
        this.$nextTick(() =>
            console.log(this.$refs.tradingVue.getRange())
        )
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.onResize)
    }
}

</script>