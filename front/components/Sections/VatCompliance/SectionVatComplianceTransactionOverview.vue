<template>
  <section id="vat-compliance-transaction-overview" class="py-5">
    <b-container>
      <h6 class="text-primary">
        Transaction Overview
      </h6>
      <h2>Unparalleled Levels Of Detail</h2>
      <p class="text-dark lead my-2">
        <span>Get in-depth insights into the VAT implications of
          each transaction.</span>
        <span v-if="Object.keys(sellerFirm).length !== 0">In the transaction panel you get a list of your
          transactions. Click on the transaction type field to
          get the details of a single transactions.</span>
      </p>
    </b-container>
    <b-container v-if="Object.keys(sellerFirm).length === 0" class="py-3">
      <card-sample
        style="max-width: 30rem"
        :page="currentPage"
        :total="total"
        primer="Bond Store Ltd"
        description="Click on the 'Upload' button at the top of the page to retreive all transaction data."
      />
    </b-container>
    <b-container v-else class="py-3" fluid style="max-width: 100rem">
      <card-transaction-inputs-showcase id="neuphormism" />
      <b-collapse id="collapse-transaction-input" class="py-3 mt-2">
        <b-card id="neuphormism">
          <b-card-text>
            <card-transaction-input-bundle
              v-if="Object.keys(transactionInput).length !== 0"
              :transaction-input-public-id="transactionInput.public_id"
              :client-public-id="sellerFirm.public_id"
              showcase
            />
            <div class="my-2">
              <small class="text-muted">
                Above you can find the bundle of related
                transactions. An typical case for related
                transactions are the <b>returns</b> of goods. If
                a customer returns a good, it will relate to a
                preceding <b>Sale</b> transaction and typically
                trigger a further <b>Refund</b> transaction.
                Here you find all related transactions in one
                place. Click on <b>Details</b> to jump directly
                to the respective transaction.
              </small>
            </div>

            <b-tabs class="mt-3">
              <b-tab title="Input File" active class="pt-3">
                <card-transaction-input
                  v-if="Object.keys(transactionInput).length !==0"
                  id="file"
                  showcase
                />
                <div class="mt-2">
                  <small class="text-muted">This is the original information as
                    provided by Amazon. You will notice that
                    in most cases not all fields of
                    information are filled. To indicate this
                    we display this
                    <b-icon
                      icon="exclamation-triangle"
                      variant="warning"
                    />
                    icon.
                  </small>
                </div>
              </b-tab>

              <b-tab title="Tax Processes" class="pt-3">
                <view-transactions
                  v-if="
                    Object.keys(transactionInput).length !==
                      0
                  "
                  :transactions="
                    transactionInput.transactions
                  "
                />
                <div class="mt-2">
                  <small class="text-muted">
                    Here you can see how this particular
                    transaction was processed. Depending its
                    type a single transaction may have
                    multiple tax implications.
                  </small>
                </div>
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
  name: "SectionVatComplianceTransactionOverview",
  data() {
    return {
      currentPage: 1,
      total: 1,
    }
  },

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
