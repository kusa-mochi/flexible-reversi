<template>
  <div class="nickname">
    <form @submit="$router.push('/room-list')">
      <div>
        あなたのニックネームを決めてね
        <input v-model="user.name" type="text" required /><button>OK</button>
      </div>
    </form>
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
