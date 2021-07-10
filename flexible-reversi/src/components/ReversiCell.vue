<template>
  <div @click="$emit('click')" class="reversi-cell">
    <div v-if="state === 0"></div>
    <div v-else-if="state === 1 || state === 2" :class="stoneStyle"></div>
    <div v-else-if="state === 3" class="wall"></div>
  </div>
</template>

<script>
export default {
  computed: {
    stoneStyle: {
      get() {
        return `stone stone--${this.state === 1 ? "black" : "white"}`;
      },
    },
  },
  name: "ReversiCell",
  props: {
    state: {
      type: Number,
      required: false,
      defaut: 1,
    },
  },
};
</script>

<style lang="scss" scoped>
.reversi-cell {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: center;
  align-items: center;

  width: 100%;
  height: 100%;
}

.stone {
  border-radius: 50%;
  border: 2px solid black;
  width: 90%;
  height: 90%;
  transition: background-color 0.3s ease-out;

  &--black {
    background-color: #505050;
  }
  &--white {
    background-color: #f5f5f5;
  }
}

.wall {
  width: 100%;
  height: 100%;
  background-color: #505050;
}
</style>
