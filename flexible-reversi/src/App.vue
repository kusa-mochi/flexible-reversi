<template>
  <div id="app">
    <div class="app-container">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    serverUrl: {
      get() {
        return this.$store.state.serverUrl;
      },
    },
    token: {
      get() {
        return this.$store.state.token;
      },
    },
  },
  created() {
    window.addEventListener("beforeunload", this.onBeforeUnloadApp);
  },
  destroyed() {
    window.removeEventListener("beforeunload", this.onBeforeUnloadApp);
  },
  methods: {
    onBeforeUnloadApp() {
      if (!this.token) return;
      const socket = new WebSocket(this.serverUrl);
      socket.send(
        JSON.stringify({
          action: "deleteToken",
          data: {
            token: this.token,
          },
        })
      );
    },
  },
  name: "App",
};
</script>

<style lang="scss">
@import url("https://fonts.googleapis.com/css2?family=Roboto&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Bungee+Inline&display=swap");

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
  color: #2a2a2a;
}

.app-container {
  // max-width: 800px;
  width: 100%;
  height: 100%;
  background-color: #eeeeee;
}

.el-message-box__wrapper .el-message-box {
  width: unset;
}
</style>
