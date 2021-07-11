<template>
  <div class="game">
    <p>game</p>
    <router-link to="/">Top</router-link>
    <p>Player: {{this.currentPlayer === 1 ? "Black" : "White"}}</p>
    <p>Empty: {{this.numEmpty}}</p>
    <p>Black: {{this.numBlack}}</p>
    <p>White: {{this.numWhite}}</p>
    <reversi-board
      @click-cell="onClickCell"
      :board-width="800"
      :board-height="400"
      :initial-board-status="initialBoardStatus"
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

    // // initialize board.
    // this.currentBoardStatus = new Array(this.boardSize.height);
    // for (let iRow = 0; iRow < this.boardSize.height; iRow++) {
    //   this.currentBoardStatus[iRow] = this.initialBoardStatus[iRow].slice();
    // }
  },
  data() {
    return {
      // currentBoardStatus: null,
      // 1:black, 2:white
      currentPlayer: 1,
      numEmpty: 0,
      numBlack: 0,
      numWhite: 0
    };
  },
  methods: {
    onClickCell(evt) {
      console.log("Game - onClickCell begin.");
      console.log(evt);
      this.currentPlayer = evt.nextPlayer;
      this.numEmpty = evt.afterStatus.numEmpty;
      this.numBlack = evt.afterStatus.numBlack;
      this.numWhite = evt.afterStatus.numWhite;
    }
  },
  name: "Game",
};
</script>

<style></style>
