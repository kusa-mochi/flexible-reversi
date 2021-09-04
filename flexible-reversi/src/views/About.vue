<template>
  <div class="about">
    <reversi-board
      :board-width="2000"
      :board-status="backgroundBoardStatus"
      :is-read-only="true"
      class="about-background"
      z-index="0"
    ></reversi-board>
    <div class="about__header">
      <el-button
        @click="onGoToTopButtonClick"
        class="go-to-top-button"
        icon="el-icon-s-home"
        >トップに戻る</el-button
      >
    </div>
    <div class="about__body">
      <div class="about__content">
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
        <div>あああああああ</div>
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
      return;
    }
    this.currentPage = "about";
  },
  data() {
    return {
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
    };
  },
  methods: {
    onGoToTopButtonClick() {
      this.$router.push({ path: "/" });
    },
  },
  name: "About",
};
</script>

<style lang="scss" scoped>
$headerHeight: 56px;

.about {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}
.about-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  opacity: 0.6;
  z-index: 0;
}
.about__header {
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
.about__body {
  position: relative;
  width: 100%;
  height: calc(100% - #{$headerHeight});
  overflow-x: hidden;
  overflow-y: scroll;

  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: flex-start;
  align-items: center;
}
.about__content {
  background-color: rgba(white, 0.95);
  width: 50%;
  margin: 8px 0px;
}

@media screen and (max-width: 1000px) {
  .about__content {
    width: 70%;
  }
}

@media screen and (max-width: 767px) {
  .about__content {
    width: 90%;
  }
}
</style>
