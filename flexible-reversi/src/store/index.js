import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    backgroundBoardStatus: [
      [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
      [3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2],
      [2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1],
      [1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0],
      [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
      [3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2],
      [2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1],
      [1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0],
      [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
      [3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2],
      [2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1],
      [1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0],
      [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
      [3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2],
      [2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1],
      [1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0],
      [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
      [3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2],
      [2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1],
      [1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0],
      [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
      [3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2],
      [2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1],
      [1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0],
      [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
      [3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2],
      [2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1],
      [1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0],
    ],
    currentPage: "none",
    myNickname: "",
    roomCounter: 1,
    rooms: [
      //   {
      //     roomState: "vacancy",
      //     roomAuthor: "くさもちA",
      //     id: 1,
      //     requireEntryPassword: false,
      //     roomName: "部屋００１",
      //     canView: false,
      //   },
    ],
    serverUrl:
      "wss://rkyu0ms32g.execute-api.ap-northeast-1.amazonaws.com/production",
    token: null,
    // socket: null,
    gameData: {
      boardSize: {
        height: 8,
        width: 16,
      },
      // 1:black, 2:white
      currentPlayerColor: 1,
      // 0:blank, 1:black, 2:white, 3:wall
      boardStatus: [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
        [0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0],
        [0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      ],
      isJustViewing: false,
      opponentNickname: "",
      roomId: -1,
      myColor: -1,
    },
    //// game data
    isGameReady: false,
    isMyTurn: false,
    isGaming: false,
    //// BGM player
    bgmPlayer: null,
  },
  mutations: {
    playBgm(state, fileName) {
      if (!state.bgmPlayer) {
        state.bgmPlayer = new Audio(require(`@/assets/sounds/${fileName}`));
        state.bgmPlayer.loop = true;
        state.bgmPlayer.volume = 0.4;
        state.bgmPlayer.play();
      }
    },
    playSound(state, fileName) {
      new Audio(require(`@/assets/sounds/${fileName}`)).play();
    },
    resetGameData(state) {
      state.gameData.currentPlayerColor = 1;
      state.gameData.isJustViewing = true;
      state.gameData.opponentNickname = "";
      state.gameData.roomId = -1;
      state.gameData.myColor = -1;
      state.isGameReady = false;
      state.isMyTurn = false;
      state.isGaming = false;
    },
    stopBgm(state) {
      if (!state.bgmPlayer) {
        state.bgmPlayer.pause();
        state.bgmPlayer.currentTime = 0;
        state.bgmPlayer = null;
      }
    },
    updateLocalRoomsData(state, newData) {
      // sort newData by id
      newData.rooms.sort((roomA, roomB) => {
        if (roomA.id === roomB.id) {
          throw "invalid room id.";
        }
        return roomA.id > roomB.id ? 1 : -1;
      });

      // reset client rooms data.
      state.rooms.splice(0, state.rooms.length);
      newData.rooms.forEach((room) => {
        const roomData = {
          roomState: room.roomState,
          roomAuthor: room.roomAuthor,
          id: room.id,
          requireEntryPassword: room.requireEntryPassword,
          roomCounter: state.roomCounter++,
          roomName: room.roomName,
          canView: room.canView,
        };
        // console.log(roomData);
        state.rooms.push(roomData);
      });
      console.log("updated rooms.");
      console.log(state.rooms);
      state.rooms.splice();
    },
  },
  actions: {
    playBgm(context, fileName) {
      context.commit("playBgm", fileName);
    },
    playSound(context, fileName) {
      context.commit("playSound", fileName);
    },
    resetGameData(context) {
      context.commit("resetGameData");
    },
    stopBgm(context) {
      context.commit("stopBgm");
    },
  },
  modules: {},
  plugins: [
    createPersistedState({
      key: "flexible-reversi",
      storage: window.sessionStorage,
    }),
  ],
});
