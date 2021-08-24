<template>
  <div class="nickname">
    <el-form>
      <div>
        あなたのニックネームを決めてね
        <el-input v-model="tmpNickname" type="text" required /><el-button
          @click="onSubmit"
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
  created() {
    // if not accessed from "top" page.
    if (this.currentPage !== "top") {
      // redirect to top page.
      this.$router.push("/");
    }
    this.currentPage = "nickname";
  },
  data() {
    return {
      tmpNickname: "",
    };
  },
  methods: {
    onSubmit(e) {
      console.log(e);
      // TODO: check if a name is not already used by another player.

      // save the nickname to a Vuex store.
      this.myNickname = this.tmpNickname;

      this.$router.push("/room-list");
    },
  },
  name: "Nickname",
};
</script>

<style lang="scss" scoped></style>
