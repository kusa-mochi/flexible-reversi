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
