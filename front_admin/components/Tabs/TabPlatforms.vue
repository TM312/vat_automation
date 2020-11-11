<template>
  <div>
    <h1 class="mb-5">
      Here is all Channel Data
    </h1>
    <b-row cols="1" cols-xl="2">
      <b-col v-for="platform in platforms" :key="platform.code" class="my-2 px-2">
        <card-platform :platform="platform" />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "TabPlatforms",

  async fetch() {
    const { store } = this.$nuxt.context
    if (this.platforms.length === 0) {
      await store.dispatch("platform/get_all")
    }
  },
  computed: {
    ...mapState({
      platforms: (state) => state.platform.platforms,
    }),
  },
}
</script>

<style>
</style>
