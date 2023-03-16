<template>
  <div id="stockRecommendation">
      <tree :data="tree" :zoomable="true" :marginY="-100" :marginX="0" layoutType="horizontal" type="tree" class="tree" id="tree"></tree>
  </div>
</template>

<script>
import {tree} from 'vued3tree'
import recommendationJson from '../../../backend/dataset/stockRecommendation.json'

export default {
components: {
  tree
},
data() {
  return {
    tree: recommendationJson
  }
},
mounted(){
  // var treeCSS = document.getElementById("tree");
  // treeCSS.style = "height: " + (window.innerHeight*0.3) + "px";
  // treeCSS.style = "width: " + (window.innerWidth*0.8) + "px";
  // console.log(treeCSS)
}
}
</script>