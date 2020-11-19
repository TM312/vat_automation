<template>
  <b-card title="Transactions">
    <div>
      <b-row>
        <b-col cols="auto">
          <b-pagination
            v-model="currentPage"
            :total-rows="transactionInputsFull.length"
            :per-page="perPage"
            aria-controls="table-transaction-inputs"
            pills
            hide-goto-end-buttons
            :disabled="transactionInputs.length===0"
          />
        </b-col>
        <b-col cols="auto" class="mr-auto">
          <span>
            <b-button-group class="ml-1">
              <b-button
                variant="outline-success"
                :pressed="null === channelCodeFilter"
                @click="setFilter()"
              >
                TOTAL
              </b-button>
              <b-button
                v-for="account in sellerFirm.accounts"
                :key="account.public_id"
                variant="outline-primary"
                :pressed="
                  account.channel_code === channelCodeFilter
                "
                @click="setFilter(account.channel_code)"
              >
                {{ account.channel_code }}
              </b-button>
            </b-button-group>
          </span>
        </b-col>
      </b-row>
    </div>
    <b-card v-if="transactionInputs.length === 0" class="text-center py-5">
      <b-card-text>
        <h5
          v-if="transactionInputs.length === 0"
          class="text-muted text-center m-5"
        >
          No Data Available Yet
        </h5>
      </b-card-text>
    </b-card>
    <div v-else>
      <table-transaction-inputs
        id="table-transaction-inputs"
        :transaction-inputs="transactionInputs"
        :client-public-id="sellerFirm.public_id"
        :per-page="perPage"
        :current-page="currentPage"
      />
    </div>
  </b-card>
</template>

<script>
import { mapState } from "vuex"

export default {
  layout: "tax-client",

  async fetch() {
    if (this.transactionInputs.length === 0) {
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
      perPage: 25,
      currentPage: 1,
      channelCodeFilter: null,
    }
  },

  computed: {
    ...mapState({
      sellerFirm: (state) => state.seller_firm.seller_firm,
      transactionInputsFull: (state) => state.transaction_input.transaction_inputs,
    }),

    transactionInputs() {
      return this.$store.getters["transaction_input/filterByChannelCode"](
        this.channelCodeFilter
      )
    },

    fetchMore() {
      if (!this.channelCodeFilter) {
        return (this.currentPage >= this.transactionInputsFull.length / this.perPage)
      } else {
        return false
      }
    },
  },

  watch: {
    fetchMore(newVal) {
      if (newVal) {
        this.refresh()
      }
    },
  },

  methods: {
    setFilter(channelCode) {
      if (channelCode == null) {
        this.channelCodeFilter = null
      } else {
        if (this.channelCodeFilter === channelCode) {
          this.channelCodeFilter = null
        } else {
          this.channelCodeFilter = channelCode
        }
      }
    },

    async refresh() {
      const { store } = this.$nuxt.context
      const params = {
        seller_firm_public_id: this.sellerFirm.public_id,
        page: this.currentPage/2 + 1,
      }
      await store.dispatch(
        "transaction_input/get_by_seller_firm_public_id",
        params
      )
    },
  },
}
</script>
