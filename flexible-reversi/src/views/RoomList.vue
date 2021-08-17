<template>
  <div class="room-list">
    <router-link to="/">Top</router-link>
    <router-link to="/game">Game</router-link>
    <div>ようこそ{{ user.name }}さん</div>
    <div class="rooms">
      <div
        v-for="(room, index) in rooms"
        :key="index"
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
            @click="makeRoomDialogVisible = true"
            class="room__make-button"
            type="primary"
          >
            <div class="button-label">部屋作成</div>
          </el-button>
          <el-button
            v-if="entryButtonVisible(room)"
            @click="onEntryButtonClick(room.requireEntryPassword)"
            class="room__entry-button"
          >
            <div class="button-label">対局</div>
            <div class="button-badge">
              <img v-if="room.requireEntryPassword" src="@/assets/key.svg" />
            </div>
          </el-button>
          <el-button
            v-if="viewButtonVisible(room)"
            @click="onViewButtonClick(room.requireViewPassword)"
            class="room__view-button"
          >
            <div class="button-label">観戦</div>
            <div class="button-badge">
              <img v-if="room.requireViewPassword" src="@/assets/key.svg" />
            </div>
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
      width="584px"
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
                v-model="makeRoomDialogFormData.firstOrSecond"
                label="first"
                >先攻(黒)</el-radio
              >
              <el-radio
                v-model="makeRoomDialogFormData.firstOrSecond"
                label="second"
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
              <div>
                <el-input
                  v-model="makeRoomDialogFormData.entryPassword2"
                  :disabled="!makeRoomDialogFormData.requireEntryPassword"
                  class="entry-password-input"
                  placeholder="もう一度同じパスワードを入力してください"
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
            <el-form-item>
              <el-checkbox
                v-model="makeRoomDialogFormData.requireViewPassword"
                :disabled="!makeRoomDialogFormData.canView"
                class="allow-view-checkbox"
                >観戦者の入室にパスワードを要求する。</el-checkbox
              >
            </el-form-item>
            <el-form-item>
              <div>
                <el-input
                  v-model="makeRoomDialogFormData.viewPassword"
                  :disabled="!makeRoomDialogFormData.requireViewPassword"
                  class="view-password-input"
                  placeholder="パスワードを入力してください(20文字以内)"
                  maxlength="20"
                  show-password
                ></el-input>
              </div>
              <div>
                <el-input
                  v-model="makeRoomDialogFormData.viewPassword2"
                  :disabled="!makeRoomDialogFormData.requireViewPassword"
                  class="view-password-input"
                  placeholder="もう一度同じパスワードを入力してください"
                  maxlength="20"
                  show-password
                ></el-input>
              </div>
            </el-form-item>
          </el-form>
        </tab-content>
        <tab-content title="ステージ設定">
          <div class="stage-select">
            <el-radio
              v-for="stageNumber in [1, 2]"
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
    <el-dialog :visible.sync="battleConfirmationDialogVisible" title="対局確認">
      <span slot="footer" class="battle-confirmation-dialog__footer">
        <el-button
          type="secondary"
          @click="battleConfirmationDialogVisible = false"
          >Cancel</el-button
        >
        <el-button type="primary" @click="battleConfirmationDialogOnStart"
          >対局開始</el-button
        >
      </span>
    </el-dialog>
    <!-- 対局用パスワード入力ダイアログ -->
    <el-dialog
      :visible.sync="passwordToEntryDialogVisible"
      title="対局用パスワード入力"
    >
      <span slot="footer" class="password-to-entry-dialog__footer">
        <el-button
          type="secondary"
          @click="passwordToEntryDialogVisible = false"
          >Cancel</el-button
        >
        <el-button type="primary" @click="passwordToEntryDialogVisible = false"
          >OK</el-button
        >
      </span>
    </el-dialog>
    <!-- 観戦用パスワード入力ダイアログ -->
    <el-dialog
      :visible.sync="passwordToViewDialogVisible"
      title="観戦用パスワード入力"
    >
      <span slot="footer" class="password-to-view-dialog__footer">
        <el-button type="secondary" @click="passwordToViewDialogVisible = false"
          >Cancel</el-button
        >
        <el-button type="primary" @click="passwordToViewDialogVisible = false"
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
    socket: {
      get() {
        return this.$store.state.socket;
      },
      set(newValue) {
        this.$store.state.socket = newValue;
      },
    },
  },
  created() {
    // if not accessed from "nickname" page.
    if (this.currentPage !== "nickname") {
      // redirect to top page.
      this.$router.push("/");
    }

    // create a WebSocket instance.
    if (this.socket === null) {
      this.socket = new WebSocket(this.serverUrl);
      this.socket.onopen = (e) => {
        console.log("onopen - begin");
        console.log(e);
        this.socket.send(
          JSON.stringify({
            action: "getRooms",
          })
        );
        console.log("onopen - fin");
      };
      this.socket.onmessage = (e) => {
        console.log("onmessage");
        // console.log(e.data);
        const parsedData = JSON.parse(e.data);
        // console.log(parsedData);
        // console.log(parsedData.rooms[0].roomState);

        // sort parsedData by id
        parsedData.rooms.sort((roomA, roomB) => {
          if (roomA.id === roomB.id) {
            throw "invalid room id.";
          }
          return roomA.id > roomB.id ? 1 : -1;
        });
        // console.log(parsedData);

        // reset client rooms data.
        this.rooms.splice(0, this.rooms.length);
        parsedData.rooms.forEach((room) => {
          const roomData = {
            roomState: room.roomState,
            roomAuthor: room.roomAuthor,
            id: room.id,
            requireEntryPassword: room.requireEntryPassword,
            requireViewPassword: room.requireViewPassword,
            roomName: room.roomName,
            canView: room.canView,
          };
          console.log(roomData);
          this.rooms.push(roomData);
        });
        this.rooms.splice();
      };
      this.socket.onclose = (e) => {
        console.log("onclose");
        console.log(e);
      };
      this.socket.onerror = (e) => {
        console.log("onerror");
        console.log(e);
      };
    } else {
      console.log("else");
      this.socket.send(
        JSON.stringify({
          action: "getRooms",
        })
      );
    }

    this.currentPage = "room-list";
  },
  data() {
    return {
      battleConfirmationDialogVisible: false,
      makeRoomDialogVisible: false,
      makeRoomDialogFormData: {
        entryPassword: "",
        entryPassword2: "",
        canView: true,
        currentPlayer: true,
        requireEntryPassword: false,
        requireViewPassword: false,
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
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
            [0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0],
            [0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          ],
        },
        stageName: "stage1",
        viewPassword: "",
        viewPassword2: "",
      },
      passwordToEntryDialogVisible: false,
      passwordToViewDialogVisible: false,
    };
  },
  destroyed() {
    if (this.socket) {
      // TODO: request to remove connection id of websocket.
    }
  },
  methods: {
    // beforeCloseMakeRoomDialog(done) {
    //   this.$confirm("次の内容で部屋を作成します。よろしいですか？")
    //     .then((_) => done())
    //     .catch((_) => {});
    // },
    battleConfirmationDialogOnStart() {
      this.battleConfirmationDialogVisible = false;
      this.$router.push({ path: "/game" });
    },
    entryButtonVisible(room) {
      return room.roomState === "standby";
    },
    makeButtonVisible(room) {
      return room.roomState === "vacancy";
    },
    // if ok button is pushed on make room dialog.
    makeRoomDialogOnOk() {
      this.makeRoomDialogVisible = false;
      this.$router.push({ path: "/game" });
    },
    onEntryButtonClick(isPasswordRequired) {
      if (isPasswordRequired) {
        this.passwordToEntryDialogVisible = true;
      } else {
        this.battleConfirmationDialogVisible = true;
      }
    },
    onMakeRoomWizardComplete() {},
    onViewButtonClick(isPasswordRequired) {
      if (isPasswordRequired) {
        this.passwordToViewDialogVisible = true;
      } else {
        this.$router.push({ path: "/game" });
      }
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
  props: {
    user: {
      type: Object,
      required: true,
      default: null,
    },
  },
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
  .entry-password-input,
  .view-password-input {
    width: 330px;
  }
  .entry-password-input {
    margin-left: 22px;
  }
  .view-password-input {
    margin-left: 44px;
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
</style>

<style lang="scss">
#make-room-dialog {
  .el-dialog__body,
  .vue-form-wizard .wizard-header {
    padding-top: 0;
  }
}
</style>
