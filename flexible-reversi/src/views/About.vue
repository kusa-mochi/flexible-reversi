<template>
  <div class="about">
    <h1>This is an about page</h1>
    <router-link to="/settings">Settings</router-link>
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
    }
    this.currentPage = "about";
  },
  name: "About",
};
</script>

<style></style>
