<template>
  <b-sidebar
    id="sidebar-transaction"
    title="Transaction Details"
    right
    shadow
    width="500px"
  >
    <div class="px-3 py-2">
      <p>
        Cras mattis consectetur purus sit amet fermentum. Cras justo
        odio, dapibus ac facilisis in, egestas eget quam. Morbi leo
        risus, porta ac consectetur ac, vestibulum at eros.
      </p>
    </div>
    <div class="mt-3">
      <sidebar-transaction-details :transaction="transaction" />
    </div>
    <b-button variant="primary">
      Details
    </b-button>
  </b-sidebar>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "SidebarTransaction",
  props: {
    transactionPublicId: {
      type: String,
      required: true,
    },
    fetchTransaction: {
      type: Boolean,
      required: true,
    },
  },

  computed: {
    ...mapState({
      transaction: (state) => state.transaction.transaction,
    }),
  },

  watch: {
    /*eslint-disable */
            async fetchTransaction(newVal) {
                if (newVal) {
                    if (
                        this.transaction.length === 0 ||
                        this.transaction.public_id !== this.transactionPublicId
                    ) {
                        const { store } = this.$nuxt.context;
                        await store.dispatch(
                            "transaction/get_by_public_id",
                            this.transactionPublicId
                        );
                    }
                }
            },
            /*eslint-disable */
        },
    };
</script>

<style>
</style>
