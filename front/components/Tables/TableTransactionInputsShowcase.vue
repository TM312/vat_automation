<template>
  <b-table
    :fields="fieldsBundle"
    :items="transactionInputs"
    :per-page="perPage"
    :current-page="currentPage"
    hover
    class="mt-3"
  >
    <template v-slot:cell(transaction_type_public_code)="data">
      <b-button
        size="sm"
        pill
        variant="link"
        @click="fetchTransactionInput(data.item.public_id)"
      >
        {{ data.value }}
      </b-button>
    </template>

    <template v-slot:cell(processed)="data" class="align-center">
      <span v-if="data.value">
        <b-icon
          v-b-popover.hover.top="'This transaction was successfully processed.'"
          icon="check-circle"
          variant="success"
        />
      </span>
      <span v-else><button-validate-transaction-input
        :transaction-input-public-id="data.item.public_id"
      /></span>
    </template>

    <template v-slot:cell(sale_total_value_gross)="data">
      <span v-if="data.value === null"></span>
      <span v-else>{{ data.value }} {{ data.item.currency_code === 'EUR' ? '€' : data.item.currency_code }}</span>
    </template>

    <template v-slot:head(departure_to_arrival)>
      <b-row no-gutters class="justify-content-md-center">
        <b-col class="text-right">
          Departure
        </b-col>
        <b-col cols="2" class="text-center">
          <b-icon icon="arrow-right" />
        </b-col>
        <b-col class="text-left">
          Arrival
        </b-col>
      </b-row>
    </template>

    <template v-slot:cell(departure_to_arrival)="data">
      <b-row no-gutters class="justify-content-md-center">
        <b-col class="text-right">
          {{ data.item.departure_country_code }}
        </b-col>
        <b-col
          v-if="
            data.item.departure_country_code ||
              data.item.arrival_country_code
          "
          cols="2"
          class="text-center"
        >
          <b-icon icon="arrow-right" />
        </b-col>
        <b-col class="text-left">
          {{ data.item.arrival_country_code }}
        </b-col>
      </b-row>
    </template>
  </b-table>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: "TableTransactionInputs",

  props: {
    sellerFirmPublicId: {
      type: String,
      required: true,
    },

    transactionInputs: {
      type: [Array, Object],
      required: true,
    },

    perPage: {
      type: Number,
      required: true
    },

    currentPage: {
      type: Number,
      required: true
    },
  },

  data() {
    return {

      fieldsBundle: [
        {
          key: "complete_date",
          sortable: false,
        },
        {
          key: "transaction_type_public_code",
          label: "Public Type",
          sortable: false,
          formatter: (value) => {
            return this.capitalize(value)
          },
        },
        {
          key: "item_sku",
          label: "SKU",
          sortable: false,
        },
        {
          key: "given_id",
          label: "Transaction ID",
          sortable: false,
        },
        {
          key: "item_quantity",
          label: "Qty",
          sortable: false,
        },
        {
          key: "sale_total_value_gross",
          label: "Total Value Gross",
          formatter: (value) => {
            return value
              ? Number.parseFloat(value).toFixed(2)
              : null
          },
          sortable: false,
        },
        {
          key: "departure_to_arrival",
          sortable: false,
        },

        {
          key: "processed",
          label: '',
          sortable: false,
        },
      ],
    }
  },

  computed: {
    ...mapState({
      transactionInput: state => state.transaction_input.transaction_input
    })
  },

  methods: {
    async fetchTransactionInput(transactionInputPublicId) {
      this.$root.$emit(
        "bv::toggle::collapse",
        "collapse-transaction-input"
      )
      if (Object.keys(this.transactionInput).length === 0 || this.transactionInput.public_id !== transactionInputPublicId) {
        const { store } = this.$nuxt.context
        await store.dispatch("transaction_input/get_by_public_id", transactionInputPublicId)
      }
    },
  }
}
</script>

<style>
</style>
