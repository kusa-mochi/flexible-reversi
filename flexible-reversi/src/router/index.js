import Vue from "vue";
import VueRouter from "vue-router";
import Top from "@/views/Top.vue";
import Nickname from "@/views/Nickname.vue";
import RoomList from "@/views/RoomList.vue";
import Game from "@/views/Game.vue";
import Settings from "@/views/Settings.vue";
import StageEditor from "@/views/StageEditor.vue";
import About from "@/views/About.vue";

Vue.use(VueRouter);

const routes = [
  // トップページ
  {
    path: "/",
    component: Top,
  },
  // ニックネーム設定ページ
  {
    path: "/nickname",
    component: Nickname,
  },
  // 部屋一覧ページ
  {
    path: "/room-list",
    component: RoomList,
  },
  // 対局ページ
  {
    path: "/game",
    component: Game,
  },
  // 設定ページ
  {
    path: "/settings",
    component: Settings,
  },
  // ステージ作成ページ
  {
    path: "/stage-editor",
    component: StageEditor,
  },
  // このゲームについて
  {
    path: "/about",
    component: About,
  },
];

const router = new VueRouter({
  routes: routes,
});

export default router;
