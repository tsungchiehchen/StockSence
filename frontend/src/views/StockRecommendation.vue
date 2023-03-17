<template>
  <div id="stockRecommendation" style="width: 100%">
    <div style="margin-top: -15px; position: absolute; margin-left: 20px; z-index: 10000">
          <v-btn variant="outlined" color="rgb(66, 184, 131)" style="margin:0 auto 0px auto; display:inline-block; padding-left: 10px; padding-right: 10px; padding-bottom: 5px; color:white;" v-on:click="changeToCluster">Cluster</v-btn>
          <v-btn variant="outlined" color="rgb(229, 64, 80)" @click="treePopup=true" style="margin: 0 auto 0px 10px; display:inline-block; padding-left: 10px; padding-right: 10px; padding-bottom: 5px; color:white;" v-on:click="changeToTree">Tree</v-btn>
    </div>
    <div id="vued3tree">
    <tree :data="tree" :zoomable="true" :marginY="-100" :marginX="0" layoutType="horizontal" :type="treeType" class="tree" id="tree"></tree>
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
    treeType: null
  }
},
mounted(){
  const url = new URL(window.location.href);
  var treeType = url.searchParams.get('treeType')
  console.log(treeType)
  this.treeType = treeType

  if (recommendationJson && Object.keys(recommendationJson).length === 0 && Object.getPrototypeOf(recommendationJson) === Object.prototype){  // 沒有相似的 stock
    document.getElementById("vued3tree").style.display = 'none';
    document.getElementById("noSimilarStock").style.display = 'block';
  }
  else{
    document.getElementById("vued3tree").style.display = 'block';
    document.getElementById("noSimilarStock").style.display = 'none';
  }
},
  methods:{
    changeToCluster: function(event){
      var url = new URL(window.location.href);
      var urlString = String(url)
      if(urlString.includes("treeType")){
        var payload = url.href.split('&treeType=')[0]
        var newURL = payload + "&treeType=" + "cluster"
        window.location.href = newURL;
      }
      else{
        payload = url.href.split('#')[0]
        newURL = payload + "&treeType=" + "cluster"
        window.location.href = newURL;
      }
    },
    changeToTree: function(event){
      var url = new URL(window.location.href);
      var urlString = String(url)
      if(urlString.includes("treeType")){
        var payload = url.href.split('&treeType=')[0]
        var newURL = payload + "&treeType=" + "tree"
        window.location.href = newURL;
      }
      else{
        payload = url.href.split('#')[0]
        newURL = payload + "&treeType=" + "tree"
        window.location.href = newURL;
      }
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