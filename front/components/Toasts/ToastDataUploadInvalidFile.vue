<template>
  <div>
    <b-toast
      v-model="toastFile"
      no-auto-hide
      title="Invalid File"
      variant="danger"
    >
      <div v-for="(fileTarget, i) in statusFileTargets" :key="i" class="pt-2">
        <div v-if="fileTarget.target === 'errorbox'">
          <b-card border-variant="danger">
            <b-card-text>{{ fileTarget.message }}</b-card-text>
          </b-card>
        </div>
        <hr v-if="statusFileTargets.length > 1" />
      </div>
    </b-toast>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'ToastDataUploadInvalidFile',

  data() {
    return {
      toastFile: false
    }
  },

  computed: {
    ...mapState({
      statusFileTargets: state => state.status.file_targets,
      lenStatusFile: state => state.status.file_targets.length,


    }),

    doneStatusFileTargets() {
      return this.$store.getters['status/doneStatusFileTargets']
    },

    totalStatusFileTargets() {
      return this.$store.getters['status/totalStatusFileTargets']
    },

  },

  watch: {
    // https://stackoverflow.com/questions/43270159/vue-js-2-how-to-watch-store-values-from-vuex
    /*eslint-disable */

        lenStatusFile (newLength, oldLength) {
            if (oldLength === 0) {
                this.toastFile = true
            // } else if (newLength === 0) {
            //     this.toastFile = false
            }
        },

       async doneStatusFileTargets (val, oldVal) {
            if (val) {
                await this.sleep(11000)
                this.toastFile = false
                await this.sleep(1000)
                const { store } = this.$nuxt.context
                store.commit('status/CLEAR_STATUS_FILE_TARGETS')
            }
       },

        /*eslint-disable */

    }


}
</script>
