<template>
  <div class="game">
    <p>game</p>
    <router-link to="/">Top</router-link>
    <p>Player: {{ this.currentPlayer === 1 ? "Black" : "White" }}</p>
    <p>Empty: {{ this.numEmpty }}</p>
    <p>Black: {{ this.numBlack }}</p>
    <p>White: {{ this.numWhite }}</p>
    <div class="board-container">
      <reversi-board
        @initialized="onInitialized"
        @click-cell="onClickCell"
        @pass-turn="onPassTurn"
        @game-set="onGameSet"
        :board-width="800"
        :initial-board-status="initialBoardStatus"
        :is-read-only="isJustViewing"
      ></reversi-board>
      <div class="hajime-label-container">
        <!-- <transition name="hajime-animation"> -->
        <div
          v-if="hajimeLabelVisilibity"
          class="hajime-label hajime-label--showing"
        >
          はじめ
        </div>
        <!-- </transition> -->
      </div>
      <div class="sokomade-label-container">
        <!-- <transition name="sokomade-animation"> -->
        <div
          v-if="sokomadeLabelVisibility"
          class="sokomade-label sokomade-label--showing"
        >
          そこまで
        </div>
        <!-- </transition> -->
      </div>
    </div>
  </div>
</template>

<script>
import ReversiBoard from "@/components/ReversiBoard";

export default {
  components: {
    ReversiBoard,
  },
  computed: {
    amIRoomAuthor: {
      get() {
        const roomId = this.gameData.roomId;
        const roomAuthor = this.rooms[roomId - 1].roomAuthor;
        return this.myNickname === roomAuthor;
      },
    },
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
    room: {
      get() {
        return this.rooms[this.gameData.roomId];
      },
      set(newValue) {
        this.rooms[this.gameData.roomId] = newValue;
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
      set(newValue) {
        this.$store.state.gameData.isJustViewing = newValue;
      }
    },
    myNickname: {
      get() {
        return this.$store.state.myNickname;
      },
    },
    rooms: {
      get() {
        return this.$store.state.rooms;
      },
      set(newValue) {
        this.$store.state.rooms = newValue;
      },
    },
    serverUrl: {
      get() {
        return this.$store.state.serverUrl;
      },
    },
    token: {
      get() {
        return this.$store.state.token;
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
      hajimeLabelVisilibity: false,
      isGameReady: false,
      numEmpty: 0,
      numBlack: 0,
      numWhite: 0,
      socket: null,
      sokomadeLabelVisibility: false,
    };
  },
  methods: {
    initializeWebSocket() {
      this.socket = new WebSocket(this.serverUrl);
      this.socket.onopen = (e) => {
        console.log("onopen");
        console.log(e);
        this.socket.send(
          JSON.stringify({
            action: "getRooms",
            data: {
              token: this.token,
            },
          })
        );
      };
      this.socket.onmessage = (e) => {
        console.log("onmessage");
        console.log(e);
        const parsedData = JSON.parse(e.data);
        console.log(parsedData);

        // check data type
        if (parsedData.dataType === "getRooms") {
          console.log("get rooms data.");
          const getRoomsData = parsedData.data;
          console.log(getRoomsData);
          this.$store.commit("updateLocalRoomsData", getRoomsData);

          console.log("room id");
          console.log(this.gameData.roomId);
          // make a connection to the server side (lambda).
          this.socket.send(
            JSON.stringify({
              action: "gameStandby",
              data: {
                token: this.token,
                roomId: this.gameData.roomId,
              },
            })
          );
        } else if (
          parsedData.dataType === "gameStandby" &&
          this.isGameReady === false
        ) {
          // if you are a room author
          if (this.amIRoomAuthor) {
            this.$notify({
              title: "Info",
              message: parsedData.data.opponentName + "さんが入室しました。",
              type: "success",
            });
          }

          this.hajimeLabelVisilibity = true;
          window.setTimeout(() => {
            this.hajimeLabelVisilibity = false;
          }, 3000);
          new Audio(require("@/assets/sounds/don.mp3")).play();

          this.isJustViewing = parsedData.data.currentPlayer === "opponent";

          this.isGameReady = true;
        }
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
      this.sokomadeLabelVisibility = true;
      window.setTimeout(() => {
        this.sokomadeLabelVisibility = false;
      }, 3000);
      new Audio(require("@/assets/sounds/dodon.mp3")).play();
    },
  },
  name: "Game",
};
</script>

<style lang="scss" scoped>
.game {
  position: relative;
}

.board-container {
  position: relative;
  width: 800px;
}

.hajime-label-container,
.sokomade-label-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;

  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: center;
  align-items: center;

  .hajime-label,
  .sokomade-label {
    font-family: "ShokakiUtage";
    animation: hajimeKeyFrames 3s;
  }
}

@keyframes hajimeKeyFrames {
  0% {
    opacity: 0;
    font-size: 250px;
  }
  6% {
    opacity: 0.7;
    font-size: 215px;
  }
  12% {
    opacity: 1;
    font-size: 200px;
  }
  75% {
    opacity: 1;
    font-size: 200px;
  }
  100% {
    opacity: 0;
    font-size: 200px;
  }
}
</style>
