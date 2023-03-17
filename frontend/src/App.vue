<script lang="ts">
import PriceDisplay from "./views/PriceDisplay.vue"
import StockRecommendation from "./views/StockRecommendation.vue"
import Toolbox from "./views/Toolbox.vue"
import NewsDisplay from "./views/NewsDisplay.vue"
import WordCloud from "./views/Wordcloud.vue"

export default {
  name: 'StockSense',
  components: {
    PriceDisplay,
    Toolbox,
    NewsDisplay,
    StockRecommendation,
    WordCloud
  }
}

document.title = "StockSense"

</script>


<template>
  <div id="container">
  <v-row no-gutters id="upperRow" style="height: 70vh; width: 100%;">
    <v-col no-gutters id="priceDisplay" style="justify-content: center; align-items: center; display:grid; width:95%; margin: 15px 7.5px 7.5px 15px; padding: 10px 10px 5px 10px">
      <PriceDisplay/>
    </v-col>
    <v-col no-gutters id="NewsDisplay&Toolbox" style="padding: 0px 0px 0px 0px;">
      <div id="toolbox" style="margin: 15px 15px 15px 7.5px; height: 13vh; padding: 15px 15px 15px 15px;">
        <Toolbox/>
      </div>
      <div id="news-display" style="margin: 7.5px 15px 7.5px 7.5px; height:52.5vh; padding: 15px 15px 15px 15px;">
        <NewsDisplay/>
      </div>
    </v-col>
  </v-row>
  <v-row no-gutters id="lowerRow" style="height: 30vh; width: 100%;">
    <v-col no-gutters style="justify-content: center; align-items: center; display:grid; flex-basis: 30%; margin: 5px 7.5px 15px 15px;" id="stockRecommendation">
      <StockRecommendation/>
    </v-col>
    <v-col no-gutters id="wordcloud" style="justify-content: center; align-items: center; margin: 5px 15px 15px 7.5px;">
      <WordCloud/>
    </v-col>
  </v-row>
</div>
</template>

<style lang="scss">
html,
body {
  width: 100%;
  height: 100%;
  min-width: 1300px;
  margin: 0;
  overflow-y: hidden;
  overflow-x: scroll;
  font: 15px -apple-system,BlinkMacSystemFont,
  Segoe UI,Roboto,Oxygen,Ubuntu,Cantarell,
  Fira Sans,Droid Sans,Helvetica Neue,sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  position: flex;
  background-color: #BDC0BA;
}

#priceDisplay, #news-display, #stockRecommendation, #wordcloud, #toolbox {
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
    width: 80vw;
    height: 20vh;
    // display: block;
    // overflow: auto; 
    position: plex;
}

.Price-History { grid-area: Price-History; }

.toolbox { grid-area: toolbox; }

.news-display { grid-area: news-display; }

.News-Recommendation { grid-area: News-Recommendation; }

.Wordcloud { grid-area: Wordcloud; }

div.tooltip {
    position: absolute;
    width: auto;
    height: auto;
    padding: 8px;
    color: white;
    background: black;
    border: 0px;
    border-radius: 10px;
    pointer-events: none;
}
</style>
