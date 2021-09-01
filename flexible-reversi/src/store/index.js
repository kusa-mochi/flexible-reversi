import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
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
  },
  mutations: {
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
  actions: {},
  modules: {},
  plugins: [
    createPersistedState({
      key: "flexible-reversi",
      storage: window.sessionStorage,
    }),
  ],
});
