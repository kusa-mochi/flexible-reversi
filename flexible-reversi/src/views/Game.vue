<template>
  <div class="game">
    <p>game</p>
    <router-link to="/">Top</router-link>
    <reversi-board
      :board-width="800"
      :board-height="400"
      :board-status="currentBoardStatus"
      :num-columns="boardSize.width"
      :num-rows="boardSize.height"
    ></reversi-board>
  </div>
</template>

<script>
import ReversiBoard from "@/components/ReversiBoard";

export default {
  components: {
    ReversiBoard,
  },
  computed: {
    boardSize: {
      get() {
        return this.$store.state.stageSettings.boardSize;
      },
    },
    currentPage: {
      get() {
        return this.$store.state.currentPage;
      },
      set(newValue) {
        this.$store.state.currentPage = newValue;
      },
    },
    initialBoardStatus: {
      get() {
        return this.$store.state.stageSettings.initialStatus;
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
    this.currentBoardStatus = this.initialBoardStatus;
  },
  data() {
    return {
      currentBoardStatus: [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 1, 0, 0, 0],
        [0, 0, 0, 1, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
      ],
    };
  },
  name: "Game",
};
</script>

<style></style>
