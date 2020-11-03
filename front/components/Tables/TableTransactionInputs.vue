<template>
  <div>
    <b-pagination
      v-model="currentPage"
      :total-rows="transactionInputs.length"
      :per-page="perPage"
      aria-controls="table-transaction-inputs"
      pills
      class="my-3"
    />
    <b-table
      id="table-transaction-inputs"
      :fields="fieldsBundle"
      :items="transactionInputs"
      :per-page="perPage"
      :current-page="currentPage"
      hover
    >
      <template v-slot:cell(transaction_type_public_code)="data">
        <!-- <b-button
          v-if="data.item.public_id != $route.params.public_id"
          variant="link"
          @click="$emit('single-view', data.item.public_id)"
        >
          {{ data.value }}
        </b-button> -->
        <nuxt-link
          v-if="data.item.public_id != $route.params.public_id"
          :to="`/clients/${clientPublicId}/transactions/${data.item.public_id}`"
          exact
        >
          {{ data.value }}
        </nuxt-link>
        <span v-else>{{ data.value }}</span>
      </template>

      <template v-slot:cell(processed)="data" class="align-center">
        <b-icon
          v-if="data.value"
          icon="check-circle"
          variant="success"
        />
        <span v-else><button-validate-transaction-input
          :transaction-input-public-id="data.item.public_id"
        /></span>
      </template>

      <template v-slot:cell(sale_total_value_gross)="data">
        <span v-if="data.value === null"></span>
        <span v-else>{{ data.value }} {{ data.item.currency_code }}</span>
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
  </div>
</template>

<script>
export default {
  name: "TableTransactionInputs",

  props: {
    clientPublicId: {
      type: String,
      required: true,
    },

    transactionInputs: {
      type: [Array, Object],
      required: true,
    },
  },

  data() {
    return {
      perPage: 25,
      currentPage: 1,
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
          key: "marketplace",
          sortable: false,
        },
        {
          key: "item_quantity",
          label: "Quantity",
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
          sortable: false,
        },
      ],
    }
  },

  // methods: {
  //     singleView(publicId) {
  //         console.log('singleView public_id:', publicId) //!!!s
  //         this.$emit('single-view', publicId)
  //     }
  // }

  // },
  // methods: {
  //     codeToName(countryCode) {
  //         return this.countries.find(country => country.code == countryCode).name
  //     },

  // },
}
</script>

<style>
</style>
