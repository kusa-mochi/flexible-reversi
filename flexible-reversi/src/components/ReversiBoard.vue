<template>
  <div class="reversi-board" :style="boardSizeStyle">
    <div v-for="iCell in this.numCells" :key="iCell" class="reversi-cell">
      {{ iCell }}
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    boardSizeStyle: {
      get() {
          return {
              "--board-width": `${this.boardWidth}px`,
              "--board-height": `${this.boardHeight}px`,
              "--num-columns": this.numColmns,
              "--num-rows": this.numRows
          };
      },
    },
    numCells: {
      get() {
        return this.numColmns * this.numRows;
      },
    },
  },
  name: "ReversiBoard",
  props: {
    boardWidth: {
        type: Number,
        require: false,
        default: 800
    },
    boardHeight: {
        type: Number,
        require: false,
        default: 800
    },
    numColmns: {
      type: Number,
      require: false,
      default: 8,
    },
    numRows: {
      type: Number,
      require: false,
      default: 8,
    }
  },
};
</script>

<style lang="scss" scoped>
.reversi-board {
  display: grid;
  grid-template-columns: repeat(
    var(--num-columns),
    unquote(
      "min(calc(var(--board-width)/var(--num-columns)), calc(var(--board-width)/var(--num-columns)))"
    )
  );
  grid-template-rows: repeat(
    var(--num-rows),
    unquote(
      "min(calc(var(--board-height)/var(--num-rows)), calc(var(--board-height)/var(--num-rows)))"
    )
  );
  align-content: center;
  justify-content: center;

  .reversi-cell {
    width: 100%;
    height: 100%;
  }
}
</style>
