<script lang="ts">
import PriceDisplay from "./views/PriceDisplay.vue"
import StockRecommendation from "./views/StockRecommendation.vue"
import NewsDisplay from "./views/NewsDisplay.vue"

export default {
  name: 'StockSense',
  components: {
    PriceDisplay,
    NewsDisplay
  }
}

document.title = "StockSense"

</script>


<template>
  <div>
  <v-row id="upperRow" style="height: 70vh; width: 100%;">
    <v-col id="priceDisplay" style="justify-content: center; align-items: center; display:grid; width:95%; margin: 25px 7.5px 15px 25px; padding: 10px 10px 5px 10px">
      <PriceDisplay/>
    </v-col>
    <v-col id="NewsDisplay" style="align-items: center; display:grid; width:30%; margin: 25px 0px 15px 7.5px;">
      <NewsDisplay/>
    </v-col>
  </v-row>
  <v-row id="lowerRow" style="height: 30vh; width: 100%; margin-top: 15px;">
    <v-col style="justify-content: center; align-items: center; display:grid; flex-basis: 45em; margin: 5px 7.5px 5px 25px;" id="stockRecommendation">
      <h1 style=""><center>Stock Recommendation Vue</center></h1>
      <!-- <StockRecommendation/> -->
    </v-col>
    <v-col id="wordcloud" style="justify-content: center; align-items: center; display:grid; margin: 5px 0px 5px 7.5px;">
      <h1 style=""><center>Wordcloud</center></h1>
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
  background-color: #BDC0BA;
}

#priceDisplay, #NewsDisplay, #stockRecommendation, #wordcloud {
  -webkit-border-radius: 15px;
  -moz-border-radius: 15px;
  border-radius: 15px;
  border: none;
  background-color: #FFF;
}

.fixTimeRangeCheckBox {
  position: absolute;
  top: 50px;
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
</style>
