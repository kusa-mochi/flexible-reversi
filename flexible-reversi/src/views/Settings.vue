<template>
  <div class="settings">
    <p>settings</p>
    <router-link to="/about">About</router-link>
    <router-link to="/">Top</router-link>
  </div>
</template>

<script>
export default {
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
    this.currentPage = "settings";
  },
  name: "Settings",
};
</script>

<style></style>
