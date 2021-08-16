<template>
  <div class="nickname">
    <el-form>
      <div>
        あなたのニックネームを決めてね
        <el-input v-model="user.name" type="text" required /><el-button
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
  },
  created() {
    // if not accessed from "top" page.
    if (this.currentPage !== "top") {
      // redirect to top page.
      this.$router.push("/");
    }
    this.currentPage = "nickname";
  },
  methods: {
    onSubmit(e) {
      console.log(e);
      // TODO: check if a name is not already used by another player.

      this.$router.push("/room-list");
    },
  },
  name: "Nickname",
  props: {
    user: {
      type: Object,
      required: true,
      default: null,
    },
  },
};
</script>

<style lang="scss" scoped></style>
