<template>
  <div id="stockRecommendation">
      <tree :data="tree" :zoomable="true" :marginY="-100" :marginX="0" layoutType="circular" class="tree" id="tree"></tree>
  </div>
</template>

<script>
import {tree} from 'vued3tree'

export default {
components: {
  tree
},
data() {
  return {
    tree: {
      name: "father",
      children:[{
        name: "son1",
        children:[ {name: "grandson"}, {name: "grandson2"}]
      },{
        name: "son2",
        children:[ {name: "grandson3"}, {name: "grandson4"}]
      }]
    }
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