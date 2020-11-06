<template>
  <b-row cols="2" cols-md="3" cols-lg="4">
    <!-- <h1>orderedBundle: {{ orderedBundle }}</h1> -->
    <b-col
      v-for="(transactionInput, index) in orderedBundle"
      :key="transactionInput.public_id"
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
                v-if="
                  transactionInputPublicId !==
                    transactionInput.public_id
                "
                size="sm"
                variant="outline-primary"
                :to="`/clients/${clientPublicId}/transactions/${transactionInput.public_id}`"
              >
                Details
              </b-button>
            </b-col>
          </b-row>
        </b-card-title>
        <b-card-sub-title class="mb-3">
          <span>{{ transactionInput.complete_date }}</span>
          <span>{{ index }}</span>
          <!-- <span v-if="index > 0">{{ $dateFns.formatDistance(new Date(transactionInput.complete_date), new Date(transactionInput.complete_date)) }}</span> -->

          <span v-if="index > 0" class="px-2">{{ (transactionInputsBundle[index-1].complete_date > transactionInput.complete_date) }}</span>
          <span v-if="index > 0" class="px-2">{{
            transactionInputsBundle[index - 1].complete_date
          }}</span>
        </b-card-sub-title>
        <b-card-text class="font-weight-bold">
          <b-row class="text-center">
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
                {{ transactionInput.currency_code }}</span>
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
    clientPublicId: {
      type: String,
      required: true,
    },

    transactionInputPublicId: {
      type: String,
      required: true,
    },
  },

  computed: {
    ...mapState({
      transactionInputsBundle: (state) => state.transaction_input.transaction_inputs_bundle
    }),
    orderedBundle() {
      var orderedTransactionInputsBundle = this.transactionInputsBundle
      return orderedTransactionInputsBundle.sort((a,b) => b.complete_date - a.complete_date)
    }
  },
  methods: {
    borderVariant(publicId) {
      return publicId === this.transactionInputPublicId
        ? "primary"
        : "secondary"
    },
  },
}
</script>

<style>
</style>
