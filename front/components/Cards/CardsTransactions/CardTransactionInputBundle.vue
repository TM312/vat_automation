<template>
  <b-row cols="2" :cols-xl="showcase ? 3 : 4">
    <!-- <h1>orderedBundle: {{ orderedBundle }}</h1> -->
    <b-col
      v-for="transactionInput in transactionInputsBundle"
      :key="transactionInput.public_id"
      class="py-3"
    >
      <b-card
        :border-variant="borderVariant(transactionInput.public_id)"
        class="h-100"
      >
        <b-card-title>
          <b-row>
            <b-col cols="auto">
              {{ transactionInput.transaction_type_public_code }}
            </b-col>
            <b-col cols="auto" class="ml-auto">
              <b-button
                v-if="!showcase && transactionInputPublicId !== transactionInput.public_id"
                size="sm"
                variant="outline-primary"
                :to="`/${sellerFirmPublicId}/transactions/${transactionInput.public_id}`"
              >
                Details
              </b-button>

              <b-button
                v-else-if="showcase && transactionInputPublicId !== transactionInput.public_id"
                size="sm"
                pill
                variant="outline-primary"
                @click="fetchTransactionInput(transactionInput.public_id)"
              >
                Details
              </b-button>
            </b-col>
          </b-row>
        </b-card-title>
        <b-card-sub-title class="mb-3">
          <span>{{ transactionInput.complete_date }}</span>
          <!-- <span>{{ index }}</span> -->
          <!-- <span v-if="index > 0">{{ $dateFns.formatDistance(new Date(transactionInput.complete_date), new Date(transactionInput.complete_date)) }}</span> -->

          <!-- <span v-if="index > 0" class="px-2">{{ (transactionInputsBundle[index-1].complete_date > transactionInput.complete_date) }}</span>
          <span v-if="index > 0" class="px-2">{{
            transactionInputsBundle[index - 1].complete_date
          }}</span> -->
        </b-card-sub-title>
        <b-card-text class="text-info">
          <b-row align-h="between">
            <b-col>
              <span
                v-if="transactionInput.arrival_country_code"
              >
                {{ transactionInput.departure_country_code }}
                <span class="px-1"><b-icon icon="arrow-right" /></span>
                {{ transactionInput.arrival_country_code }}
              </span>
            </b-col>
            <b-col>
              <span>QTY: {{ transactionInput.item_quantity }}</span>
            </b-col>
            <b-col>
              <span>{{ transactionInput.sale_total_value_gross }}
                {{ transactionInput.currency_code === 'EUR' ? '€' : transactionInput.currency_code }}</span>
            </b-col>
          </b-row>
        </b-card-text>

        <b-card-text>
          <span class="text-muted">
            <small>{{ transactionInput.channel_code }}</small>
            <small class="mx-1">|</small>
            <span v-if="transactionInput.marketplace">
              <small>{{ transactionInput.marketplace }}</small>
              <small class="mx-1">|</small>
            </span>
            <small class="ml">{{
              transactionInput.item_sku
            }}</small>
          </span>
        </b-card-text>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "CardTransactionInputBundle",

  props: {
    sellerFirmPublicId: {
      type: String,
      required: true,
    },

    transactionInputPublicId: {
      type: String,
      required: true,
    },

    showcase: {
      type: Boolean,
      required: false,
      default: false
    }
  },

  computed: {
    ...mapState({
      transactionInputsBundle: (state) => state.transaction_input.transaction_inputs_bundle,
      transactionInput: (state) => state.transaction_input.transaction_input
    }),
    // orderedBundle() {
    //   var orderedTransactionInputsBundle = this.transactionInputsBundle
    //   return orderedTransactionInputsBundle.sort((a,b) => b.complete_date - a.complete_date)
    // }
  },
  methods: {
    borderVariant(publicId) {
      return publicId === this.transactionInputPublicId ? "primary" : "secondary"
    },

    async fetchTransactionInput(transactionInputPublicId) {
      if (Object.keys(this.transactionInput).length === 0 || this.transactionInput.public_id !== transactionInputPublicId) {
        const { store } = this.$nuxt.context
        await store.dispatch("transaction_input/get_by_public_id", transactionInputPublicId)
      }
    },
  },
}
</script>

<style>
</style>
