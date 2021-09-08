<template>
  <div id="game" class="game" :class="{ 'game--wait': !isMyTurn }">
    <div class="game__header">
      <div class="header-left">
        <el-button
          @click="onExitButtonClick"
          class="exit-button"
          icon="el-icon-back"
          >退室</el-button
        >
        <p>
          {{ gameData.currentPlayerColor === 1 ? "黒" : "白" }}({{
            isMyTurn ? "あなた" : "相手"
          }})の番です。
        </p>
      </div>
      <div class="header-right">
        <el-badge :hidden="chatBadgeHidden" is-dot>
          <el-button
            @click="onChatWindowToggle"
            circle
            icon="el-icon-chat-dot-round"
          ></el-button>
        </el-badge>
      </div>
    </div>
    <div class="game__body">
      <div class="board-container">
        <reversi-board
          @initialized="onInitialized"
          @stone-put="onStonePut"
          :board-width="boardPxWidth"
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
          <div
            v-if="loseLabelVisibility"
            class="lose-label lose-label--showing"
          >
            敗北。。
          </div>
        </div>
      </div>
    </div>
    <el-dialog
      :close-on-click-modal="false"
      :close-on-press-escape="true"
      :modal="false"
      :visible.sync="chatVisibility"
      id="chat-window"
      :show-close="false"
      :width="chatWindowWidth"
    >
      <div class="chat-log">
        <div v-for="logItem in chatLogs" :key="logItem.key" class="log-record">
          <div class="log-record__nickname">{{ logItem.nickname }}</div>
          <div class="log-record__colon">:</div>
          <div class="log-record__message">{{ logItem.message }}</div>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-form
          @submit.native.prevent="onChatSubmit"
          :inline="true"
          :model="chatForm"
        >
          <el-input
            v-model="chatForm.chatInput"
            placeholder="対戦相手とのチャットだよ"
          >
            <el-button
              @click="onChatSubmit"
              slot="append"
              icon="el-icon-s-promotion"
            ></el-button>
          </el-input>
        </el-form>
      </span>
    </el-dialog>
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
    boardPxWidth: {
      get() {
        if (this.windowWidth < 800) {
          return this.windowWidth;
        } else {
          return 800;
        }
      },
    },
    chatWindowWidth: {
      get() {
        if (this.windowWidth <= 416) {
          return `${this.windowWidth * 0.96}px`;
        } else {
          return "400px";
        }
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
      },
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
      chatBadgeHidden: true,
      chatForm: {
        chatInput: "",
      },
      chatLogCounter: 0,
      chatLogs: [
        // {
        //   nickname: "くさもち",
        //   message:
        //     "こんにちはあああああああああああああああああああああああああああああああああ",
        //   key: 0,
        // },
      ],
      chatVisibility: false,
      hajimeLabelVisilibity: false,
      numEmpty: 0,
      numBlack: 0,
      numWhite: 0,
      socket: null,
      loseLabelVisibility: false,
      winLabelVisibility: false,
      windowWidth: 800,
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
            this.$store.dispatch("playSound", "info.mp3");
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
          this.$store.dispatch("playSound", "don.mp3");
          this.isJustViewing = parsedData.data.currentPlayer !== "you";
          this.gameData.myColor =
            parsedData.data.currentPlayer === "you" ? 1 : 2;
          this.isMyTurn = parsedData.data.currentPlayer === "you";
          this.gameData.currentPlayerColor = 1;
          this.isGameReady = true;
          this.isGaming = true;
        } else if (parsedData.dataType === "putStone") {
          console.log("received putStone");
          this.$store.dispatch("playSound", "put-stone.mp3");
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
        } else if (parsedData.dataType === "exitRoomDuringGame") {
          console.log("received exitRoom");
          this.onGameSet(true, "oppponentExit");
        } else if (parsedData.dataType === "sendChat") {
          this.$store.dispatch("playSound", "receive-chat.mp3");
          this.chatLogs.unshift({
            nickname: parsedData.data.nickname,
            message: parsedData.data.message,
            key: this.chatLogCounter++,
          });

          // new chat notification
          if (!this.chatVisibility) {
            this.chatBadgeHidden = false;
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
    onChatWindowToggle() {
      this.chatVisibility = !this.chatVisibility;
      if (this.chatVisibility) {
        this.chatBadgeHidden = true;
      }
    },
    onChatSubmit() {
      // send input text to opponent through lambda.
      this.socket.send(
        JSON.stringify({
          action: "sendChat",
          data: {
            token: this.token,
            message: this.chatForm.chatInput,
            roomId: this.gameData.roomId,
          },
        })
      );

      this.chatForm.chatInput = "";
    },
    onExitButtonClick() {
      if (this.isGaming) {
        this.$confirm("敗戦となりますが、退室しますか？", "退室確認", {
          confirmButtonText: "はい",
          cancelButtonText: "いいえ",
          type: "warning",
        }).then(() => {
          // send exit signal to the lambda.
          this.socket.send(
            JSON.stringify({
              action: "exitRoomDuringGame",
              data: {
                token: this.token,
                roomId: this.gameData.roomId,
              },
            })
          );

          this.onGameSet(false);
          window.setTimeout(() => {
            this.$store.dispatch("playSound", "open-door.mp3");
            // go to the room list page.
            this.$router.push("/room-list");
          }, 2000);
        });
      } else {
        // reset params.
        this.isJustViewing = true;
        this.isMyTurn = false;
        this.isGameReady = false;
        this.isGaming = false;

        this.$store.dispatch("playSound", "open-door.mp3");

        // send exit signal to the lambda.
        this.socket.send(
          JSON.stringify({
            action: "exitRoom",
            data: {
              token: this.token,
              roomId: this.gameData.roomId,
            },
          })
        );

        // go to the room list page.
        this.$router.push("/room-list");
      }
    },
    onInitialized(evt) {
      console.log("reversi board initialized.");
      console.log(evt);
    },
    // gameResult: true=win, false=lose
    onGameSet(gameResult, whyGameSet) {
      console.log("game is set.");
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
      this.$store.dispatch("playSound", "dodon.mp3");

      // reset params.
      this.isJustViewing = true;
      this.isMyTurn = false;
      this.isGameReady = false;
      this.isGaming = false;

      // reason of game set
      switch (whyGameSet) {
        case "oppponentExit":
          this.$store.dispatch("playSound", "info.mp3");
          this.$notify({
            title: "Info",
            message: "対戦相手の退室により勝利しました。",
            type: "info",
          });
          break;
        default:
          break;
      }
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
    onWindowResize() {
      this.windowWidth = window.innerWidth;
    },
  },
  mounted() {
    this.windowWidth = window.innerWidth;
    window.addEventListener("resize", this.onWindowResize);
  },
  name: "Game",
};
</script>

<style lang="scss" scoped>
$headerHeight: 56px;

.game {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;

  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: flex-start;
  align-items: center;

  &--wait {
    cursor: wait;
  }
}

.game-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  opacity: 0.6;
  z-index: 0;

  background-color: black;
  height: 100%;
}

.game__header {
  position: relative;
  width: 100%;
  height: $headerHeight;
  background-color: rgba(white, 0.95);

  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  align-content: center;

  .header-left {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: flex-start;
    align-items: center;
    align-content: center;

    position: relative;

    .exit-button {
      position: relative;
      margin: 8px;
      z-index: 10;
    }
  }

  .header-right {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: flex-start;
    align-items: center;
    align-content: center;

    position: relative;
    margin: 8px;
    z-index: 10;
  }
}

.game__body {
  position: relative;
  width: 100%;
  height: calc(100% - #{$headerHeight});
  overflow: hidden;

  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  align-items: flex-start;
  align-content: flex-start;

  flex-grow: 1;
}

.board-container {
  position: relative;
  width: 100%;

  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: flex-start;
  align-items: center;
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

.chat-log {
  position: relative;
  width: 100%;
  height: 410px;
  background-color: rgba(black, 0.1);
  overflow-x: hidden;
  overflow-y: auto;

  display: flex;
  flex-direction: column-reverse;
  flex-wrap: nowrap;

  .log-record {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: flex-start;
    align-items: flex-start;

    position: relative;
    width: 100%;
    margin: 4px;

    &__nickname {
      position: relative;
      width: 96px;
    }
    &__colon {
      position: relative;
      width: 16px;
    }
    &__message {
      position: relative;
      width: calc(100% - 96px - 16px);
    }
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

@media screen and (max-width: 550px) {
  @keyframes hajimeKeyFrames {
    0% {
      opacity: 0;
      font-size: 150px;
    }
    6% {
      opacity: 0.7;
      font-size: 115px;
    }
    12% {
      opacity: 1;
      font-size: 92px;
    }
    75% {
      opacity: 1;
      font-size: 92px;
    }
    100% {
      opacity: 0;
      font-size: 92px;
    }
  }
}
</style>

<style lang="scss">
#game {
  .game__header {
    .el-icon-chat-dot-round {
      font-size: 20px;
    }
    .el-button.is-circle {
      & + .el-badge__content.is-dot {
        top: 7px;
        right: 14px;
        width: 16px;
        height: 16px;
      }
    }
  }
}

#chat-window {
  // no click/tap events on the dialog mask.
  pointer-events: none;

  .el-dialog {
    position: absolute;
    margin: 0;
    margin-top: 0 !important;
    top: 64px;
    right: 8px;
    height: 510px;
    pointer-events: auto;
  }
  .el-dialog__header {
    padding: 0;
  }
  .el-dialog__body {
    padding: 20px 20px 0 20px;
  }
  .el-dialog__footer {
    padding: 20px;
  }
  .el-icon-s-promotion {
    font-size: 24px;
  }
}
</style>
