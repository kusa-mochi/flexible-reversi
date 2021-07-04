<template>
  <div class="top">
    <p>top</p>
    <img alt="app logo" src="../assets/logo_mochi.png" />
    <router-link to="/stage-select">Start</router-link>
    <router-link to="/settings">Settings</router-link>
  </div>
</template>

<script>
// // @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";

export default {
  components: {
    // HelloWorld,
  },
  computed: {
    currentPage: {
      get() {
        return this.$store.state.currentPage;
      },
      set(newValue) {
        this.$store.state.currentPage = newValue;
      },
    },
  },
  created() {
    this.currentPage = "top";
  },
  name: "Top",
};
</script>
