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
      :is-read-only="isJustViewing"
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
        return this.$store.state.gameData.boardSize;
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
    gameData: {
      get() {
        return this.$store.state.gameData;
      },
      set(newValue) {
        this.$store.state.gameData = newValue;
      },
    },
    initialBoardStatus: {
      get() {
        return this.$store.state.gameData.initialBoardStatus;
      },
    },
    isJustViewing: {
      get() {
        return this.$store.state.gameData.isJustViewing;
      },
    },
    serverUrl: {
      get() {
        return this.$store.state.serverUrl;
      },
    },
  },
  created() {
    // if not accessed from "room list" page.
    if (this.currentPage !== "room-list") {
      // redirect to top page.
      this.$router.push("/");
    }

    // create a WebSocket instance.
    if (this.socket === null) {
      this.initializeWebSocket();
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
      socket: null,
    };
  },
  methods: {
    initializeWebSocket() {
      this.socket = new WebSocket(this.serverUrl);
      this.socket.onopen = (e) => {
        console.log("onopen");
        console.log(e);
      };
      this.socket.onmessage = (e) => {
        console.log("onmessage");
        console.log(e);
      };
      this.socket.onclose = (e) => {
        console.log("onclose");
        console.log(e);
      };
      this.socket.onerror = (e) => {
        console.log("onerror");
        console.log(e);
      };
    },
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
