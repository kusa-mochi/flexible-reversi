<template>
  <div class="game">
    <p>game</p>
    <router-link to="/">Top</router-link>
    <p>Player: {{ this.currentPlayer === 1 ? "Black" : "White" }}</p>
    <p>Empty: {{ this.numEmpty }}</p>
    <p>Black: {{ this.numBlack }}</p>
    <p>White: {{ this.numWhite }}</p>
    <reversi-board
      @initialized="onInitialized"
      @click-cell="onClickCell"
      @pass-turn="onPassTurn"
      @game-set="onGameSet"
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
    // if not accessed from "room list" page.
    if (this.currentPage !== "room-list") {
      // redirect to top page.
      this.$router.push("/");
    }
    this.currentPage = "game";
  },
  data() {
    return {
      // currentBoardStatus: null,
      // 1:black, 2:white
      currentPlayer: 1,
      numEmpty: 0,
      numBlack: 0,
      numWhite: 0,
    };
  },
  methods: {
    onInitialized(evt) {
      console.log("Game -onInitialied begin.");
      console.log(evt);
      this.currentPlayer = evt.nextPlayer;
      this.numEmpty = evt.numEmpty;
      this.numBlack = evt.numBlack;
      this.numWhite = evt.numWhite;
    },
    onClickCell(evt) {
      console.log("Game - onClickCell begin.");
      console.log(evt);
      this.currentPlayer = evt.nextPlayer;
      this.numEmpty = evt.numEmpty;
      this.numBlack = evt.numBlack;
      this.numWhite = evt.numWhite;
    },
    onPassTurn(evt) {
      console.log("Game - onPassTurn begin.");
      console.log(evt);
      this.numEmpty = evt.numEmpty;
      this.numBlack = evt.numBlack;
      this.numWhite = evt.numWhite;
    },
    onGameSet(evt) {
      console.log("Game - onGameSet begin.");
      console.log(evt);
      this.numEmpty = evt.numEmpty;
      this.numBlack = evt.numBlack;
      this.numWhite = evt.numWhite;
      if (evt.numBlack > evt.numWhite) {
        console.log("Winner BLACK !!!");
      } else if (evt.numWhite > evt.numBlack) {
        console.log("Winner WHITE !!!");
      } else if (evt.numBlack === evt.numWhite) {
        console.log("Draw");
      }
    },
  },
  name: "Game",
};
</script>

<style></style>
