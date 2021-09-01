<template>
  <div class="nickname">
    <el-form>
      <div>
        あなたのニックネームを決めてね
        <el-input v-model="tmpNickname" type="text" required /><el-button
          @click="onSubmit"
          :disabled="!gotToken"
          >OK</el-button
        >
      </div>
    </el-form>
  </div>
</template>

<script>
export default {
  computed: {
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
    // // if not accessed from "top" page.
    // if (this.currentPage !== "top") {
    //   // redirect to top page.
    //   this.$router.push("/");
    //   return;
    // }

    // if your nickanme is already set.
    if(this.myNickname) {
      // redirect to the room list page.
      this.$router.push("/room-list");
    }

    // create a WebSocket instance.
    if (this.socket === null) {
      this.initializeWebSocket();
    }

    this.currentPage = "nickname";
  },
  data() {
    return {
      tmpNickname: "",
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

        // request a token to keep communicating with the server even after a page transition.
        this.socket.send(JSON.stringify({ action: "newToken" }));
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
              this.$notify({
                title: "Error",
                message: `${this.tmpNickname} という名前は既に使われています。別の名前を指定してください。`,
                type: "error",
              });
              break;
            case "isAvailable":
              // save the nickname to a Vuex store.
              this.myNickname = this.tmpNickname;
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
    onSubmit(e) {
      console.log(e);
      // check if a name is not already used by another player.
      this.socket.send(
        JSON.stringify({
          action: "checkNicknameAvailability",
          data: {
            nickname: this.tmpNickname,
            token: this.token,
          },
        })
      );
    },
  },
  name: "Nickname",
};
</script>

<style lang="scss" scoped></style>
