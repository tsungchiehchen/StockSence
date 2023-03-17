<template>
    <div class="item-inner" style="width:100%">
      <div class="head">
        <span># {{ source.key }}</span>
        <span style="word-wrap:break-word;" :style="source.color" >{{ source.name }}</span>
      </div>
      <div style="margin-top: 10px; text-align: center;">
        <v-btn color="#1E88A8" class="white--text ma-2" style="color:white" :href="source.desc" target="_blank" rel="noopener noreferrer">Open News
        <v-icon right dark>
          mdi-open-in-new
        </v-icon>
        </v-btn>
      </div>
    </div>
  </template>
  
  <script>
  
  export default {
    name: 'dynamic-size-item',
  
    props: {
      source: {
        type: Object,
        default () {
          return {}
        }
      }
    },

    mounted(){
      document.querySelector('.test');
    }
  }
  </script>
  
  <style>
.head {
    font-weight: bold;
}
span:first-child {
    margin-right: 1em;
}
.desc {
    padding-top: .5em;
    text-align: justify;
}
.v-btn__content{
  margin-right: 0px !important;
}
  </style>