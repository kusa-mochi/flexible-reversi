<template>
  <div id="app">
    <div class="app-container">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style lang="scss">
@import url("https://fonts.googleapis.com/css2?family=Roboto&display=swap");
@import url('https://fonts.googleapis.com/css2?family=Bungee+Inline&display=swap');

* {
  margin: 0;
  padding: 0;
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
  font-family: "Roboto", sans-serif;
}

.app-container {
  // max-width: 800px;
  width: 100%;
  height: 100%;
  background-color: #eeeeee;
}
</style>
