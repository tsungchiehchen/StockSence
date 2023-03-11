<template>
    <trading-vue :data="this.$data" :width="this.width" :height="this.height" :toolbar="true" ref="tradingVue">
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
            ohlcv: [
                [ 1551128400000, 33,  37.1, 14,  14,  196 ],
                [ 1551132000000, 13.7, 30, 6.6,  30,  206 ],
                [ 1551135600000, 29.9, 33, 21.3, 21.8, 74 ],
                [ 1551139200000, 21.7, 25.9, 18, 24,  140 ],
                [ 1551142800000, 24.1, 24.1, 24, 24.1, 29 ],
            ],
        }
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