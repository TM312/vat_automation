<template>
  <div>
    <toast-data-upload-invalid-file />
    <b-toast
      v-model="toastSellerFirm"
      no-auto-hide
      :title="titleSellerFirm"
      :variant="doneStatusSellerFirmTargets ? 'success' : ''"
    >
      <div v-for="(sellerFirmTarget, i) in statusSellerFirmTargets" :key="i" class="pt-2">
        <div v-if="sellerFirmTarget.target !== 'errorbox' && sellerFirmTarget.target !== 'infobox'">
          <div v-if="statusSellerFirmTargets[i].done">
            <b-row no-gutters>
              <b-col cols="1">
                <b-icon icon="check-circle" variant="success" />
              </b-col>
              <b-col cols="11">
                <p lead>
                  {{ statusSellerFirmTargets[i].message }}
                </p>
              </b-col>
            </b-row>
          </div>

          <div v-else>
            <b-progress :value="statusSellerFirmTargets[i].current" :max="statusSellerFirmTargets[i].total" animated />
          </div>
          <small class="text-muted mt-1">Source: <i>{{ statusSellerFirmTargets[i].target }}</i></small>
        </div>

        <div v-else-if="sellerFirmTarget.target === 'errorbox'">
          <b-card border-variant="danger">
            <b-card-text>{{ sellerFirmTarget.message }}</b-card-text>
          </b-card>
        </div>

        <div v-else-if="sellerFirmTarget.target === 'infobox'">
          <b-card border-variant="info">
            <b-card-text>
              {{ sellerFirmTarget.message }}
              <span v-if="doneStatusSellerFirmTargets && sellerFirmTarget.duplicate_list && sellerFirmTarget.duplicate_list.length > 2">
                <b-icon v-b-modal.seller-firm-duplicates icon="info-circle" variant="outline-info" class="ml-1" />
                <b-modal id="seller-firm-duplicates" title="Transaction Duplicates">
                  <ul>
                    <li v-for="(duplicate, index) in sellerFirmTarget.duplicate_list" :key="index">{{ duplicate }}</li>
                  </ul>
                </b-modal>
              </span>
            </b-card-text>
          </b-card>
        </div>

        <hr v-if="statusSellerFirmTargets.length > 1" />
      </div>
    </b-toast>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: 'ToastSellerFirmDataUpload',

    data() {
        return {
            toastSellerFirm: false
        }
    },

    computed: {
        ...mapState({
            statusSellerFirmTargets: state => state.status.seller_firm_targets,
            lenStatusSellerFirm: state => state.status.seller_firm_targets.length,


        }),

        doneStatusSellerFirmTargets() {
            return this.$store.getters['status/doneStatusSellerFirmTargets']
        },

        totalStatusSellerFirmTargets() {
            return this.$store.getters['status/totalStatusSellerFirmTargets']
        },

        titleSellerFirm() {
            if (this.doneStatusSellerFirmTargets) {
                return (this.lenStatusSellerFirm === 1) ? 'Uploaded seller firm data processed' : `${this.totalStatusSellerFirmTargets} uploaded seller firms processed`
            } else {
                return 'New seller firms are being registered...'
            }
        },

    },

    watch: {
        // https://stackoverflow.com/questions/43270159/vue-js-2-how-to-watch-store-values-from-vuex
        /*eslint-disable */

        lenStatusSellerFirm (newLength, oldLength) {
            if (oldLength === 0) {
                this.toastSellerFirm = true
            }
        },

       async doneStatusSellerFirmTargets (val, oldVal) {
            if (val) {
                await this.sleep(11000)
                this.toastSellerFirm = false
                await this.sleep(1000)
                const { store } = this.$nuxt.context
                store.commit('status/CLEAR_STATUS_SELLER_FIRM_TARGETS')
            }
       },

        /*eslint-disable */

    }


}
</script>
