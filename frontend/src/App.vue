<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
  document.title = "StockSense"
</script>

<style lang="scss">
html,
body {
  height: 100%;
  margin: 0;
  overflow-y: hidden;
  overflow-x: hidden;
  font: 15px sans-serif;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}

.fixTimeRangeCheckBox {
  position: absolute;
  top: 13px;
  right: 80px;
  color: #888;
  font: 11px -apple-system,BlinkMacSystemFont,
  Segoe UI,Roboto,Oxygen,Ubuntu,Cantarell,
  Fira Sans,Droid Sans,Helvetica Neue,sans-serif
}
</style>
