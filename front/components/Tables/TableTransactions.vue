<template>
  <div>
    <h6>transactionPublicId: {{ transactionPublicId }}</h6>
    <br />
    <sidebar-transaction
      :transaction-public-id="transactionPublicId"
    />
    <h5 v-if="transactions.length === 0" class="text-muted text-center m-5">
      There are no tax related processes of this tax treatment.
    </h5>
    <b-table v-else :fields="fields" :items="transactions" hover>
      <!-- <template v-slot:cell(type_code)="data">
        <nuxt-link :to="`/transactions/${data.item.transaction_input_public_id}`">
            {{ data.value }}
        </nuxt-link>
        </template> -->

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

      <template #cell(type_code)="data">
        <b-button
          v-b-toggle.sidebar-transaction
          variant="link"
          @click="setSidebar(data.item.public_id)"
        >
          {{ capitalize(data.value) }}
        </b-button>
      </template>

      <template #cell(departure_to_arrival)="data">
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

      <template #cell(tax_jurisdiction_code)="data">
        {{ $store.getters["country/countryNameByCode"](data.value) }}
      </template>

      <!-- <template #cell(details)="row">
                <b-button size="sm" @click="row.toggleDetails">
                Details
                </b-button>
            </template>

            <template #row-details>
                <p>hello</p>
                <b-card>
                <ul>
                    <li v-for="(value, key) in row.item" :key="key">
                    {{ key }}: {{ value }}
                    </li>
                </ul>
                </b-card>
            </b-table>
        </div>
        </template> -->
    </b-table>

    <b-button
      v-if="buttonShow"
      variant="outline-primary"
      :disabled="$fetchState.pending"
      block
      @click="refresh"
    >
      <b-spinner v-if="$fetchState.pending" small />
      <b-icon v-else icon="chevron-down" />
      Show More
    </b-button>
  </div>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "TableTransactions",

  props: {
    taxTreatmentCode: {
      type: String,
      required: true,
    },
  },

  async fetch() {
    if (this.transactions.length === 0 && !this.fetched) {
      console.log(
        "this.transactions.length === 0:",
        this.transactions.length === 0
      )
      const { store } = this.$nuxt.context
      const params = {
        tax_record_public_id: this.taxRecord.public_id,
        tax_treatment_code: this.taxTreatmentCode,
        page: 1,
      }
      await store.dispatch(
        "transaction/get_by_tax_record_tax_treatment",
        params
      )
    }
  },

  data() {
    return {
      buttonShow: true,
      transactionPublicId: "",

      fields: [
        {
          key: "tax_date",
          sortable: false,
        },
        // {
        //   key: "transaction_input_given_id",
        //   label: "Given ID",
        //   sortable: false,
        // },
        // {
        //   key: "transaction_input_activity_id",
        //   label: "Activity ID",
        //   sortable: false,
        // },
        {
          key: "type_code",
          sortable: false,
        },
        {
          key: "departure_to_arrival",
          sortable: false,
        },
        {
          key: "tax_jurisdiction_code",
          label: "Tax Jurisdiction",
          sortable: false,
        }
      ],
    }
  },

  computed: {
    ...mapState({
      taxRecord: (state) => state.tax_record.tax_record,
    }),
    transactions() {
      return this.$store.getters[
        "transaction/getTransactionsByTaxTreatmentCode"
      ](this.taxTreatmentCode)
    },

    currentPage() {
      return Math.trunc(this.transactions.length / 50) //needs to match with api config transactions_per_page
    },
  },

  watch: {
    /*eslint-disable */
            transactions(newVal, oldVal) {
                if (newVal.length < oldVal.length + 50) {
                    this.buttonShow = false;
                }
            },
        },

        methods: {
            async refresh() {
                const { store } = this.$nuxt.context;
                const params = {
                    tax_record_public_id: this.taxRecord.public_id,
                    tax_treatment_code: this.taxTreatmentCode,
                    page: this.currentPage + 1,
                };
                await store.dispatch(
                    "transaction/get_by_tax_record_tax_treatment",
                    params
                );
            },
            setSidebar(transactionPublicId) {
                (this.transactionPublicId = transactionPublicId)
            },
        },
    };
</script>

<style>
</style>
