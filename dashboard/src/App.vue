<script lang="ts">
import wordcloud from './components/WordCloud.vue'
import barchart from './components/BarChart.vue'


export default {
  name: 'app',
  components: {
    wordcloud,
    barchart
  }
}

</script>

<template>
  <div id="body" style="text-align: center">
    <v-container id="main-container" class="d-flex flex-column flex-nowrap" fluid>
      <v-row no-gutters>
        <v-col>
          <h1 class="title">Data Visualization for COVID-19 Open Research Dataset</h1>
          <br/><br/>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col>
          <h3 class="chartTitle">Most Frequent Words in Paper's Abstract</h3>
          <wordcloud/>
        </v-col>
        <v-col>
          <h3 class="chartTitle">Number of Papers by Publication Month Between Nov. 2019 to Jan. 2023</h3>
          <br>
          <barchart/>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col class="description">
          <p style="font-weight: bolder;"> Features: </p>
          <ul>
            <li>Frequently appearing words in abstracts will be displayed in larger font with a darker color</li>
            <li>Hover over a word to view its frequency</li>
          </ul>
          <p style="margin-top: 15px;font-weight: bolder;"> Insight: </p>
          As expected, the most frequent word in the abstracts of this COVID-19 dataset is 'COVID-19'. Since this dataset is research oriented, the second most frequent word is 'patient', followed by 'study' and 'pandemic'.
        </v-col>
        <v-col class="description">
          <p style="font-weight: bolder;"> Features: </p>
            <ul>
              <li>Displays a red line as the trend line of the chart</li>
              <li>Hover over any bar to view the number of papers in that month</li>
            </ul>
            <p style="margin-top: 15px;font-weight: bolder;"> Insight: </p>
            The chart shows a significant increase in the number of published papers, rising by over 10 times, at the outset of the pandemic in 2020. However, as the pandemic situation stabilized, the number of publications has decreased.
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<style>
#body {
  height: 850px;
  display:flex; flex-direction:column; justify-content:center;
}
.title {
  font-familt: 'Aerial';
  font-size: 35px;
  text-align: center;
}
.chartTitle {
  font-familt: 'Aerial';
  font-size: 20px;
  text-align: center;
  margin-right: 15px;
  margin-left: 15px;
}
.description {
  text-align: left;
  margin-top: 25px;
  margin-right: 35px;
  margin-left: 35px;
  font-size: 16px;
}
ul {
  list-style-position: inside;
  font-familt: 'Aerial';
}
</style>
