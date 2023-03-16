<template>
  <div id="app">
    <div class="wrapper">
      <virtual-list 
        class="list"
        style="overflow-y: auto; height: 48vh;"
        data-key="key"
        :data-sources="items"
        :data-component="itemComponent"
        :estimate-size="80"
        :item-class="'list-item-dynamic'"
      />
    </div>
  </div>
</template>

<script>
import Item from '../components/NewsDisplayItems'
import { getData } from '../components/data'
import VirtualList from 'vue-virtual-scroll-list'
import newsJson from '../../../backend/dataset/NewsSentimentList.json'

export default {
  name: 'App',
  data() {
    return {
      itemComponent: Item,
      items: []
    }
  },
  mounted(){
    const url = new URL(window.location.href)
    var rate = url.searchParams.get('rate')
    
    var processedItems = []
    var key = 1
    //console.log(newsJson[0])
    for (var i = 0; i < 3; i++) {
      for (var j = 0; j < newsJson[i].length; j++){
        if(rate >= 0){
          if(i == 0){
            var color = "color: #42b883"
          }
          else if(i == 1){
            color = "color: #787878"
          }
          else{
            color = "color: #e54050"
          }
        }
        else{
          if(i == 0){
            color = "color: #e54050"
          }
          else if(i == 1){
            color = "color: #787878"
          }
          else{
            color = "color: #42b883"
          }
        }
        let news = {
          "key": key,
          "name": newsJson[i][j].title + " (" + newsJson[i][j].datetime + ")",
          "desc": newsJson[i][j].desc,
          "color": color
        }
        key++
        processedItems.push(news)
      }
    }
    //console.log(processedItems)
    this.items = processedItems
  }
  // computed: {
  //   computedItems() {
      

  //     // return this.items.map((item, index) => {
  //     //   item.key = `${index+1}`
  //     //   return item
  //     // })
  //   }
  // }
}
</script>

<style>
.list {
  width: 100%;
  height: 500px;
  border: 2px solid;
  border-radius: 3px;
  overflow-y: auto;
  border-color: dimgray;
}
.list-item-dynamic {
    display: flex;
    align-items: center;
    padding: 1em;
    border-bottom: 1px solid;
    border-color: lightgray;
}

</style>