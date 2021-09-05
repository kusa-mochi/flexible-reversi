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
        <table class="about__table">
          <tbody>
            <tr>
              <td>ゲーム名</td>
              <td>Flexible Reversi</td>
            </tr>
            <tr>
              <td>バージョン</td>
              <td>1.0.0</td>
            </tr>
            <tr>
              <td>作者</td>
              <td>もち</td>
            </tr>
            <tr>
              <td>作者サイト</td>
              <td>
                <el-link
                  href="https://slash-mochi.net/"
                  target="_blank"
                  type="primary"
                  >// もちぶろ</el-link
                >
              </td>
            </tr>
            <tr>
              <td>ライセンス</td>
              <td>フリー（GPL 3）</td>
            </tr>
            <tr>
              <td>ソースコード</td>
              <td>
                <el-link
                  href="https://github.com/kusa-mochi/flexible-reversi"
                  target="_blank"
                  type="primary"
                  >https://github.com/kusa-mochi/flexible-reversi</el-link
                >
              </td>
            </tr>
            <tr>
              <td>お問合せ</td>
              <td class="email">@</td>
            </tr>
          </tbody>
        </table>
        <table class="history">
          <thead>
            <tr>
              <th>バージョン</th>
              <th>更新内容</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1.0.0</td>
              <td>新規リリース</td>
            </tr>
          </tbody>
        </table>
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
  methods: {
    onGoToTopButtonClick() {
      new Audio(require("@/assets/sounds/cancel-button.mp3")).play();
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
  // background-color: rgba(white, 0.95);
  width: 50%;
  margin: 4px 0px;
}
.about__table {
  width: 100%;
  background-color: rgba(white, 0.95);
  margin: 4px 0;

  td {
    padding: 16px;

    &.email {
      &:before {
        content: "whoatemyapplepie";
      }
      &:after {
        content: "gmail.com";
      }
    }
  }
}
.history {
  width: 100%;
  background-color: rgba(white, 0.95);
  margin: 8px 0 4px 0;

  th,
  td {
    padding: 16px;
  }
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
  .about__table,
  .history {
    th,
    td {
      padding: 4px;
    }
  }
}
</style>
