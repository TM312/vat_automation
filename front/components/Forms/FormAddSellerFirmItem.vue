<template>
  <b-card bg-variant="white">
    <b-form-group
      label-cols-lg="3"
      label="New Item"
      label-size="lg"
      label-class="font-weight-bold pt-0"
      class="mb-2"
    >
      <b-form-group
        label-cols-sm="3"
        label-align-sm="right"
        label-for="brand_name"
        label="Brand Name"
      >
        <b-form-input
          id="brand_name"
          v-model="payload.brand_name"
          type="text"
          class="mt-1"
        />
      </b-form-group>

      <b-form-group
        label-cols-sm="3"
        label-align-sm="right"
        label-for="name"
        label="Name"
      >
        <b-form-input
          id="name"
          v-model="payload.name"
          type="text"
          class="mt-1"
        />
      </b-form-group>


      <b-form-group
        label-cols-sm="3"
        label-align-sm="right"
        label-for="sku"
        label="SKU"
      >
        <b-form-input
          id="sku"
          v-model="payload.sku"
          type="text"
          class="mt-1"
        />
      </b-form-group>

      <b-form-group
        label-cols-sm="3"
        label-align-sm="right"
        label-for="ean"
        label="EAN"
      >
        <b-form-input
          id="ean"
          v-model="payload.ean"
          type="text"
          class="mt-1"
        />
      </b-form-group>

      <b-form-group
        label-cols-sm="3"
        label-align-sm="right"
        label-for="asin"
        label="ASIN"
      >
        <b-form-input
          id="asin"
          v-model="payload.asin"
          type="text"
          class="mt-1"
        />
      </b-form-group>


      <b-form-group
        label-cols-sm="3"
        label-align-sm="right"
        label-for="fnsku"
        label="FNSKU"
      >
        <b-form-input
          id="fnsku"
          v-model="payload.fnsku"
          type="text"
          class="mt-1"
        />
      </b-form-group>

      <b-form-group
        label-cols-sm="3"
        label-align-sm="right"
        label-for="weight_kg"
        label="Weight [in kg]"
      >
        <b-form-input
          id="weight_kg"
          v-model="payload.weight_kg"
          type="number"
          step="0.01"
          class="mt-1"
        />
      </b-form-group>

      <b-form-group
        label-cols-sm="3"
        label-align-sm="right"
        label-for="unit_cost_price_net"
        label="Unit Cost Price Net"
      >
        <b-form-input
          id="unit_cost_price_net"
          v-model="payload.unit_cost_price_net"
          type="number"
          step="0.01"
          class="mt-1"
        />
      </b-form-group>

      <b-form-group
        label-cols-sm="3"
        label-align-sm="right"
        label-for="unit_cost_price_currency_code"
        label="Unit Cost Price Currency"
      >
        <b-form-select v-if="$fetchState.pending" id="unit_cost_price_currency_code" disabled />
        <b-form-select
          v-else
          id="unit_cost_price_currency_code"
          v-model="payload.unit_cost_price_currency_code"
          :options="optionsUnitCostPriceCurrencyCodes"
        />
      </b-form-group>

      <b-form-group
        label-cols-sm="3"
        label-align-sm="right"
        label-for="valid_from"
        label="Valid From"
      >
        <b-form-datepicker
          id="valid_from"
          v-model="payload.valid_from"
        />
      </b-form-group>

      <b-form-group
        label-cols-sm="3"
        label-align-sm="right"
        label-for="valid_to"
        invalid-feedback="'Valid From' needs to predate 'Valid To'"
        :state="validation_valid_to"
        label="Valid To"
        description="If you do not pass a final validity date, it will be considered valid until updated."
      >
        <b-form-datepicker
          id="valid_to"
          v-model="payload.valid_to"
          :state="validation_valid_to"
        />
      </b-form-group>



      <b-form-group
        label-cols-sm="3"
        label-align-sm="right"
        label-for="tax_code_code"
        label="Tax Code"
      >
        <b-form-select v-if="$fetchState.pending" id="tax_code_code" disabled />
        <b-form-select
          v-else
          id="tax_code_code"
          v-model="payload.tax_code_code"
          :options="optionsTaxCodes"
        />
      </b-form-group>
    </b-form-group>


    <b-button
      variant="primary"
      :disabled="validation_submit"
      block
      @click="submitPayload()"
    >
      <b-icon icon="box-arrow-in-up" /> Add New Item
    </b-button>
  </b-card>
</template>

<script>
    import { mapState } from "vuex"

    export default {
        name: 'FormAddSellerFirmItem',

        async fetch() {
            const { store } = this.$nuxt.context
            await store.dispatch("currency/get_all")
            await store.dispatch("tax_code/get_all")
        },

        data() {
            return {
                payload: {
                        brand_name: null,
                        name: null,
                        sku: null,
                        ean: null,
                        asin: null,
                        fnsku: null,
                        weight_kg: null,
                        unit_cost_price_currency_code: null,
                        unit_cost_price_net: null,
                        valid_from: null,
                        valid_to: null,
                        tax_code_code: null
                    },
            }
        },

        computed: {
            ...mapState({
                currencies: state => state.currency.currencies,
                tax_code_codes: state => state.tax_code.tax_codes
            }),

            optionsUnitCostPriceCurrencyCodes() {
                let options = this.currencies.map(currency => {
                    let properties = {
                        value: currency.code,
                        text: currency.name
                    }
                    return properties
                })
                return options
            },

            optionsTaxCodes() {
                let options = this.tax_code_codes.map(tax_code => {
                    let properties = {
                        value: tax_code.code,
                        text: tax_code.code
                    }
                    return properties
                })
                return options
            },

            validation_valid_to() {
                if (this.payload.valid_to !== null) {
                    return this.payload.valid_from <= this.payload.valid_to
                } else {
                    return null
                }
            },

            validation_submit() {
                if (
                    this.payload.sku !== null &&
                    this.payload.tax_code_code !== null &&
                    this.payload.tax_code_code !== '' &&
                    this.payload.unit_cost_price_currency_code !== null &&
                    this.payload.unit_cost_price_currency_code !== '' &&
                    this.payload.valid_from !== null &&
                    this.validation_valid_to !== false
                ) {
                    return false
                } else {
                    return true
                }
            }
        },

        methods: {


            async submitPayload() {
                try {
                    // removes all empty values from object : https://stackoverflow.com/questions/23774231/how-do-i-remove-all-null-and-empty-string-values-from-a-json-object
                    Object.keys(this.payload).forEach(k => (!this.payload[k] && this.payload[k] !== undefined) && delete this.payload[k])

                    await this.create_by_seller_firm_public_id()

                    this.payload.ean = null
                    this.payload.asin = null
                    this.payload.fnsku = null
                    this.payload.weight_kg = null
                    this.payload.unit_cost_price_net = null

                    console.log('this.payload after reset: ', this.payload)

                    await this.$store.dispatch(
                        "seller_firm/get_by_public_id",
                        this.$route.params.public_id
                    )
                    this.$emit('flash')
                    await this.$toast.success('New item successfully added.', {
                        duration: 5000
                    })
                } catch (error) {
                    this.$toast.error(error, { duration: 5000 })
                }
            },

            async create_by_seller_firm_public_id() {
                const data_array = [this.$route.params.public_id, this.payload]

                await this.$store.dispatch(
                    "item/create_by_seller_firm_public_id",
                    data_array
                )
            },
        }
    }
</script>

<style>

</style>
