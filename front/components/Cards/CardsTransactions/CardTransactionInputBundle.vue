<template>
  <b-row cols="2" cols-md="3" cols-lg="4">
    <b-col v-for="(transactionInput, index) in transactionInputsBundle" :key="transactionInput.public_id">
      <b-card
        :title="transactionInput.transaction_type_public_code"
        :border-variant="borderVariant(transactionInput.public_id)"
      >
        <b-card-sub-title class="mb-3">
          <span>{{ transactionInput.complete_date }}</span>
          <!-- <span>{{ $dateFns.formatDistance(transactionInput.complete_date, transactionInput.complete_date) }}</span> -->

          <span v-if="index > 0" class="px-2">{{ (transactionInputsBundle[index-1].complete_date - transactionInput.complete_date) }}</span>
        </b-card-sub-title>
        <b-card-text class="text-primary">
          <span v-if="transactionInput.arrival_country_code">
            {{ transactionInput.departure_country_code }}
            <span class="px-1"><b-icon icon="arrow-right" /></span>
            {{ transactionInput.arrival_country_code }}
          </span>
        </b-card-text>
        <b-card-text class="text-muted">
          <span>
            <small>{{ transactionInput.channel_code }}</small>
            <small class="mx-1">|</small>
            <span v-if="transactionInput.marketplace">
              <small>{{ transactionInput.marketplace }}</small>
              <small class="mx-1">|</small>
            </span>
            <small class="ml">{{ transactionInput.item_sku }}</small>
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
    transactionInputPublicId: {
      type: String,
      required: true
    }
  },

  computed: {
    ...mapState({
      transactionInputsBundle: (state) =>
        state.transaction_input.transaction_inputs_bundle,
    }),
  },
  methods: {
    borderVariant(publicId) {
      return publicId === this.transactionInputPublicId ? 'primary' : 'secondary'
    }
  },
}
</script>

<style>
</style>
