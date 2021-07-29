<template>
  <div class="top">
    <p>top</p>
    <img alt="app logo" src="../assets/logo_mochi.png" />
    <ul>
      <li><router-link to="/nickname">スタート</router-link></li>
      <li><router-link to="/settings">設定</router-link></li>
      <li><router-link to="/stage-editor">ステージをつくる</router-link></li>
    </ul>
  </div>
</template>

<script>
// // @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";

export default {
  components: {
    // HelloWorld,
  },
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
    this.currentPage = "top";
  },
  name: "Top",
};
</script>
