<script lang="ts">
import PriceDisplay from "./views/PriceDisplay.vue"
import StockRecommendation from "./views/StockRecommendation.vue"
import NewsDisplay from "./views/NewsDisplay.vue"

export default {
  name: 'StockSense',
  components: {
    PriceDisplay,
    StockRecommendation,
    NewsDisplay
  }
}

document.title = "StockSense"

</script>


<template>
  <div>
  <v-row id="upperRow" style="height: 70vh">
    <v-col id="priceDisplay">
      <PriceDisplay/>
    </v-col>
    <v-col id="NewsDisplay">
      <NewsDisplay/>
    </v-col>
  </v-row>
  <v-row id="lowerRow" style="height: 70vh; width: 100%">
    <v-col style="width: 83vw">
      <StockRecommendation/>
    </v-col>
    <v-col>
      <h1 style="justify-content: center; align-items: center; display:grid; height: 30vh;"><center>Wordcloud</center></h1>
    </v-col>
  </v-row>
</div>
</template>

<style lang="scss">
html,
body {
  width: 100%;
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
    width: 83vw;
    height: 30vh;
    // display: block;
    // overflow: auto; 
    position: plex;
}

.priceDisplayVue{
  height: 70vh
}
</style>
