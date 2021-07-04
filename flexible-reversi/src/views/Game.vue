<template>
  <div class="game">
    <p>game</p>
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
    // if not accessed from "stage select" page.
    if (this.currentPage !== "stage-select") {
      // redirect to top page.
      this.$router.push("/");
    }
    this.currentPage = "game";
  },
  name: "Game",
};
</script>

<style></style>
