<template>
  <div @click="$emit('click')" class="reversi-cell">
    <div v-if="state === 0"></div>
    <div v-else-if="state === 1" class="stone stone--black"></div>
    <div v-else-if="state === 2" class="stone stone--white"></div>
    <div v-else-if="state === 3" class="wall"></div>
    <div v-else-if="state === 4" class="reversible-stone">
      <div class="reversible-stone__black"></div>
      <div class="reversible-stone__white"></div>
      <div class="reversible-stone__border"></div>
    </div>
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

  position: relative;
  width: 100%;
  height: 100%;
}

.stone {
  position: relative;
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
  position: relative;
  width: 100%;
  height: 100%;
  background-color: #505050;
}

.reversible-stone {
  position: relative;
  width: 90%;
  height: 90%;
  transform: rotate(-45deg);

  &__black,
  &__white,
  &__border {
    position: absolute;
    left: 0;
  }

  &__black {
    top: 0;
    width: 100%;
    height: 50%;
    background-color: #505050;
    border: none;
    border-radius:50% 50% 0 0/100% 100% 0 0;
  }
  &__white {
    top: 50%;
    width: 100%;
    height: 50%;
    background-color: #f5f5f5;
    border: none;
    border-radius:0 0 50% 50% /0 0 100% 100%;
  }
  &__border {
    width: 100%;
    height: 100%;
    background-color: transparent;
    border-radius: 50%;
    border: 2px solid black;
  }
}
</style>
