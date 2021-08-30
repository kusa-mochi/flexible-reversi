export default class ReversiNode {
  // initStatus: init board status. 2-dims number array.
  // player: 1:black, 2:white
  constructor(initStatus, player) {
    if (
      initStatus === undefined ||
      initStatus === null ||
      !Array.isArray(initStatus) ||
      initStatus.length === 0 ||
      !Array.isArray(initStatus[0]) ||
      initStatus[0].length === 0
    ) {
      throw "initStatus must be 2-dimensional array of numbers.";
    }
    if (!this.between(player, 1, 2)) {
      throw "player:" + player + ", 'player' must be 1 or 2.";
    }

    // instance fields
    this._numRow = 0;
    this._numColumn = 0;
    this._status = [];
    this._player = 0;

    this._numRow = initStatus.length;
    this._numColumn = initStatus[0].length;
    this._player = player;

    for (let iRow = 0; iRow < this._numRow; iRow++) {
      const newRow = initStatus[iRow].slice(0);
      this._status.push(newRow);
    }

    // console.log("ReversiNode initialized.");
    // console.log("  _numRow: " + this._numRow);
    // console.log("  _numColumn: " + this._numColumn);
    // console.log("  _player: " + this._player);
    // console.log("  _status:");
    // console.log(this._status);
  }

  canPutStone(iColumn, iRow) {
    return this.putStoneCore(iColumn, iRow);
  }

  canPutStoneOnAnyPlace() {
    for (let iRow = 0; iRow < this._numRow; iRow++) {
      for (let iColumn = 0; iColumn < this._numColumn; iColumn++) {
        if (this.canPutStone(iColumn, iRow)) return true;
      }
    }
    return false;
  }

  getNumEmpty() {
    return this.getNumSpecificStateCells(0);
  }

  getNumBlack() {
    return this.getNumSpecificStateCells(1);
  }

  getNumWhite() {
    return this.getNumSpecificStateCells(2);
  }

  getNumSpecificStateCells(state) {
    let output = 0;
    for (let iRow = 0; iRow < this._numRow; iRow++) {
      output += this._status[iRow].filter((item) => item === state).length;
    }
    return output;
  }

  putStoneCore(iColumn, iRow) {
    // console.log("putStoneCore begin.");
    if (!this.between(iColumn, 0, this._numColumn - 1)) {
      throw "invalid range 'iColumn'.";
    }
    if (!this.between(iRow, 0, this._numRow - 1)) {
      throw "invalid range 'iRow'.";
    }

    // if not an empty cell.
    if (this._status[iRow][iColumn] !== 0) {
      // console.log("it is not an empty cell.");
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
      up || rightUp || right || rightDown || down || leftDown || left || leftUp;

    return searchResult;
  }

  // search if a player can put its stone on specified direction.
  // columnDirection: -1/0/+1
  // rowDirection: -1/0/+1
  searchOnDirection(iColumn, iRow, dirColumn, dirRow) {
    if (this._status[iRow][iColumn] != 0) {
      return false;
    }

    const xNeighbor = iColumn + dirColumn;
    const yNeighbor = iRow + dirRow;
    const boardWidth = this._status[0].length;
    const boardHeight = this._status.length;
    if (
      !this.between(xNeighbor, 0, boardWidth - 1) ||
      !this.between(yNeighbor, 0, boardHeight - 1)
    ) {
      return false;
    }

    let x = xNeighbor;
    let y = yNeighbor;
    const opponentPlayerColor = this.opponentPlayer();

    if (this._status[y][x] !== opponentPlayerColor) {
      return false;
    }

    x += dirColumn;
    y += dirRow;
    while (
      this.between(x, 0, boardWidth - 1) &&
      this.between(y, 0, boardHeight - 1)
    ) {
      if (this._status[y][x] == this._player) {
        return true;
      }
      if (this._status[y][x] == opponentPlayerColor) {
        x += dirColumn;
        y += dirRow;
      }
    }

    // // if a neighbor is opponent
    // if (this._status[y][x] === opponent) {
    //   let ifBreak = false;
    //   for (
    //     x += columnDirection, y += rowDirection;
    //     this.between(x, 0, this._numColumn - 1) &&
    //     this.between(y, 0, this._numRow - 1);
    //     x += columnDirection, y += rowDirection
    //   ) {
    //     // console.log(`(${x},${y}): ${this._status[y][x]}`);
    //     const currentCell = this._status[y][x];
    //     switch (currentCell) {
    //       case 0: // empty cell
    //         ifBreak = true;
    //         break;
    //       case 3: // wall
    //         ifBreak = true;
    //         break;
    //       default:
    //         if (currentCell === this._player) {
    //           canPut = true;
    //         } else if (currentCell === opponent) {
    //           // do nothing.
    //         } else {
    //           throw `invalid cell state:${currentCell}`;
    //         }
    //         break;
    //     }

    //     if (ifBreak) break;
    //   }

    //   if (canPut) {
    //     return true;
    //   }
    // }

    return false;
  }

  opponentPlayer() {
    return this._player === 1 ? 2 : 1;
  }

  between(n, min, max) {
    return min <= n && n <= max;
  }
}
