<template>
  <b-card title="Base Data">
    <b-table-lite
      borderless
      fixed
      small
      :items="itemsDates"
      :fields="fieldsDates"
      class="mb-4"
    />
    <b-table-lite
      borderless
      fixed
      small
      :items="itemsCategory"
      :fields="fieldsCategory"
      class="mb-4"
    >
      <template v-slot:cell(value)="data">
        <span v-if="Array.isArray(data.value) === true">
          <span>{{ data.value[0] }} </span>
          <b-popover
            :target="`popover-vatin-${vatNumberByCountryCode}`"
            triggers="hover"
            placement="top"
            class="ml-2"
            :title="`${vatNumberByCountryCode.country_code}-${vatNumberByCountryCode.number}`"
          >
            <div>
              Valid:
              <b-icon
                :variant="
                  vatNumberByCountryCode.valid
                    ? 'success'
                    : 'danger'
                "
                :icon="
                  vatNumberByCountryCode.valid
                    ? 'check-circle'
                    : 'x-circle'
                "
              />
            </div>
            <div>
              Request Date:
              {{ vatNumberByCountryCode.request_date }}
            </div>
          </b-popover>
          <b-badge
            :id="`popover-vatin-${vatNumberByCountryCode}`"
            variant="secondary"
            class="ml-2"
          >
            {{ data.value[1] }}-{{ data.value[2] }}
          </b-badge>
        </span>
        <span v-else>{{ data.value }}</span>
      </template>
    </b-table-lite>

    <b-table-lite
      borderless
      fixed
      small
      :items="itemsLogistics"
      :fields="fieldsLogistics"
      class="mb-4"
    >
      <template v-slot:cell(category)="data">
        <span>
          {{ data.value[0] }}
          <b-icon icon="arrow-right" class="mx-2" variant="primary" />
          {{ data.value[1] }}
        </span>
      </template>
      <template v-slot:cell(value)="data">
        <span>
          {{ data.value[0] }}
          <b-icon icon="arrow-right" class="mx-2" variant="primary" />
          {{ data.value[1] }}
        </span>
      </template>
    </b-table-lite>

    <b-table-lite
      borderless
      fixed
      small
      :items="itemsTaxRates"
      :fields="fieldsTaxRates"
      class="mb-4"
    >
      <template v-slot:cell(value)="data">
        <span>{{
          Number.parseFloat(data.value[0] * 100).toFixed(1)
        }}%</span>
        <b-badge
          v-b-popover.hover.top="
            taxRateTypes.find((el) => el.code === data.value[1])[
              'description'
            ]
          "
          class="ml-2"
          :title="
            taxRateTypes.find((el) => el.code === data.value[1])[
              'name'
            ]
          "
          :variant="data.value[1] === 'S' ? 'primary' : 'success'"
        >
          {{
            taxRateTypes.find((el) => el.code === data.value[1])[
              "name"
            ]
          }}
        </b-badge>
      </template>
    </b-table-lite>
  </b-card>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "CardTransactionBaseData",
  props: {
    transaction: {
      type: [Array, Object],
      required: true,
    },
  },
  computed: {
    ...mapState({
      taxRateTypes: (state) => state.tax_rate_type.tax_rate_types,
    }),

    vatNumberByCountryCode() {
      return this.$store.getters["seller_firm/vatNumberByCountryCode"](
        this.transaction.tax_jurisdiction_code
      )
    },

    taxJurisdiction() {
      return this.$store.getters["country/countryNameByCode"](
        this.transaction.tax_jurisdiction_code
      )
    },
    itemsDates() {
      return [
        {
          date: "Tax Date",
          value: this.transaction.tax_date //this.$dateFns.format( this.transaction.tax_date, "MMMM, dd, yyyy" ),
        },
        {
          date: "Tax Calculation Date",
          value: this.transaction.tax_calculation_date //this.$dateFns.format( this.transaction.tax_calculation_date, "MMMM, dd, yyyy" ),
        },
      ]
    },

    fieldsDates() {
      return [
        { key: "date", label: "Dates" },
        { key: "value", label: "" },
      ]
    },

    itemsCategory() {
      return [
        {
          category: "Transaction Type",
          value: this.capitalize(this.transaction.type_code),
        },
        {
          category: "Tax Treatment",
          value: this.capitalize(this.transaction.tax_treatment_code),
        },
        {
          category: "Tax Jurisdiction",
          value: [
            this.taxJurisdiction,
            this.vatNumberByCountryCode.country_code,
            this.vatNumberByCountryCode.number,
          ],
        },
      ]
    },

    fieldsCategory() {
      return [
        { key: "category", label: "Categories" },
        { key: "value", label: "" },
      ]
    },

    itemsLogistics() {
      return [
        {
          category: ["Departure", "Arrival"],
          value: [
            this.transaction.departure_country_code,
            this.transaction.arrival_country_code,
          ],
        },
      ]
    },

    fieldsLogistics() {
      return [{ key: "logistics" }, { key: "value", label: "" }]
    },

    itemsTaxRates() {
      return [
        {
          tax_rate: "Item",
          value: [
            this.transaction.item_price_vat_rate,
            this.transaction.item_tax_rate_type_code,
          ],
        },
        {
          tax_rate: "Shipment",
          value: [
            this.transaction.shipment_price_vat_rate,
            this.transaction.shipment_tax_rate_type_code,
          ],
        },
        {
          tax_rate: "Gift Wrap",
          value: [
            this.transaction.gift_wrap_price_vat_rate,
            this.transaction.gift_wrap_tax_rate_type_code,
          ],
        },
      ]
    },

    fieldsTaxRates() {
      return [
        { key: "tax_rate", label: "Tax Rates" },
        { key: "value", label: "" },
      ]
    },
  },
}
</script>

<style>
</style>
