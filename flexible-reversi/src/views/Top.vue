<template>
  <div id="top" class="top">
    <reversi-board
      :board-width="2000"
      :board-status="backgroundBoardStatus"
      :is-read-only="true"
      class="top-background"
      z-index="0"
    ></reversi-board>
    <div class="app-logo">
      <a href="https://slash-mochi.net/">
        <img alt="app logo" src="../assets/logo_mochi.png" />
      </a>
    </div>
    <div class="app-name">Flexible Reversi</div>
    <el-menu class="top-menu" router @open="handleOpen" @close="handleClose">
      <el-menu-item class="top-menu-item" index="Nickname">
        <i class="el-icon-s-grid"></i>スタート
      </el-menu-item>
      <el-menu-item class="top-menu-item" disabled index="Settings">
        <i class="el-icon-setting"></i>設定
      </el-menu-item>
      <el-menu-item class="top-menu-item" disabled index="StageEditor">
        <i class="el-icon-edit"></i>ステージをつくる
      </el-menu-item>
      <el-menu-item class="top-menu-item" index="About">
        <i class="el-icon-cold-drink"></i>バージョン情報
      </el-menu-item>
    </el-menu>
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
    this.currentPage = "top";
  },
  name: "Top",
};
</script>

<style lang="scss" scoped>
.top {
  position: relative;
  overflow: hidden;
  width: 100%;
  height: 100%;

  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: center;
  align-items: center;

  .top-background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    opacity: 0.6;
  }
  .app-logo {
    position: absolute;
    top: 10px;
    left: 10px;

    img {
      width: 64px;
    }
  }
  .app-name {
    $fontSize: 32px;
    color: #2a2a2a;
    position: absolute;
    top: calc(50% - 109px);
    left: calc(50% - 534px);
    font-size: 102px;
    font-family: "Bungee Inline", Roboto, cursive;
  }
  .top-menu {
    margin-top: 440px;
  }
}

@media screen and (max-width: 1100px) {
  .top {
    .app-name {
      font-size: 40px;
      left: calc(50% - 202px);
    }
    .top-menu {
      margin-top: 240px;
    }
  }
}

@media screen and (max-width: 500px) {
  .top {
    .app-name {
      font-size: 28px;
      left: calc(50% - 147px);
    }
    .top-menu {
      margin-top: 187px;
    }
  }
}
</style>

<style lang="scss">
#top {
  .el-menu {
    border: none;
  }
}
</style>
