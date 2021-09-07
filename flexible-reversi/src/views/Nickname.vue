<template>
  <div class="nickname">
    <reversi-board
      :board-width="2000"
      :board-status="backgroundBoardStatus"
      :is-read-only="true"
      class="nickname-background"
      z-index="0"
    ></reversi-board>
    <div class="nickname__header">
      <el-button
        @click="onGoToTopButtonClick"
        class="go-to-top-button"
        icon="el-icon-s-home"
        >トップに戻る</el-button
      >
    </div>
    <div class="nickname__body">
      <div class="form-container">
        <el-form @submit.native.prevent="onSubmit" :inline="true" :model="form">
          <div>
            <div class="nickname-input-label">
              あなたのニックネームを決めてね
            </div>
            <div class="nickname-input-container">
              <el-input
                v-model="form.tmpNickname"
                @keyboard.enter.prevent
                class="nickname-input"
                maxlength="20"
                placeholder="ニックネーム"
                ref="nicknameInput"
                required
                show-word-limit
                type="text"
              /><el-button @click="onSubmit" :disabled="!gotToken"
                >OK</el-button
              >
            </div>
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import ReversiBoard from "@/components/ReversiBoard.vue";
export default {
  components: {
    ReversiBoard,
  },
  computed: {
    backgroundBoardStatus: {
      get() {
        return this.$store.state.backgroundBoardStatus;
      },
    },
    currentPage: {
      get() {
        return this.$store.state.currentPage;
      },
      set(newValue) {
        this.$store.state.currentPage = newValue;
      },
    },
    myNickname: {
      get() {
        return this.$store.state.myNickname;
      },
      set(newValue) {
        this.$store.state.myNickname = newValue;
      },
    },
    serverUrl: {
      get() {
        return this.$store.state.serverUrl;
      },
    },
    token: {
      get() {
        return this.$store.state.token;
      },
      set(newValue) {
        if (newValue === undefined || newValue === null || newValue === "") {
          throw "invalid token value.";
        }
        this.$store.state.token = newValue;
      },
    },
  },
  created() {
    // if your nickanme is already set.
    if (this.myNickname) {
      // redirect to the room list page.
      this.$router.push("/room-list");
      return;
    }

    // create a WebSocket instance.
    if (this.socket === null) {
      this.initializeWebSocket();
    }

    this.currentPage = "nickname";
  },
  data() {
    return {
      form: {
        tmpNickname: "",
      },
      socket: null,
      gotToken: false,
    };
  },
  methods: {
    initializeWebSocket() {
      this.socket = new WebSocket(this.serverUrl);
      this.socket.onopen = (e) => {
        console.log("onopen");
        console.log(e);

        if (!this.token) {
          // request a token to keep communicating with the server even after a page transition.
          this.socket.send(JSON.stringify({ action: "newToken" }));
        }
      };
      this.socket.onmessage = (e) => {
        console.log("onmessage");
        console.log(e);
        const parsedData = JSON.parse(e.data);
        console.log(parsedData);

        // check data type
        if (parsedData.dataType === "newToken") {
          console.log("received newToken");
          const token = parsedData.data.token;
          this.token = token;
          this.gotToken = true;
        } else if (parsedData.dataType === "checkNicknameAvailability") {
          console.log("received checkNicknameAvailability");
          const availability = parsedData.data.nicknameAvailability;
          switch (availability) {
            case "inUse":
              this.$store.dispatch("playSound", "info.mp3");
              this.$notify({
                title: "Error",
                message: `${this.form.tmpNickname} という名前は既に使われています。別の名前を指定してください。`,
                type: "error",
              });
              break;
            case "isAvailable":
              this.$store.dispatch("playSound", "ok-button.mp3");
              // save the nickname to a Vuex store.
              this.myNickname = this.form.tmpNickname;
              // go to the room list page.
              this.$router.push("/room-list");
              return;
            default:
              break;
          }
        }
      };
      this.socket.onclose = (e) => {
        console.log("onclose");
        console.log(e);
      };
      this.socket.onerror = (e) => {
        console.log("onerror");
        console.log(e);
      };
    },
    onGoToTopButtonClick() {
      this.$store.dispatch("playSound", "cancel-button.mp3");
      this.$router.push({ path: "/" });
    },
    onSubmit(e) {
      console.log("onSubmit");
      console.log(e);
      // check if a name is not already used by another player.
      this.socket.send(
        JSON.stringify({
          action: "checkNicknameAvailability",
          data: {
            nickname: this.form.tmpNickname,
            token: this.token,
          },
        })
      );
    },
  },
  mounted() {
    this.$refs.nicknameInput.focus();
  },
  name: "Nickname",
};
</script>

<style lang="scss" scoped>
$headerHeight: 56px;

.nickname {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}
.nickname-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  opacity: 0.6;
}
.nickname__header {
  position: relative;
  width: 100%;
  height: $headerHeight;
  background-color: rgba(white, 0.95);

  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: flex-start;
  align-items: center;
  align-content: center;

  .go-to-top-button {
    position: relative;
    margin: 8px;
    z-index: 10;
  }
}
.nickname__body {
  position: relative;
  width: 100%;
  height: calc(100% - #{$headerHeight});
  overflow: hidden;

  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: center;
  align-items: center;

  .form-container {
    background-color: rgba(white, 0.95);
    padding: 16px;
    z-index: 10;
  }
  .nickname-input-container {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: flex-start;
    align-items: flex-start;
    align-content: flex-start;
  }
  .nickname-input {
    width: 376px;
    margin-right: 8px;
  }
}

@media screen and (max-width: 400px) {
  .nickname__body {
    .nickname-input {
      width: 100%;
    }
  }
}
</style>
