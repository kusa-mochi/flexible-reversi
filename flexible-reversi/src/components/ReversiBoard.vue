<template>
  <div class="reversi-board" :style="boardSizeStyle">
    <template v-for="(tmp1, iRow) in numRows">
      <template v-for="(tmp2, iColumn) in numColumns">
        <div :key="iRow * numColumns + iColumn" class="reversi-cell">
          <reversi-cell :state="cellState(iColumn, iRow)"></reversi-cell>
        </div>
      </template>
    </template>
  </div>
</template>

<script>
import ReversiCell from "@/components/ReversiCell";

export default {
  components: {
    ReversiCell,
  },
  computed: {
    boardSizeStyle: {
      get() {
        return {
          "--board-width": `${this.boardWidth}px`,
          "--board-height": `${this.boardHeight}px`,
          "--num-columns": this.numColumns,
          "--num-rows": this.numRows,
        };
      },
    },
  },
  methods: {
    cellState(iColumn, iRow) {
      return this.boardStatus[iRow][iColumn];
    },
  },
  name: "ReversiBoard",
  props: {
    boardWidth: {
      type: Number,
      require: false,
      default: 800,
    },
    boardHeight: {
      type: Number,
      require: false,
      default: 800,
    },
    boardStatus: {
      type: Array,
      required: true,
    },
    numColumns: {
      type: Number,
      require: false,
      default: 8,
    },
    numRows: {
      type: Number,
      require: false,
      default: 8,
    },
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

  width: var(--board-width);
  height: var(--board-height);
  background-color: #00a858;
  border: 4px solid #505050;

  .reversi-cell {
    width: 100%;
    height: 100%;
    border: 0.5px solid #505050;
  }
}
</style>
