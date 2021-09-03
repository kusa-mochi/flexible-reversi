<template>
  <div class="game" :class="{ 'game--wait': !isMyTurn }">
    <p>game</p>
    <el-button @click="onExitButtonClick" icon="el-icon-back">退室</el-button>
    <p>
      {{ gameData.currentPlayerColor === 1 ? "黒" : "白" }}({{
        isMyTurn ? "あなた" : "相手"
      }})の番です。
    </p>
    <div class="board-container">
      <reversi-board
        @initialized="onInitialized"
        @stone-put="onStonePut"
        :board-width="800"
        :board-status="boardStatus"
        :is-read-only="isJustViewing"
        :player-color="gameData.currentPlayerColor"
      ></reversi-board>
      <div class="hajime-label-container">
        <div
          v-if="hajimeLabelVisilibity"
          class="hajime-label hajime-label--showing"
        >
          はじめ
        </div>
      </div>
      <div class="win-label-container">
        <div v-if="winLabelVisibility" class="win-label win-label--showing">
          勝利！
        </div>
      </div>
      <div class="lose-label-container">
        <div v-if="loseLabelVisibility" class="lose-label lose-label--showing">
          敗北。。
        </div>
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
    boardStatus: {
      get() {
        return this.$store.state.gameData.boardStatus;
      },
    },
    isJustViewing: {
      get() {
        return this.$store.state.gameData.isJustViewing;
      },
      set(newValue) {
        this.$store.state.gameData.isJustViewing = newValue;
      },
    },
    isGameReady: {
      get() {
        return this.$store.state.isGameReady;
      },
      set(newValue) {
        this.$store.state.isGameReady = newValue;
      },
    },
    isGaming: {
      get() {
        return this.$store.state.isGaming;
      },
      set(newValue) {
        this.$store.state.isGaming = newValue;
      }
    },
    isMyTurn: {
      get() {
        return this.$store.state.isMyTurn;
      },
      set(newValue) {
        this.$store.state.isMyTurn = newValue;
      },
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
    // // if not accessed from "room list" page.
    // if (this.currentPage !== "room-list") {
    //   // redirect to top page.
    //   this.$router.push("/");
    //   return;
    // }

    // create a WebSocket instance.
    if (this.socket === null) {
      this.initializeWebSocket();
    }

    this.currentPage = "game";
  },
  data() {
    return {
      hajimeLabelVisilibity: false,
      numEmpty: 0,
      numBlack: 0,
      numWhite: 0,
      socket: null,
      loseLabelVisibility: false,
      winLabelVisibility: false,
    };
  },
  methods: {
    initializeWebSocket() {
      this.socket = new WebSocket(this.serverUrl);
      let gotRoomData = false;

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
          console.log("received getRooms");
          const getRoomsData = parsedData.data;
          this.$store.commit("updateLocalRoomsData", getRoomsData);

          // prevent subsequent processes from being called more than once.
          if (gotRoomData) return;
          else gotRoomData = true;

          // make a connection to the server side (lambda).
          this.socket.send(
            JSON.stringify({
              action: "gameStandby",
              data: {
                token: this.token,
                nickname: this.myNickname,
                roomId: this.gameData.roomId,
              },
            })
          );
        } else if (
          parsedData.dataType === "gameStandby" &&
          this.isGameReady === false
        ) {
          console.log("received gameStandby");
          // if you are a room author
          if (this.amIRoomAuthor) {
            this.$notify({
              title: "Info",
              message: parsedData.data.opponentName + "さんが入室しました。",
              type: "success",
            });
          }

          // start game.

          this.hajimeLabelVisilibity = true;
          window.setTimeout(() => {
            this.hajimeLabelVisilibity = false;
          }, 3000);
          new Audio(require("@/assets/sounds/don.mp3")).play();
          this.isJustViewing = parsedData.data.currentPlayer !== "you";
          this.gameData.myColor =
            parsedData.data.currentPlayer === "you" ? 1 : 2;
          this.isMyTurn = parsedData.data.currentPlayer === "you";
          this.gameData.currentPlayerColor = 1;
          this.isGameReady = true;
          this.isGaming = true;
        } else if (parsedData.dataType === "putStone") {
          console.log("received putStone");
          new Audio(require("@/assets/sounds/put-stone.mp3")).play();
          this.boardStatus.splice(0, this.boardStatus.length);
          parsedData.data.boardStatus.forEach((row) => {
            this.boardStatus.push(row.slice());
          });

          switch (parsedData.data.nextPlayer) {
            case "you":
              console.log("next player is you.");
              this.gameData.currentPlayerColor = this.gameData.myColor;
              this.isJustViewing = false;
              this.isMyTurn = true;
              break;
            case "notYou":
              console.log("next player is not you.");
              this.gameData.currentPlayerColor =
                this.gameData.myColor == 1 ? 2 : 1;
              this.isJustViewing = true;
              this.isMyTurn = false;
              break;
            case "youWin":
              this.onGameSet(true);
              break;
            case "youLose":
              this.onGameSet(false);
              break;
            default:
              break;
          }
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
    onExitButtonClick() {
      this.$confirm("敗戦となりますが、退室しますか？", "退室確認", {
        confirmButtonText: "はい",
        cancelButtonText: "いいえ",
        type: "warning",
      }).then(() => {
        // TODO: send exit signal to the lambda.

        // go to the room list page.
        this.$router.push("/room-list");
      });
    },
    onInitialized(evt) {
      console.log("reversi board initialized.");
      console.log(evt);
    },
    // gameResult: true=win, false=lose
    onGameSet(gameResult) {
      console.log("game is set.");
      this.isJustViewing = true;
      this.isMyTurn = true;
      if (gameResult) {
        this.winLabelVisibility = true;
        window.setTimeout(() => {
          this.winLabelVisibility = false;
        }, 3000);
      } else {
        this.loseLabelVisibility = true;
        window.setTimeout(() => {
          this.loseLabelVisibility = false;
        }, 3000);
      }
      new Audio(require("@/assets/sounds/dodon.mp3")).play();
      this.isGaming = false;
    },
    onStonePut(evt) {
      const iColumn = evt.column;
      const iRow = evt.row;
      console.log(`put column:${iColumn} row:${iRow}`);

      // make the board readonly.
      this.isJustViewing = true;

      this.isMyTurn = false;

      // send put data to the lambda.
      this.socket.send(
        JSON.stringify({
          action: "putStone",
          data: {
            token: this.token,
            roomId: this.gameData.roomId,
            column: iColumn,
            row: iRow,
          },
        })
      );
    },
  },
  name: "Game",
};
</script>

<style lang="scss" scoped>
.game {
  position: relative;

  &--wait {
    cursor: wait;
  }
}

.board-container {
  position: relative;
  width: 800px;
}

.hajime-label-container,
.win-label-container,
.lose-label-container {
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
  .win-label,
  .lose-label {
    font-family: "ShokakiUtage";
    animation: hajimeKeyFrames 3s;
    white-space: nowrap;
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
