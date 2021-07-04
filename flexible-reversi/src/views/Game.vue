<template>
  <div class="game">
    <p>game</p>
    <router-link to="/">Top</router-link>
    <reversi-board></reversi-board>
  </div>
</template>

<script>
import ReversiBoard from "@/components/ReversiBoard";

export default {
  components: {
    ReversiBoard,
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
