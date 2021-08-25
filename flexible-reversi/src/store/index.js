import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    currentPage: "none",
    myNickname: "",
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
    stageSettings: {
      // 0:blank, 1:black, 2:white
      initialStatus: [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
        [0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0],
        [0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      ],
      boardSize: {
        height: 8,
        width: 16,
      },
    },
  },
  mutations: {},
  actions: {},
  modules: {},
});
