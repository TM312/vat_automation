<template>
  <div>
    <h1 class="mb-5">
      Here is all Channel Data
    </h1>
    <b-row cols="1" cols-xl="2">
      <b-col v-for="channel in channels" :key="channel.code" class="my-2 px-2">
        <b-card class="h-100">
          <b-card-title>
            <b-row>
              <b-col cols="auto">
                {{ channel.name }}
              </b-col>
              <b-col cols="auto ml-auto">
                <b-button variant="outline-warning" size="sm">
                  <b-icon icon="pencil-square" /> Edit
                </b-button>
              </b-col>
            </b-row>
          </b-card-title>
          <b-card-sub-title>Code: {{ channel.code }}</b-card-sub-title>
          <b-card-text class="mt-3">
            {{ channel.description }}
          </b-card-text>
        </b-card>
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
