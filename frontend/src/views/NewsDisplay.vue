<template>
  <div id="app">
    <div class="wrapper">
      <virtual-list 
        class="list"
        style="overflow-y: auto; height: 62vh;"
        data-key="key"
        :data-sources="computedItems"
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

export default {
  name: 'App',
  data() {
    return {
      itemComponent: Item,
      items: [
        { price: '1', name: 'mm', desc: '123' },
        { price: '22', name: 'aa' },
        { price: '55', name: 'dd' },
        { price: '77', name: 'gg' },
        { price: '123', name: 'kk' },
        { price: '53', name: 'mn' },
        { price: '11', name: 'mm' },
        { price: '22', name: 'a' },
        { price: '33', name: 'd' },
        { price: '77', name: 'g' },
        { price: '1283', name: 'k' },
        { price: '589', name: 'n' }
      ]
    }
  },
  computed: {
    computedItems() {
      return this.items.map((item, index) => {
        item.key = `${index+1}`
        return item
      })
    }
  }
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