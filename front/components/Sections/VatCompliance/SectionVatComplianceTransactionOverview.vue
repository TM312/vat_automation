<template>
  <section id="vat-compliance-transaction-overview" class="py-5">
    <b-container>
      <h6 class="text-primary">
        Step 3
      </h6>
      <h1>Transaction Overview</h1>
      <p class="lead my-2">
        Get unparalleled insights by reviewing the processing of each
        individual transaction.
      </p>
    </b-container>
    <b-container fluid style="max-width: 100rem">
      <card-transaction-inputs-showcase id="neuphormism" class="my-3" />
      <b-collapse id="collapse-transaction-input" class="py-3 mt-2">
        <b-card id="neuphormism">
          <b-card-title>
            <b-row>
              <b-col cols="auto" class="ml-auto">
                <b-button size="sm" variant="outline-danger" @click="$root.$emit('bv::toggle::collapse', 'collapse-transaction-input')">
                  <b-icon icon="x" />
                </b-button>
              </b-col>
            </b-row>
          </b-card-title>
          <b-card-text>
            <card-transaction-input-bundle
              v-if="Object.keys(transactionInput).length !== 0"
              :transaction-input-public-id="transactionInput.public_id"
              :client-public-id="sellerFirm.public_id"
              showcase
            />

            <b-tabs class="mt-3">
              <b-tab title="Input File" active>
                <card-transaction-input
                  v-if="Object.keys(transactionInput).length !== 0"
                  id="file"
                  showcase
                />
              </b-tab>

              <b-tab title="Tax Processes">
                <view-transactions
                  v-if="Object.keys(transactionInput).length !== 0"
                  :transactions="transactionInput.transactions"
                />
              </b-tab>
            </b-tabs>
          </b-card-text>
        </b-card>
      </b-collapse>
    </b-container>
  </section>
</template>

<script>
import { mapState } from "vuex"

export default {
  computed: {
    ...mapState({
      sellerFirm: (state) => state.seller_firm.seller_firm,
      transactionInput: (state) =>
        state.transaction_input.transaction_input,
    }),
  },
}
</script>

<style scoped>
    #neuphormism {
        border-radius: 5px;
        box-shadow: 6px 6px 12px #bdbcbc, -6px -6px 12px #ffffff !important;
    }
</style>
