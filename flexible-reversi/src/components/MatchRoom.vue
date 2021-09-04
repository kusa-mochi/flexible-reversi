<template>
  <div class="match-room">
    <div class="room-image-container">
      <img
        v-if="state == 'vacancy'"
        :style="roomSizeStyle"
        class="room-image"
        src="@/assets/room_vacancy.svg"
      />
      <img
        v-else-if="state == 'inPreparation'"
        :style="roomSizeStyle"
        class="room-image"
        src="@/assets/room_inPreparation.svg"
      />
      <img
        v-else-if="state == 'standby'"
        :style="roomSizeStyle"
        class="room-image"
        src="@/assets/room_standby.svg"
      />
      <img
        v-else-if="state == 'inGame'"
        :style="roomSizeStyle"
        class="room-image"
        src="@/assets/room_inGame.svg"
      />
      <img
        v-else-if="state == 'error'"
        :style="roomSizeStyle"
        class="room-image"
        src="@/assets/room_error.svg"
      />
      <img v-else src="@/assets/room_vacancy.svg" />
    </div>
    <div class="room-id">No.{{ roomId }}</div>
    <div v-if="authorName" class="room-author-name">{{ authorName }}&nbsp;の部屋</div>
    <div v-if="!authorName" class="room-author-name">空室</div>
    <div class="room-title">{{ title }}</div>
  </div>
</template>

<script>
export default {
  computed: {
    roomSizeStyle: {
      get() {
        return {
          "--room-width": this.width,
        };
      },
    },
  },
  name: "MatchRoom",
  props: {
    authorName: {
      type: String,
      required: false,
      default: "",
    },
    roomId: {
      type: Number,
      required: false,
      default: 0,
    },
    state: {
      type: String,
      required: false,
      default: "vacancy",
    },
    title: {
      type: String,
      required: false,
      default: "",
    },
    width: {
      type: String,
      required: false,
      default: "200px",
    },
  },
};
</script>

<style lang="scss" scoped>
.match-room {
  position: relative;

  .room-id {
    position: absolute;
    top: 0;
    left: 0;
    text-align: left;
    font-family: "Bungee Inline", Roboto, cursive;
    font-size: 28px;
  }

  .room-author-name,
  .room-title {
    position: absolute;
    top: 0;
    left: 0;
    text-align: center;
  }

  .room-author-name {
    background-color: rgba(255, 255, 255, 0.8);
    padding: 4px;
    left: 15%;
    top: 24%;
    width: 200px;
  }

  .room-title {
    width: 200px;
    top: 3%;
    left: 50%;
  }

  .room-image {
    width: var(--room-width);
  }
}
</style>
