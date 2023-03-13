<script lang="ts">
import PriceDisplay from "./views/PriceDisplay.vue"
import StockRecommendation from "./views/StockRecommendation.vue"

export default {
  name: 'StockSense',
  components: {
    PriceDisplay,
    StockRecommendation
  }
}

document.title = "StockSense"
</script>


<template>
  <div id="StockSense">
    <div id="upperRow">
        <div id="priceDisplay">
          <PriceDisplay/>
        </div>
    </div>
    <div id="lowerRow">
        <div>
          <StockRecommendation/>
        </div>
    </div>
  </div>
</template>

<style lang="scss">
html,
body {
  height: 100%;
  margin: 0;
  overflow-y: hidden;
  overflow-x: hidden;
  font: 15px -apple-system,BlinkMacSystemFont,
  Segoe UI,Roboto,Oxygen,Ubuntu,Cantarell,
  Fira Sans,Droid Sans,Helvetica Neue,sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  position: flex;
}

.fixTimeRangeCheckBox {
  position: absolute;
  top: 19px;
  color: rgb(51, 51, 51);
  font: 13px -apple-system,BlinkMacSystemFont,
  Segoe UI,Roboto,Oxygen,Ubuntu,Cantarell,
  Fira Sans,Droid Sans,Helvetica Neue,sans-serif
}

.tree {
    width: 90%;
    height: 30%;
    // display: block;
    // overflow: auto; 
    position: fixed;
}
</style>
