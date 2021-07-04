<template>
  <div id="app">
    <div class="app-container">
      <router-view />
    </div>
  </div>
</template>

<style lang="scss">
* {
  margin: 0;
  padding: 0;
  color: black;
  box-sizing: border-box;
}

html,
body {
  width: 100%;
  height: 100%;
}

#app {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: center;
  align-items: stretch;

  width: 100%;
  height: 100%;
}

.app-container {
  // max-width: 800px;
  width: 100%;
  height: 100%;
  background-color: #eeeeee;
}
</style>
