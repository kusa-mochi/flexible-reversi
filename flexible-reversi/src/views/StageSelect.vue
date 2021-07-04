<template>
  <div class="stage-select">
    <p>stage select</p>
    <router-link to="/">Top</router-link>
    <router-link to="/game">Game</router-link>
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
    this.currentPage = "stage-select";
  },
  name: "StageSelect",
};
</script>

<style></style>
