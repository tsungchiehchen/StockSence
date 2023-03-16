<template>
  <div id="stockRecommendation">
    <!-- <v-radio-group v-model="row" row style="position:absolute z-index:1000">
      <v-radio label="tree"></v-radio>
      <v-radio label="cluster"></v-radio>
    </v-radio-group> -->
    <div id="vued3tree">
    <tree :data="tree" :zoomable="true" :marginY="-100" :marginX="0" layoutType="horizontal" type="tree" class="tree" id="tree"></tree>
    </div>
    <div id="noSimilarStock">
      <h1>No similar stock under distance 5</h1>
    </div>
  </div>
</template>

<script>
import {tree} from 'vued3tree'
import recommendationJson from '../../../backend/dataset/stockRecommendation.json'
import Vue from 'vue'
import Vuesax from 'vuesax'
import 'vuesax/dist/vuesax.css'
import 'material-icons/iconfont/material-icons.css';

Vue.use(Vuesax)

export default {
components: {
  tree
},
data() {
  return {
    tree: recommendationJson,
    radioGroup: 1,
  }
},
mounted(){
  if (recommendationJson && Object.keys(recommendationJson).length === 0 && Object.getPrototypeOf(recommendationJson) === Object.prototype){  // 沒有相似的 stock
    document.getElementById("vued3tree").style.display = 'none';
    document.getElementById("noSimilarStock").style.display = 'block';
  }
  else{
    document.getElementById("vued3tree").style.display = 'block';
    document.getElementById("noSimilarStock").style.display = 'none';
  }
}
}
</script>

<style lang="stylus">
.examplex
  display: flex;
  align-items: center;
  justify-content: center;
  .a-icon
    outline: none;
    text-decoration: none !important;
    display: flex;
    align-items: center;
    justify-content: center;
    i
      font-size: 18px;
</style>