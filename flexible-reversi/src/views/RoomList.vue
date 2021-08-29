<template>
  <div class="room-list">
    <router-link to="/">Top</router-link>
    <router-link to="/game">Game</router-link>
    <div>ようこそ{{ myNickname }}さん</div>
    <div class="rooms">
      <div
        v-for="room in rooms"
        :key="room.roomCounter"
        :class="`room ${room.roomState}`"
      >
        <div class="room-number">#{{ room.id }}</div>
        <div v-if="roomTitleVisible(room.roomState)" class="room-title">
          {{ room.roomName }}
        </div>
        <div v-if="roomAuthorVisible(room.roomState)" class="room-host">
          開設者：{{ room.roomAuthor }}
        </div>
        <div class="room-state">{{ roomStateLabel(room.roomState) }}</div>
        <div class="buttons-area">
          <el-button
            v-if="makeButtonVisible(room)"
            @click="onMakeRoomDialogOpen(room.id)"
            class="room__make-button"
            type="primary"
          >
            <div class="button-label">部屋作成</div>
          </el-button>
          <el-button
            v-if="entryButtonVisible(room)"
            @click="onEntryButtonClick(room.id, room.requireEntryPassword)"
            class="room__entry-button"
          >
            <div class="button-label">対局</div>
            <div class="button-badge">
              <img v-if="room.requireEntryPassword" src="@/assets/key.svg" />
            </div>
          </el-button>
          <el-button
            v-if="viewButtonVisible(room)"
            @click="onViewButtonClick()"
            class="room__view-button"
          >
            <div class="button-label">観戦</div>
          </el-button>
        </div>
      </div>
    </div>

    <!-- 各種ダイアログ -->
    <!-- 部屋作成ダイアログ -->
    <el-dialog
      :visible.sync="makeRoomDialogVisible"
      id="make-room-dialog"
      title="部屋作成"
      width="784px"
    >
      <form-wizard
        @on-complete="onMakeRoomWizardComplete"
        color="#078080"
        title=""
        subtitle=""
      >
        <tab-content title="部屋のパスワードなどの設定">
          <el-form :model="makeRoomDialogFormData">
            <el-form-item>
              <el-input
                v-model="makeRoomDialogFormData.roomName"
                class="room-name-input"
                placeholder="部屋の名前(20文字以内)"
                maxlength="20"
                show-word-limit
              />
            </el-form-item>
            <el-form-item>
              あなたは
              <el-radio
                v-model="makeRoomDialogFormData.firstPlayer"
                :label="true"
                >先攻(黒)</el-radio
              >
              <el-radio
                v-model="makeRoomDialogFormData.firstPlayer"
                :label="false"
                >後攻(白)</el-radio
              >
            </el-form-item>
            <el-form-item>
              <el-checkbox v-model="makeRoomDialogFormData.requireEntryPassword"
                >対戦者の入室にパスワードを要求する。</el-checkbox
              >
            </el-form-item>
            <el-form-item>
              <div>
                <el-input
                  v-model="makeRoomDialogFormData.entryPassword"
                  :disabled="!makeRoomDialogFormData.requireEntryPassword"
                  class="entry-password-input"
                  placeholder="パスワードを入力してください(20文字以内)"
                  maxlength="20"
                  show-password
                  show-word-limit
                ></el-input>
              </div>
            </el-form-item>
            <el-form-item>
              <el-checkbox v-model="makeRoomDialogFormData.canView"
                >観戦を許可する。</el-checkbox
              >
            </el-form-item>
          </el-form>
        </tab-content>
        <tab-content title="ステージ設定">
          <div class="stage-select">
            <el-radio
              v-for="stageNumber in Object.keys(
                makeRoomDialogFormData.stageData
              ).length"
              v-model="makeRoomDialogFormData.stageName"
              :key="stageNumber"
              :label="`stage${stageNumber}`"
              border
              class="stage-select-radio"
            >
              <reversi-board
                :board-width="200"
                :initial-board-status="
                  makeRoomDialogFormData.stageData[`stage${stageNumber}`]
                "
                :is-read-only="true"
              ></reversi-board>
            </el-radio>
          </div>
        </tab-content>
      </form-wizard>
    </el-dialog>
    <!-- 対局前確認ダイアログ -->
    <el-dialog
      :visible.sync="battleConfirmationDialogVisible"
      id="battle-confirmation-dialog"
      title="対局前確認"
      width="440px"
    >
      <div class="main-message">
        <span class="room-author">{{
          battleConfirmationDialogData.roomAuthor
        }}</span
        >さんとの対局を開始します。
      </div>
      <div class="who-is-first">
        あなたは<span class="who-is-first-span">{{
          battleConfirmationDialogData.firstPlayer ? "後攻" : "先攻"
        }}</span
        >です。
      </div>
      <div class="stage-image-label">使用ステージ</div>
      <div class="stage-image">
        <reversi-board
          :board-width="400"
          :initial-board-status="
            battleConfirmationDialogData.initialBoardStatus
          "
          :is-read-only="true"
        ></reversi-board>
      </div>
      <span slot="footer" class="battle-confirmation-dialog__footer">
        <el-button
          type="secondary"
          @click="battleConfirmationDialogVisible = false"
          >キャンセル</el-button
        >
        <el-button type="primary" @click="battleConfirmationDialogOnStart"
          >対局開始</el-button
        >
      </span>
    </el-dialog>
    <!-- 対局用パスワード入力ダイアログ -->
    <el-dialog
      :visible.sync="passwordToEntryDialogVisible"
      id="pass-to-entry-dialog"
      title="対局用パスワード入力"
    >
      <el-form>
        <el-form-item>
          <el-input
            v-model="passwordToEntryDialogFormData.password"
            type="password"
            autocomplete="off"
            maxlength="20"
            show-password
          ></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="password-to-entry-dialog__footer">
        <el-button
          type="secondary"
          @click="passwordToEntryDialogVisible = false"
          >キャンセル</el-button
        >
        <el-button type="primary" @click="onPasswordToEntryDialogOk"
          >OK</el-button
        >
      </span>
    </el-dialog>
  </div>
</template>

<script>
import ReversiBoard from "@/components/ReversiBoard.vue";
export default {
  components: { ReversiBoard },
  computed: {
    currentPage: {
      get() {
        return this.$store.state.currentPage;
      },
      set(newValue) {
        this.$store.state.currentPage = newValue;
      },
    },
    myNickname: {
      get() {
        return this.$store.state.myNickname;
      },
    },
    rooms: {
      cache: false,
      get() {
        return this.$store.state.rooms;
      },
      set(newValue) {
        this.rooms.splice(0, this.rooms.length);
        newValue.forEach((item) => {
          this.rooms.push(item);
        });
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
    gameData: {
      get() {
        return this.$store.state.gameData;
      },
      set(newValue) {
        this.$store.state.gameData = newValue;
      },
    },
  },
  created() {
    // if not accessed from "nickname" page.
    if (this.currentPage !== "nickname") {
      // redirect to top page.
      this.$router.push("/");
      return;
    }

    // create a WebSocket instance.
    if (this.socket === null) {
      this.initializeWebSocket();
    } else {
      console.log("else");
      this.reloadRooms();
    }

    window.addEventListener("beforeunload", this.closeSocket);

    this.currentPage = "room-list";
  },
  data() {
    return {
      battleConfirmationDialogVisible: false,
      battleConfirmationDialogData: {
        initialBoardStatus: [],
        roomAuthor: "",
        firstPlayer: true,
      },
      makeRoomDialogVisible: false,
      makeRoomDialogFormData: {
        entryPassword: "",
        canView: true,
        currentPlayer: true,
        firstPlayer: true,
        requireEntryPassword: false,
        id: -1, // room id
        roomName: "",
        stageData: {
          stage1: [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 1, 0, 0, 0],
            [0, 0, 0, 1, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
          ],
          stage2: [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0],
            [0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          ],
          stage3: [
            [3, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 3],
            [3, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 3],
            [3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3],
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0],
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3],
            [3, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 3],
            [3, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 3],
          ],
          stage4: [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 2, 1, 0, 0],
            [0, 0, 1, 2, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
          ],
        },
        stageName: "stage1",
      },
      passwordToEntryDialogFormData: {
        password: "",
        id: -1, // room id
      },
      passwordToEntryDialogVisible: false,
      // passwordToViewDialogVisible: false,
      socket: null,
    };
  },
  destroyed() {
    window.removeEventListener("beforeunload", this.closeSocket);
  },
  methods: {
    battleConfirmationDialogOnStart() {
      this.battleConfirmationDialogVisible = false;
      let boardStatus = [];
      this.battleConfirmationDialogData.initialBoardStatus.forEach(
        (boardRow) => {
          boardStatus.push(boardRow.slice());
        }
      );
      const gameData = {
        initialBoardStatus: boardStatus,
        boardSize: {
          width: this.battleConfirmationDialogData.initialBoardStatus[0].length,
          height: this.battleConfirmationDialogData.initialBoardStatus.length,
        },
        isJustViewing: false,
        myNickname: this.myNickname,
        opponntNickname: this.battleConfirmationDialogData.roomAuthor,
        roomId: this.gameData.roomId,
      };
      this.gameData = gameData;
      this.$router.push({ path: "/game" });
    },
    closeSocket() {
      if (this.socket) {
        this.socket.close();
      }
    },
    entryButtonVisible(room) {
      return room.roomState === "standby";
    },
    initializeWebSocket() {
      this.socket = new WebSocket(this.serverUrl);
      this.socket.onopen = (e) => {
        console.log("onopen - begin");
        console.log(e);
        this.reloadRooms();
        console.log("onopen - fin");
      };
      // if receive some data from API Gateway (Lambda)
      this.socket.onmessage = (e) => {
        console.log("onmessage");
        console.log(e);
        const parsedData = JSON.parse(e.data);
        console.log(parsedData);

        // check data type
        if (parsedData.dataType === "getRooms") {
          console.log("get rooms data.");
          const getRoomsData = parsedData.data;
          this.$store.commit("updateLocalRoomsData", getRoomsData);
        } else if (parsedData.dataType === "checkedEntryPassword") {
          console.log("checked entry password.");
          const checkResult = parsedData.data.result;
          console.log(checkResult);
          switch (checkResult) {
            case "OK":
              // show battleConfirmationDialog.
              this.battleConfirmationDialogData.firstPlayer =
                parsedData.data.firstPlayer;
              console.log("firstPlayer:");
              console.log(parsedData.data.firstPlayer);
              this.battleConfirmationDialogData.initialBoardStatus =
                parsedData.data.currentBoard;
              this.battleConfirmationDialogData.roomAuthor =
                parsedData.data.roomAuthor;
              this.battleConfirmationDialogVisible = true;
              break;
            case "NG":
              // TODO: show NG password messagebox.
              break;
            default:
              throw "invalid value @ checkResult";
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
    makeButtonVisible(room) {
      return room.roomState === "vacancy";
    },
    onEntryButtonClick(roomId, isPasswordRequired) {
      if (isPasswordRequired) {
        this.onPasswordToEntryDialogOpen(roomId);
      } else {
        this.gameData.roomId = roomId;
        this.battleConfirmationDialogVisible = true;
      }
    },
    onMakeRoomDialogOpen(roomId) {
      console.log("onMakeRoomDialogOpen start.");
      this.makeRoomDialogVisible = true;
      this.makeRoomDialogFormData.id = roomId;
      this.gameData.roomId = roomId;
      console.log("room id : " + this.makeRoomDialogFormData.id);
      this.socket.send(
        JSON.stringify({
          action: "updateRoom",
          data: {
            boardLogs: [],
            canView: this.makeRoomDialogFormData.canView,
            currentBoard: [],
            currentPlayer: this.makeRoomDialogFormData.currentPlayer,
            entryPassword: this.makeRoomDialogFormData.entryPassword,
            firstPlayer: true,
            id: this.makeRoomDialogFormData.id,
            opponentId: "",
            opponentName: "",
            requireEntryPassword:
              this.makeRoomDialogFormData.requireEntryPassword,
            roomAuthor: this.myNickname,
            roomAuthorId: this.token,
            roomName: this.makeRoomDialogFormData.roomName,
            roomState: "inPreparation",
            thinkingCounter: 0,
            token: this.token,
          },
        })
      );
    },
    onMakeRoomWizardComplete() {
      console.log("make room wizard completed.");
      let board = [];
      this.makeRoomDialogFormData.stageData[
        this.makeRoomDialogFormData.stageName
      ].forEach((row) => {
        board.push(row.slice());
      });
      const dataToSend = {
        // ルートキー（request.body.actionの場合）
        action: "updateRoom",
        // サーバに伝えるデータの中身の例
        data: {
          boardLogs: [],
          canView: this.makeRoomDialogFormData.canView,
          currentBoard: board,
          currentPlayer: this.makeRoomDialogFormData.currentPlayer,
          entryPassword: this.makeRoomDialogFormData.entryPassword,
          firstPlayer: this.makeRoomDialogFormData.firstPlayer,
          id: this.makeRoomDialogFormData.id,
          opponentId: "",
          opponentName: "",
          requireEntryPassword:
            this.makeRoomDialogFormData.requireEntryPassword,
          roomAuthor: this.myNickname,
          roomAuthorId: this.token,
          roomName: this.makeRoomDialogFormData.roomName,
          roomState: "standby",
          thinkingCounter: 0,
          token: this.token,
        },
      };
      console.log(dataToSend);
      this.socket.send(JSON.stringify(dataToSend));
      const gameData = {
        initialBoardStatus: board,
        boardSize: {
          width: board[0].length,
          height: board.length,
        },
        isJustViewing: false,
        myNickname: this.myNickname,
        opponntNickname: "",
        roomId: this.gameData.roomId,
      };
      this.gameData = gameData;
      this.makeRoomDialogVisible = false;
      this.$router.push({ path: "/game" });
    },
    onPasswordToEntryDialogOk() {
      this.socket.send(
        JSON.stringify({
          action: "checkEntryPassword",
          data: {
            id: this.passwordToEntryDialogFormData.id,
            password: this.passwordToEntryDialogFormData.password,
            token: this.token,
          },
        })
      );
      console.log("password: " + this.passwordToEntryDialogFormData.password);
      this.passwordToEntryDialogVisible = false;
    },
    onPasswordToEntryDialogOpen(roomId) {
      console.log("onPasswordToEntryDialogOpen start.");
      this.passwordToEntryDialogVisible = true;
      this.passwordToEntryDialogFormData.id = roomId;
      this.gameData.roomId = roomId;
      console.log("room id : " + this.passwordToEntryDialogFormData.id);
    },
    // onViewButtonClick(isPasswordRequired) {
    onViewButtonClick() {
      // if (isPasswordRequired) {
      //   this.passwordToViewDialogVisible = true;
      // } else {
      this.$router.push({ path: "/game" });
      // }
    },
    reloadRooms() {
      this.socket.send(
        JSON.stringify({
          action: "getRooms",
          data: {
            token: this.token,
          },
        })
      );
    },
    roomStateLabel(roomState) {
      let ret = "";

      switch (roomState) {
        case "vacancy":
          ret = "空室";
          break;
        case "inPreparation":
          ret = "準備中";
          break;
        case "standby":
          ret = "待機中";
          break;
        case "inGame":
          ret = "使用中";
          break;
        default:
          ret = "エラー";
          break;
      }

      return ret;
    },
    roomAuthorVisible(roomState) {
      return roomState !== "vacancy";
    },
    roomTitleVisible(roomState) {
      return roomState === "standby" || roomState === "inGame";
    },
    viewButtonVisible(room) {
      return (
        room.canView &&
        (room.roomState === "standby" || room.roomState === "inGame")
      );
    },
  },
  name: "RoomList",
};
</script>

<style lang="scss" scoped>
.rooms {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: flex-start;
  align-items: flex-start;
  align-content: flex-start;
}
.room {
  $roomPadding: 8px;
  position: relative;
  width: 350px;
  height: 200px;
  margin: $roomPadding;
  padding: $roomPadding;
  // border-width: 8px;
  // border-style: solid;

  .buttons-area {
    position: absolute;
    right: $roomPadding;
    bottom: $roomPadding;
  }

  &__make-button,
  &__entry-button,
  &__view-button {
    position: relative;

    .button-badge {
      position: absolute;
      right: -7px;
      top: -4px;
    }

    .button-badge,
    img {
      width: 20px;
      height: 20px;
    }
  }

  &.vacancy {
    $bg: #999999ff;
    background-color: rgba($bg, 0.3);
    // border-color: $bg;
  }
  &.in-preparation {
    $bg: #f1c232ff;
    background-color: rgba($bg, 0.3);
    // border-color: $bg;
  }
  &.standby {
    $bg: #e69138ff;
    background-color: rgba($bg, 0.3);
    // border-color: $bg;
  }
  &.in-game {
    $bg: #a64d79ff;
    background-color: rgba($bg, 0.3);
    // border-color: $bg;
  }
}

.room-number {
  font-size: 32px;
}

.room-state {
  font-size: 56px;
}

.el-dialog {
  min-width: 442px;
}

#make-room-dialog {
  .room-name-input {
    width: 400px;
  }
  .entry-password-input {
    width: 330px;
  }
  .entry-password-input {
    margin-left: 22px;
  }
  .allow-view-checkbox {
    margin-left: 22px;
  }

  .stage-select {
    .stage-select-radio {
      height: 240px;
    }
  }
}

#battle-confirmation-dialog {
  .room-author,
  .who-is-first-span {
    font-weight: bold;
    font-size: 24px;
  }
}
</style>

<style lang="scss">
#make-room-dialog {
  .el-dialog__body,
  .vue-form-wizard .wizard-header {
    padding-top: 0;
  }
}
</style>
