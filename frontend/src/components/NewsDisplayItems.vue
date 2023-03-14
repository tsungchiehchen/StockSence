<template>
    <div class="item-inner">
      <div class="head">
        <span># {{ source.key }}</span>
        <span>{{ source.name }}</span>
      </div>
      <div class="desc">{{ source.desc }}</div>
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
  </style>