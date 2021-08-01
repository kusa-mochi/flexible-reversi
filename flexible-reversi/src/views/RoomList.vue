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
        <el-button
          v-if="makeButtonVisible(roomState)"
          class="room__make-button"
          type="primary"
        >
          <div class="button-label">部屋作成</div>
        </el-button>
        <el-button
          v-if="entryButtonVisible(roomState)"
          class="room__entry-button"
        >
          <div class="button-label">参加</div>
          <div class="button-badge">
            <img v-if="roomState.lockEntryButton" src="@/assets/key.svg" />
          </div>
        </el-button>
        <el-button
          v-if="viewButtonVisible(roomState)"
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
    this.currentPage = "room-list";
  },
  data() {
    return {
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
    entryButtonVisible(roomState) {
      return roomState.state === "standby";
    },
    makeButtonVisible(roomState) {
      return roomState.state === "vacancy";
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
  width: 350px;
  height: 200px;
  margin: 8px;
  border-width: 8px;
  border-style: solid;
  border-radius: 40px;

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
    border-color: $bg;
  }
  &.in-preparation {
    $bg: #f1c232ff;
    background-color: rgba($bg, 0.3);
    border-color: $bg;
  }
  &.standby {
    $bg: #e69138ff;
    background-color: rgba($bg, 0.3);
    border-color: $bg;
  }
  &.in-game {
    $bg: #a64d79ff;
    background-color: rgba($bg, 0.3);
    border-color: $bg;
  }
}

.room-number {
  font-size: 32px;
}

.room-state {
  font-size: 56px;
}
</style>
