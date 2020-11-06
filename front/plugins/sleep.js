import Vue from 'vue'

Vue.mixin({
  methods: {
    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
    },
  }
})
