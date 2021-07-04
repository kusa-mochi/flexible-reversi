import Vue from "vue";
import VueRouter from "vue-router";
import Top from "../views/Top.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Top",
    component: Top,
  },
  {
    path: "/stage-select",
    name: "StageSelect",
    component: function () {
      return import(/* webpackChunkName: "stage-select" */ "../views/StageSelect.vue");
    },
  },
  {
    path: "/game",
    name: "Game",
    component: function () {
      return import(/* webpackChunkName: "game" */ "../views/Game.vue");
    },
  },
  {
    path: "/settings",
    name: "Settings",
    component: function () {
      return import(/* webpackChunkName: "settings" */ "../views/Settings.vue");
    },
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: function () {
      return import(/* webpackChunkName: "about" */ "../views/About.vue");
    },
  },
];

const router = new VueRouter({
  routes,
});

export default router;
