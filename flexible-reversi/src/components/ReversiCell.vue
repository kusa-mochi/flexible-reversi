<template>
  <div @click="$emit('click')" class="reversi-cell">
    <div v-if="state === 0"></div>
    <div v-else-if="state === 1" class="stone stone--black"></div>
    <div v-else-if="state === 2" class="stone stone--white"></div>
    <div v-else-if="state === 3" class="wall"></div>
  </div>
</template>

<script>
export default {
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
