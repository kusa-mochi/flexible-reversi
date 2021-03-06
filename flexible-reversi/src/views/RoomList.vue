<template>
  <div class="room-list">
    <reversi-board
      :board-width="2000"
      :board-status="backgroundBoardStatus"
      :is-read-only="true"
      class="room-list__background"
      z-index="0"
    ></reversi-board>
    <div class="room-list__header">
      <el-button
        @click="onGoToTopButtonClick"
        class="go-to-top-button"
        icon="el-icon-s-home"
        >トップに戻る</el-button
      >
      <div class="welcome-message">
        ようこそ&nbsp;<span class="my-nickname">{{ myNickname }}</span
        >&nbsp;さん
      </div>
    </div>
    <div class="rooms">
      <div v-for="room in rooms" :key="room.roomCounter" class="room">
        <match-room
          :author-name="room.roomAuthor"
          :room-id="room.id"
          :state="room.roomState"
          :title="room.roomName"
          width="330px"
        ></match-room>
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
          <!-- <el-button
            v-if="viewButtonVisible(room)"
            @click="onViewButtonClick()"
            class="room__view-button"
          >
            <div class="button-label">観戦</div>
          </el-button> -->
        </div>
      </div>
    </div>

    <!-- 各種ダイアログ -->
    <!-- 部屋作成ダイアログ -->
    <el-dialog
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :show-close="false"
      :visible.sync="makeRoomDialogVisible"
      id="make-room-dialog"
      class="make-room-dialog"
      title="部屋作成"
      width="100%"
    >
      <div class="make-room-dialog__content">
        <div class="make-room-dialog__body">
          <form-wizard
            @on-complete="onMakeRoomWizardComplete"
            color="#078080"
            title=""
            subtitle=""
          >
            <tab-content title="部屋の名前などの設定">
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
                  <el-checkbox
                    v-model="makeRoomDialogFormData.requireEntryPassword"
                    >対戦者の入室にパスワードを要求する。</el-checkbox
                  >
                  <el-input
                    v-model="makeRoomDialogFormData.entryPassword"
                    :disabled="!makeRoomDialogFormData.requireEntryPassword"
                    class="entry-password-input"
                    placeholder="パスワードを入力してください(20文字以内)"
                    maxlength="20"
                    show-password
                    show-word-limit
                  ></el-input>
                </el-form-item>
                <!-- <el-form-item>
              <el-checkbox v-model="makeRoomDialogFormData.canView"
                >観戦を許可する。</el-checkbox
              >
            </el-form-item> -->
              </el-form>
            </tab-content>
            <tab-content title="ステージ設定">
              <div class="stage-select">
                <el-carousel
                  @change="onStageCarouselChanged"
                  :autoplay="false"
                  arrow="always"
                  indicator-position="outside"
                  trigger="click"
                  :type="stageCarouselType"
                  height="256px"
                >
                  <el-carousel-item
                    v-for="stageNumber in Object.keys(
                      makeRoomDialogFormData.stageData
                    ).length"
                    :key="stageNumber"
                  >
                    <div class="stage-item">
                      <el-radio
                        v-model="makeRoomDialogFormData.stageName"
                        :label="`stage${stageNumber}`"
                        border
                        class="stage-select-radio"
                      >
                        <reversi-board
                          :board-width="200"
                          :board-status="
                            makeRoomDialogFormData.stageData[
                              `stage${stageNumber}`
                            ]
                          "
                          :is-read-only="true"
                        ></reversi-board>
                      </el-radio>
                    </div>
                  </el-carousel-item>
                </el-carousel>
              </div>
            </tab-content>
          </form-wizard>
        </div>
        <div class="make-room-dialog__footer">
          <div class="footer-left">
            <el-button @click="onMakeRoomDialogCancel" type="primary"
              >キャンセル</el-button
            >
          </div>
        </div>
      </div>
    </el-dialog>
    <!-- 対局前確認ダイアログ -->
    <el-dialog
      :visible.sync="battleConfirmationDialogVisible"
      id="battle-confirmation-dialog"
      class="battle-confirmation-dialog"
      title="対局前確認"
      :width="battleConfirmationDialogWidth"
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
          :board-width="boardWidthOnBattleConfirmationDialog"
          :board-status="battleConfirmationDialogData.initialBoardStatus"
          :is-read-only="true"
        ></reversi-board>
      </div>
      <span slot="footer" class="battle-confirmation-dialog__footer">
        <el-button type="secondary" @click="battleConfirmationDialogOnCancel"
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
      class="pass-to-entry-dialog"
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
        <el-button type="secondary" @click="onPasswordToEntryDialogCancel"
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
import MatchRoom from "@/components/MatchRoom.vue";
import ReversiBoard from "@/components/ReversiBoard.vue";

export default {
  components: {
    MatchRoom,
    ReversiBoard,
  },
  computed: {
    backgroundBoardStatus: {
      get() {
        return this.$store.state.backgroundBoardStatus;
      },
    },
    battleConfirmationDialogWidth: {
      get() {
        if (this.windowWidth < 360) {
          return `${this.windowWidth - 8}px`;
        } else if (this.windowWidth < 448) {
          return `${this.windowWidth - 16}px`;
        } else {
          return "448px";
        }
      },
    },
    boardWidthOnBattleConfirmationDialog: {
      get() {
        if (this.windowWidth < 360) {
          return this.windowWidth - 48;
        } else if (this.windowWidth < 448) {
          return this.windowWidth - 56;
        } else {
          return 398;
        }
      },
    },
    stageCarouselType: {
      get() {
        if (this.windowWidth > 556) {
          return "card";
        } else {
          return "";
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
    // if a nickname is not defined yet
    if (!this.myNickname) {
      // redirect to the top page.
      this.$router.push("/");
      return;
    }

    this.loading = this.$loading({
      lock: true,
      text: "読込中",
      spinner: "el-icon-loading",
      background: "rgba(0, 0, 0, 0.7)",
    });

    // create a WebSocket instance.
    if (this.socket === null) {
      this.initializeWebSocket();
    } else {
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
      loading: null,
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
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 1, 2, 1, 0, 0, 0],
            [0, 0, 0, 1, 3, 3, 2, 0, 0, 0],
            [0, 0, 0, 2, 3, 3, 1, 0, 0, 0],
            [0, 0, 0, 1, 2, 1, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          ],
          stage5: [
            [0, 4, 0, 0, 0, 0, 4, 0],
            [4, 4, 0, 0, 0, 0, 4, 4],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 1, 0, 0, 0],
            [0, 0, 0, 1, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [4, 4, 0, 0, 0, 0, 4, 4],
            [0, 4, 0, 0, 0, 0, 4, 0],
          ],
          stage6: [
            [2, 0, 0, 0, 0, 0, 0, 1],
            [0, 2, 0, 0, 0, 0, 1, 0],
            [0, 0, 2, 0, 0, 1, 0, 0],
            [0, 0, 0, 2, 1, 0, 0, 0],
            [0, 0, 0, 1, 2, 0, 0, 0],
            [0, 0, 1, 0, 0, 2, 0, 0],
            [0, 1, 0, 0, 0, 0, 2, 0],
            [1, 0, 0, 0, 0, 0, 0, 2],
          ],
          stage7: [
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
      windowWidth: 800,
    };
  },
  destroyed() {
    window.removeEventListener("beforeunload", this.closeSocket);
    window.removeEventListener("resize", this.onWindowResize);
  },
  methods: {
    battleConfirmationDialogOnCancel() {
      this.$store.dispatch("playSound", "cancel-button.mp3");
      this.$store.commit("resetGameData");
      this.battleConfirmationDialogVisible = false;
    },
    battleConfirmationDialogOnStart() {
      this.$store.dispatch("playSound", "ok-button.mp3");
      this.battleConfirmationDialogVisible = false;
      let boardStatus = [];
      this.battleConfirmationDialogData.initialBoardStatus.forEach(
        (boardRow) => {
          boardStatus.push(boardRow.slice());
        }
      );
      const gameData = {
        boardStatus: boardStatus,
        boardSize: {
          width: this.battleConfirmationDialogData.initialBoardStatus[0].length,
          height: this.battleConfirmationDialogData.initialBoardStatus.length,
        },
        isJustViewing: false,
        myNickname: this.myNickname,
        opponntNickname: this.battleConfirmationDialogData.roomAuthor,
        roomId: this.gameData.roomId,
        // if firstPlayer is true, the room author(opponent) is a first player.
        myColor: this.battleConfirmationDialogData.firstPlayer ? 2 : 1,
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
        console.log("onopen");
        console.log(e);
        this.reloadRooms();
      };
      // if receive some data from API Gateway (Lambda)
      this.socket.onmessage = (e) => {
        console.log("onmessage");
        console.log(e);
        const parsedData = JSON.parse(e.data);
        console.log(parsedData);

        // check data type
        if (parsedData.dataType === "getRooms") {
          console.log("received getRooms.");
          const getRoomsData = parsedData.data;
          this.$store.commit("updateLocalRoomsData", getRoomsData);
          this.loading.close();
        } else if (parsedData.dataType === "checkedEntryPassword") {
          console.log("received checkedEntryPassword.");
          const checkResult = parsedData.data.result;
          switch (checkResult) {
            case "OK":
              this.$store.dispatch("playSound", "ok-button.mp3");
              // show battleConfirmationDialog.
              this.battleConfirmationDialogData.firstPlayer =
                parsedData.data.firstPlayer;
              this.battleConfirmationDialogData.initialBoardStatus =
                parsedData.data.currentBoard;
              this.battleConfirmationDialogData.roomAuthor =
                parsedData.data.roomAuthor;
              this.battleConfirmationDialogVisible = true;
              break;
            case "NG":
              this.$store.dispatch("playSound", "info.mp3");
              this.$notify({
                title: "Error",
                message: "パスワードが違います。",
                type: "error",
              });
              break;
            default:
              throw "invalid value @ checkResult";
          }
        }
      };
      this.socket.onclose = (e) => {
        console.log("onclose");
        console.log(e);
        // reconnect
        this.initializeWebSocket();
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
        this.onOpenEntry(roomId);
      }
    },
    onGoToTopButtonClick() {
      this.$store.dispatch("playSound", "cancel-button.mp3");
      this.$router.push({ path: "/" });
    },
    onMakeRoomDialogCancel() {
      console.log("onMakeRoomDialogCancel");
      this.$store.dispatch("playSound", "cancel-button.mp3");
      this.$store.commit("resetGameData");
      this.makeRoomDialogVisible = false;
      this.socket.send(
        JSON.stringify({
          action: "exitRoom",
          data: {
            token: this.token,
            roomId: this.makeRoomDialogFormData.id,
          },
        })
      );
    },
    onMakeRoomDialogOpen(roomId) {
      console.log("onMakeRoomDialogOpen");
      this.$store.dispatch("playSound", "ok-button.mp3");
      this.makeRoomDialogVisible = true;
      this.makeRoomDialogFormData.id = roomId;
      this.gameData.roomId = roomId;
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
      console.log("onMakeRoomWizardComplete");
      let board = [];
      this.makeRoomDialogFormData.stageData[
        this.makeRoomDialogFormData.stageName
      ].forEach((row) => {
        board.push(row.slice());
      });
      const dataToSend = {
        // root key
        action: "updateRoom",
        // data to the lambda
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
        boardStatus: board,
        boardSize: {
          width: board[0].length,
          height: board.length,
        },
        isJustViewing: false,
        myNickname: this.myNickname,
        opponntNickname: "",
        roomId: this.gameData.roomId,
        myColor: this.makeRoomDialogFormData.firstPlayer ? 1 : 2,
      };
      this.gameData = gameData;
      this.makeRoomDialogVisible = false;
      this.$router.push({ path: "/game" });
    },
    onOpenEntry(roomId) {
      this.gameData.roomId = roomId;
      this.socket.send(
        JSON.stringify({
          action: "checkEntryPassword",
          data: {
            id: roomId,
            password: "",
            token: this.token,
          },
        })
      );
    },
    onPasswordToEntryDialogCancel() {
      this.$store.dispatch("playSound", "cancel-button.mp3");
      this.$store.commit("resetGameData");
      this.passwordToEntryDialogVisible = false;
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
      this.passwordToEntryDialogVisible = false;
    },
    onPasswordToEntryDialogOpen(roomId) {
      console.log("onPasswordToEntryDialogOpen");
      this.$store.dispatch("playSound", "ok-button.mp3");
      this.passwordToEntryDialogVisible = true;
      this.passwordToEntryDialogFormData.id = roomId;
      this.gameData.roomId = roomId;
    },
    onStageCarouselChanged(newIndex, _) {
      this.$store.dispatch("playSound", "stage-select.mp3");
      this.makeRoomDialogFormData.stageName = `stage${newIndex + 1}`;
    },
    onViewButtonClick() {
      this.$router.push({ path: "/game" });
    },
    onWindowResize() {
      this.windowWidth = window.innerWidth;
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
  mounted() {
    this.windowWidth = window.innerWidth;
    window.addEventListener("resize", this.onWindowResize);
  },
  name: "RoomList",
};
</script>

<style lang="scss" scoped>
.room-list {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;

  display: flex;
  flex-direction: column;
}
.room-list__header {
  position: relative;
  width: 100%;
  background-color: rgba(white, 0.95);

  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: flex-start;
  align-items: center;
  align-content: center;
}
.room-list__background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  opacity: 0.4;
}
.go-to-top-button {
  position: relative;
  margin: 8px;
  z-index: 10;
}
.welcome-message {
  position: relative;
  margin: 8px;
  z-index: 10;
}
.my-nickname {
  font-size: 24px;
}
.rooms {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  align-items: flex-start;
  align-content: flex-start;

  flex-grow: 1;

  position: relative;
  overflow-x: hidden;
  overflow-y: scroll;
  width: 100%;
}
.room {
  $roomPadding: 8px;
  position: relative;
  margin: $roomPadding;
  padding: $roomPadding;
  height: 211px;
  background-color: rgba(white, 0.95);

  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: space-between;
  align-items: flex-end;

  .buttons-area {
    position: relative;
    width: 100%;

    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: flex-end;
    align-items: flex-start;
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

.make-room-dialog {
  .make-room-dialog__content {
    width: 100%;

    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    justify-content: flex-start;
    align-items: center;
  }

  .make-room-dialog__body {
    width: 100%;
  }

  .make-room-dialog__footer {
    width: 100%;
    border-top: 1px solid gray;
    padding-top: 20px;

    .footer-left {
      display: flex;
      flex-direction: row;
      flex-wrap: wrap;
      justify-content: flex-start;
      align-items: flex-start;
      align-content: center;
    }
  }

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
    .stage-item {
      position: relative;

      display: flex;
      flex-direction: column;
      flex-wrap: nowrap;
      justify-content: flex-start;
      align-items: center;
    }
    .stage-select-radio {
      background-color: white;
      height: 240px;
    }
  }
}

.battle-confirmation-dialog {
  .who-is-first {
    margin-bottom: 24px;
  }

  .room-author,
  .who-is-first-span {
    font-weight: bold;
    font-size: 24px;
  }
}
</style>

<style lang="scss">
#make-room-dialog {
  .el-dialog {
    max-width: 800px;
  }
  .el-dialog__body,
  .vue-form-wizard .wizard-header {
    padding-top: 0;
  }
  .el-dialog__body {
    padding-bottom: 20px;
  }
  .stage-select {
    .el-radio {
      padding: 8px;
    }
    .el-radio__inner {
      display: none;
    }
    .el-radio.is-bordered {
      transition: opacity 0.3s linear;
      opacity: 0.6;
      &.is-checked {
        border-width: 3px;
        opacity: 1;
      }
    }
    .el-carousel__item {
      &.is-active {
        pointer-events: none;

        .el-radio {
          pointer-events: auto;
        }
      }
    }
  }
}

#battle-confirmation-dialog {
  .el-dialog__body {
    padding: 10px 20px;
  }
}

@media screen and (max-width: 767px) {
  #pass-to-entry-dialog {
    .el-dialog {
      width: 70%;
    }
  }
}

@media screen and (max-width: 480px) {
  #make-room-dialog {
    .el-dialog__header {
      padding: 10px;
    }
    .el-dialog__body {
      padding: 10px;
    }
    .wizard-header {
      padding: 0;
    }
    .wizard-tab-content {
      padding: 30px 0 0 0;
    }
    .wizard-card-footer {
      padding: 20px 0 0 20px;
    }
    .room-name-input {
      width: 100%;
    }
    .entry-password-input {
      width: 94%;
    }
    .el-form-item {
      margin-bottom: 12px;
    }
    .vue-form-wizard {
      padding-bottom: 12px;
    }
    .make-room-dialog__footer {
      padding-top: 12px;
    }
  }

  #pass-to-entry-dialog {
    .el-dialog {
      width: 96%;
    }
  }
}
</style>
