<template>
  <div class="settings">
    <p>settings</p>
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
    // if not accessed from "top" page.
    if (this.currentPage !== "top") {
      // redirect to top page.
      this.$router.push("/");
      return;
    }
    this.currentPage = "settings";
  },
  name: "Settings",
};
</script>

<style></style>
