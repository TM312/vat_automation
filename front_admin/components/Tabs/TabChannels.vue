<template>
  <div>
    <h1 class="mb-5">
      Here is all Channel Data
    </h1>
    <b-row cols="1" cols-xl="2">
      <b-col v-for="channel in channels" :key="channel.code" class="my-2 px-2">
        <card-channel :channel="channel" />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "TabAccounts",

  async fetch() {
    const { store } = this.$nuxt.context
    if (this.channels.length === 0) {
      await store.dispatch("channel/get_all")
    }
  },
  computed: {
    ...mapState({
      channels: (state) => state.channel.channels,
    }),
  },
}
</script>

<style>
</style>
