<template>
  <div>
    <div v-if="transactionInputTable">
      <!-- <b-button v-if="transactionInputs.length > 0" variant="outline-danger" class="ml-auto" :disabled="buttonRemoveDisabled" @click="removeAll">
        Delete All
      </b-button> -->
      <b-tabs pills content-class="mt-3">
        <b-tab title="Total" active>
          <b-card
            v-if="transactionInputs.length === 0"
            class="text-center py-5"
          >
            <b-card-text>
              <h5 v-if="transactionInputs.length === 0" class="text-muted text-center m-5">
                No Data Available Yet
              </h5>
            </b-card-text>
          </b-card>
          <div v-else>
            <table-transaction-inputs :transaction-inputs="transactionInputs" @single-view="getSingleView($event)" />
          </div>
        </b-tab>
        <b-tab v-for="account in sellerFirm.accounts" :key="account.public_id" :title="account.channel_code" :disabled="transactionInputs.length === 0">
          <b-card
            v-if="transactionInputsChannel(account.channel_code).length === 0"
            sub-title="No transactions have been registered for this channel."
            class="text-center py-5"
          />
          <div v-else>
            <lazy-table-transaction-inputs :transaction-inputs="transactionInputsChannel(account.channel_code)" @single-view="getSingleView($event)" />
          </div>
        </b-tab>
      </b-tabs>
      <div v-if="transactionInputs.length !== 0">
        <b-button v-show="buttonFetchMore" variant="outline-primary" :disabled="$fetchState.pending" block @click="refresh">
          <b-spinner v-if="$fetchState.pending" small />
          <b-icon v-else icon="chevron-down" />
          Show More
        </b-button>
      </div>
    </div>

    <div v-else>
      <b-button variant="outline-info" @click="getTableView">
        <b-icon icon="arrow-left" /> Go Back
      </b-button>
      <hr class="my-3" />
      <lazy-container-transaction-input :transaction-input-public-id="transactionInputPublicId" />
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "OverviewTransactionInputs",

  async fetch() {
    if (
      this.transactionInputs.length === 0 ||
                this.sellerFirm.public_id !== this.$route.params.public_id
    ) {
      const { store } = this.$nuxt.context
      const params = {
        seller_firm_public_id: this.sellerFirm.public_id,
        page: 1,
      }
      await store.dispatch(
        "transaction_input/get_by_seller_firm_public_id",
        params
      )
    }
  },

  data() {
    return {
      buttonRemoveDisabled: false,
      buttonFetchMore: true,
      transactionInputTable: true,
      transactionInputPublicId: "",
    }
  },

  computed: {
    ...mapState({
      sellerFirm: (state) => state.seller_firm.seller_firm,
      transactionInputs: (state) =>
        state.transaction_input.transaction_inputs,
    }),

    currentPage() {
      return Math.trunc(this.transactionInputs.length / 50)
    },
  },

  methods: {
    getTableView() {
      console.log("getTableView")
      this.transactionInputPublicId = ""
      this.transactionInputTable = true
    },

    getSingleView(payload) {
      console.log("publicId:", payload)
      this.transactionInputPublicId = payload
      this.transactionInputTable = false
    },

    async refresh() {
      const { store } = this.$nuxt.context
      const tiLengthBefore = this.transactionInputs.length
      const params = {
        seller_firm_public_id: this.sellerFirm.public_id,
        page: this.currentPage + 1,
      }
      await store.dispatch(
        "transaction_input/get_by_seller_firm_public_id",
        params
      )
      const tiLengthAfter = this.transactionInputs.length

      if (tiLengthBefore === tiLengthAfter) {
        this.buttonFetchMore = false
      }
    },

    async removeAll() {
      this.buttonRemoveDisabled = true
      if (this.transactionInputs.length > 0) {
        try {
          await this.$store.dispatch("transaction_input/delete_all")
          await this.$store.dispatch(
            "seller_firm/get_by_public_id",
            this.sellerFirm.public_id
          )
          this.$router.push(
            `/clients/${this.sellerFirm.public_id}`
          )
        } catch (error) {
          this.$toast.error(error, { duration: 5000 })
          this.buttonRemoveDisabled = false
          return []
        }
      }
    },

    transactionInputsChannel(channelCode) {
      return this.transactionInputs.filter(
        (transaction_input) =>
          transaction_input.channel_code === channelCode
      )
    },
  },
}
</script>

<style>
</style>
