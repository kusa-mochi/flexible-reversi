<template>
  <div class="reversi-board" :style="boardSizeStyle">
    <template v-for="(tmp1, iRow) in numRows">
      <template v-for="(tmp2, iColumn) in numColumns">
        <div :key="iRow * numColumns + iColumn" class="reversi-cell">
          <reversi-cell
            @click="onClickCell(iColumn, iRow)"
            :state="boardStatus[iRow][iColumn]"
          ></reversi-cell>
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
    numColumns: {
      get() {
        return this.boardStatus[0].length;
      },
    },
    numRows: {
      get() {
        return this.boardStatus.length;
      },
    },
    opponentPlayerColor: {
      get() {
        return this.playerColor == 1 ? 2 : 1;
      },
    },
  },
  created() {
    // this.boardStatus = new ReversiNode(this.initialBoardStatus, 1);
    // const returnValue = {
    //   nextPlayer: this.boardStatus._player,
    //   numEmpty: this.boardStatus.getNumEmpty(),
    //   numBlack: this.boardStatus.getNumBlack(),
    //   numWhite: this.boardStatus.getNumWhite(),
    //   canPutStone: this.boardStatus.canPutStoneOnAnyPlace(),
    // };
    // this.$emit("initialized", returnValue);
    this.$emit("initialized");
  },
  methods: {
    between(n, min, max) {
      return min <= n && n <= max;
    },
    canPutStone(iColumn, iRow) {
      console.log("player color");
      console.log(this.playerColor);
      if (!this.between(iColumn, 0, this.numColumns - 1)) {
        throw "invalid range 'iColumn'.";
      }
      if (!this.between(iRow, 0, this.numRows - 1)) {
        throw "invalid range 'iRow'.";
      }

      // if not an empty cell.
      if (this.boardStatus[iRow][iColumn] !== 0) {
        console.log("it is not an empty cell.");
        // it cannot put a stone.
        return false;
      }

      const up = this.searchOnDirection(iColumn, iRow, 0, -1);
      const rightUp = this.searchOnDirection(iColumn, iRow, 1, -1);
      const right = this.searchOnDirection(iColumn, iRow, 1, 0);
      const rightDown = this.searchOnDirection(iColumn, iRow, 1, 1);
      const down = this.searchOnDirection(iColumn, iRow, 0, 1);
      const leftDown = this.searchOnDirection(iColumn, iRow, -1, 1);
      const left = this.searchOnDirection(iColumn, iRow, -1, 0);
      const leftUp = this.searchOnDirection(iColumn, iRow, -1, -1);

      const searchResult =
        up ||
        rightUp ||
        right ||
        rightDown ||
        down ||
        leftDown ||
        left ||
        leftUp;

      return searchResult;
    },
    onClickCell(iColumn, iRow) {
      if (this.isReadOnly) return;

      console.log(`on click cell: ${iColumn}, ${iRow}`);
      const result = this.canPutStone(iColumn, iRow);

      // if you can put a stone
      if (result) {
        console.log("emitting..");
        this.$emit("stone-put", {
          column: iColumn,
          row: iRow,
        });
        // this.putSound.play();
      }

      // const returnValue = {
      //   nextPlayer: this.playerColor,
      //   numEmpty: this.boardStatus.getNumEmpty(),
      //   numBlack: this.boardStatus.getNumBlack(),
      //   numWhite: this.boardStatus.getNumWhite(),
      //   canPutStone: this.boardStatus.canPutStoneOnAnyPlace(),
      // };

      // if (
      //   returnValue.numEmpty === 0 ||
      //   returnValue.numBlack === 0 ||
      //   returnValue.numWhite === 0
      // ) {
      //   this.$emit("game-set", returnValue);
      //   return;
      // }

      // if (!returnValue.canPutStone) {
      //   // this.boardStatus.goToNextTurn();
      //   if (!this.boardStatus.canPutStoneOnAnyPlace()) {
      //     this.$emit("game-set", returnValue);
      //     return;
      //   } else {
      //     this.$emit("pass-turn", returnValue);
      //   }
      //   return;
      // }

      // this.$emit("click-cell", returnValue);
      // this.$emit("click-cell");
    },
    searchOnDirection(iColumn, iRow, dirColumn, dirRow) {
      const xNeighbor = iColumn + dirColumn;
      const yNeighbor = iRow + dirRow;
      if (
        !this.between(xNeighbor, 0, this.numColumns - 1) ||
        !this.between(yNeighbor, 0, this.numRows - 1)
      ) {
        return false;
      }

      let x = xNeighbor;
      let y = yNeighbor;

      if (this.boardStatus[y][x] !== this.opponentPlayerColor) {
        return false;
      }

      for (
        x += dirColumn, y += dirRow;
        this.between(x, 0, this.numColumns - 1) &&
        this.between(y, 0, this.numRows - 1);
        x += dirColumn, y += dirRow
      ) {
        if (this.boardStatus[y][x] === this.playerColor) {
          return true;
        }
        if (this.boardStatus[y][x] !== this.opponentPlayerColor) {
          return false;
        }
      }

      return false;
    },
    // setBoardStatus(status, nextPlayerColor) {
    //   this.boardStatus.splice(0, this.boardStatus.length);
    //   status.forEach((row) => {
    //     this.boardStatus.push(row.slice());
    //   });
    //   this.playerColor = nextPlayerColor;
    //   this.putSound.play();
    // },
  },
  name: "ReversiBoard",
  props: {
    boardWidth: {
      type: Number,
      required: false,
      default: 800,
    },
    boardStatus: {
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
    playerColor: {
      type: Number,
      required: false,
      default: 1,
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
