<template>
  <div class="reversi-board" :style="boardSizeStyle">
    <template v-for="(tmp1, iRow) in numRows">
      <template v-for="(tmp2, iColumn) in numColumns">
        <div :key="iRow * numColumns + iColumn" class="reversi-cell">
          <reversi-cell
            @click="onClickCell(iColumn, iRow)"
            :state="boardStatus._status[iRow][iColumn]"
          ></reversi-cell>
        </div>
      </template>
    </template>
  </div>
</template>

<script>
import ReversiCell from "@/components/ReversiCell";
import ReversiNode from "@/classes/ReversiNode.js";

export default {
  components: {
    ReversiCell,
  },
  computed: {
    boardHeight: {
      get() {
        return (this.boardWidth * this.numRows) / this.numColumns;
      },
    },
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
    currentBoardStatus: {
      get() {
        return this.boardStatus._status;
      },
    },
    numColumns: {
      get() {
        return this.initialBoardStatus[0].length;
      },
    },
    numRows: {
      get() {
        return this.initialBoardStatus.length;
      },
    },
  },
  created() {
    this.boardStatus = new ReversiNode(this.initialBoardStatus, 1);
    const returnValue = {
      nextPlayer: this.boardStatus._player,
      numEmpty: this.boardStatus.getNumEmpty(),
      numBlack: this.boardStatus.getNumBlack(),
      numWhite: this.boardStatus.getNumWhite(),
      canPutStone: this.boardStatus.canPutStoneOnAnyPlace(),
    };
    this.$emit("initialized", returnValue);
  },
  data() {
    return {
      boardStatus: null,
    };
  },
  methods: {
    onClickCell(iColumn, iRow) {
      if (this.isReadOnly) return;

      const putSound = new Audio(require("@/assets/put-stone.mp3"));
      console.log("on click cell: " + iColumn + ", " + iRow);
      const result = this.boardStatus.putStone(iColumn, iRow);
      this.boardStatus._status = this.boardStatus._status.slice(0);

      // if a stone was put.
      if (result) {
        this.$emit("stone-put", {
          column: iColumn,
          row: iRow,
        });
        putSound.play();
      }

      const returnValue = {
        nextPlayer: this.boardStatus._player,
        numEmpty: this.boardStatus.getNumEmpty(),
        numBlack: this.boardStatus.getNumBlack(),
        numWhite: this.boardStatus.getNumWhite(),
        canPutStone: this.boardStatus.canPutStoneOnAnyPlace(),
      };

      if (
        returnValue.numEmpty === 0 ||
        returnValue.numBlack === 0 ||
        returnValue.numWhite === 0
      ) {
        this.$emit("game-set", returnValue);
        return;
      }

      if (!returnValue.canPutStone) {
        this.boardStatus.goToNextTurn();
        if (!this.boardStatus.canPutStoneOnAnyPlace()) {
          this.$emit("game-set", returnValue);
          return;
        } else {
          this.$emit("pass-turn", returnValue);
        }
        return;
      }

      this.$emit("click-cell", returnValue);
    },
    setBoardStatus(status) {
      this.boardStatus._status.splice(0, this.boardStatus._status.length);
      status.forEach((row) => {
        this.boardStatus._status.push(row.slice());
      });
    },
  },
  name: "ReversiBoard",
  props: {
    boardWidth: {
      type: Number,
      required: false,
      default: 800,
    },
    initialBoardStatus: {
      type: Array,
      required: true,
      default: () => [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 1, 0, 0, 0],
        [0, 0, 0, 1, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
      ],
    },
    isReadOnly: {
      type: Boolean,
      required: false,
      default: false,
    },
    // numColumns: {
    //   type: Number,
    //   required: false,
    //   default: 8,
    // },
    // numRows: {
    //   type: Number,
    //   required: false,
    //   default: 8,
    // },
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
