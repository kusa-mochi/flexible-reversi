<template>
  <div class="room-list">
    <router-link to="/">Top</router-link>
    <router-link to="/game">Game</router-link>
    <div>ようこそ{{ user.name }}さん</div>
    <div class="rooms">
      <div
        v-for="(roomState, index) in roomStatus"
        :key="index"
        :class="`room ${roomState.state}`"
      >
        <div class="room-number">#&nbsp;{{ index + 1 }}</div>
        <div v-if="roomTitleVisible(roomState.state)" class="room-title">
          {{ roomState.name }}
        </div>
        <div v-if="roomHostnameVisible(roomState.state)" class="room-host">
          開設者：{{ roomState.hostname }}
        </div>
        <div class="room-state">{{ roomStateLabel(roomState.state) }}</div>
        <div class="buttons-area">
          <el-button
            v-if="makeButtonVisible(roomState)"
            @click="makeRoomDialogVisible = true"
            class="room__make-button"
            type="primary"
          >
            <div class="button-label">部屋作成</div>
          </el-button>
          <el-button
            v-if="entryButtonVisible(roomState)"
            @click="onEntryButtonClick(roomState.lockEntryButton)"
            class="room__entry-button"
          >
            <div class="button-label">対局</div>
            <div class="button-badge">
              <img v-if="roomState.lockEntryButton" src="@/assets/key.svg" />
            </div>
          </el-button>
          <el-button
            v-if="viewButtonVisible(roomState)"
            @click="onViewButtonClick(roomState.lockViewButton)"
            class="room__view-button"
          >
            <div class="button-label">観戦</div>
            <div class="button-badge">
              <img v-if="roomState.lockViewButton" src="@/assets/key.svg" />
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
              <el-checkbox v-model="makeRoomDialogFormData.lockEntry"
                >対戦者の入室にパスワードを要求する。</el-checkbox
              >
            </el-form-item>
            <el-form-item>
              <div>
                <el-input
                  v-model="makeRoomDialogFormData.entryPassword"
                  :disabled="!makeRoomDialogFormData.lockEntry"
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
                  :disabled="!makeRoomDialogFormData.lockEntry"
                  class="entry-password-input"
                  placeholder="もう一度同じパスワードを入力してください"
                  maxlength="20"
                  show-password
                  show-word-limit
                ></el-input>
              </div>
            </el-form-item>
            <el-form-item>
              <el-checkbox v-model="makeRoomDialogFormData.viewAvailable"
                >観戦を許可する。</el-checkbox
              >
            </el-form-item>
            <el-form-item>
              <el-checkbox
                v-model="makeRoomDialogFormData.lockView"
                :disabled="!makeRoomDialogFormData.viewAvailable"
                class="allow-view-checkbox"
                >観戦者の入室にパスワードを要求する。</el-checkbox
              >
            </el-form-item>
            <el-form-item>
              <div>
                <el-input
                  v-model="makeRoomDialogFormData.viewPassword"
                  :disabled="!makeRoomDialogFormData.lockView"
                  class="view-password-input"
                  placeholder="パスワードを入力してください(20文字以内)"
                  maxlength="20"
                  show-password
                ></el-input>
              </div>
              <div>
                <el-input
                  v-model="makeRoomDialogFormData.viewPassword2"
                  :disabled="!makeRoomDialogFormData.lockView"
                  class="view-password-input"
                  placeholder="もう一度同じパスワードを入力してください"
                  maxlength="20"
                  show-password
                ></el-input>
              </div>
            </el-form-item>
          </el-form>
        </tab-content>
        <tab-content title="ステージ設定"></tab-content>
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
export default {
  computed: {
    currentPage: {
      get() {
        return this.$store.state.currentPage;
      },
      set(newValue) {
        this.$store.state.currentPage = newValue;
      },
    },
  },
  created() {
    // if not accessed from "nickname" page.
    if (this.currentPage !== "nickname") {
      // redirect to top page.
      this.$router.push("/");
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
        firstOrSecond: "first",
        lockEntry: false,
        lockView: false,
        roomName: "",
        stageData: [],
        viewAvailable: true,
        viewPassword: "",
        viewPassword2: "",
      },
      passwordToEntryDialogVisible: false,
      passwordToViewDialogVisible: false,
      roomStatus: [
        {
          state: "vacancy",
          hostname: "くさもちA",
          lockEntryButton: false,
          lockViewButton: false,
          name: "部屋００１",
          viewingAvailable: false,
        },
        {
          state: "in-preparation",
          hostname: "くさもちB",
          lockEntryButton: false,
          lockViewButton: false,
          name: "部屋００２",
          viewingAvailable: false,
        },
        {
          state: "standby",
          hostname: "くさもちC",
          lockEntryButton: false,
          lockViewButton: false,
          name: "部屋００３",
          viewingAvailable: false,
        },
        {
          state: "standby",
          hostname: "くさもちD",
          lockEntryButton: false,
          lockViewButton: false,
          name: "部屋００４",
          viewingAvailable: true,
        },
        {
          state: "standby",
          hostname: "くさもちE",
          lockEntryButton: true,
          lockViewButton: false,
          name: "部屋００５",
          viewingAvailable: false,
        },
        {
          state: "standby",
          hostname: "くさもちF",
          lockEntryButton: false,
          lockViewButton: true,
          name: "部屋００６",
          viewingAvailable: true,
        },
        {
          state: "standby",
          hostname: "くさもちG",
          lockEntryButton: true,
          lockViewButton: false,
          name: "部屋００７",
          viewingAvailable: true,
        },
        {
          state: "standby",
          hostname: "くさもちH",
          lockEntryButton: true,
          lockViewButton: true,
          name: "部屋００８",
          viewingAvailable: true,
        },
        {
          state: "in-game",
          hostname: "くさもちI",
          lockEntryButton: false,
          lockViewButton: false,
          name: "部屋００８",
          viewingAvailable: false,
        },
        {
          state: "in-game",
          hostname: "くさもちJ",
          lockEntryButton: false,
          lockViewButton: false,
          name: "部屋００８",
          viewingAvailable: true,
        },
        {
          state: "in-game",
          hostname: "くさもちK",
          lockEntryButton: false,
          lockViewButton: true,
          name: "部屋００８",
          viewingAvailable: true,
        },
      ],
    };
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
    entryButtonVisible(roomState) {
      return roomState.state === "standby";
    },
    makeButtonVisible(roomState) {
      return roomState.state === "vacancy";
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
    roomStateLabel(state) {
      let ret = "";

      switch (state) {
        case "vacancy":
          ret = "空室";
          break;
        case "in-preparation":
          ret = "準備中";
          break;
        case "standby":
          ret = "待機中";
          break;
        case "in-game":
          ret = "使用中";
          break;
        default:
          ret = "エラー";
          break;
      }

      return ret;
    },
    roomHostnameVisible(state) {
      return state !== "vacancy";
    },
    roomTitleVisible(state) {
      return state === "standby" || state === "in-game";
    },
    viewButtonVisible(roomState) {
      return (
        roomState.viewingAvailable &&
        (roomState.state === "standby" || roomState.state === "in-game")
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
}
</style>
