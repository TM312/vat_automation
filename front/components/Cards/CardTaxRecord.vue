<template>
  <div>
    <b-card border-variant="primary">
      <b-card-title>
        <b-row>
          <b-col cols="auto" class="mb-2">
            {{ taxJurisdiction.name }}
          </b-col>
          <b-col cols="auto ml-auto">
            <b-button variant="outline-danger" :disabled="buttonDisabled" @click="remove(taxRecord.public_id)">
              Delete
            </b-button>
          </b-col>
        </b-row>
      </b-card-title>
      <b-card-sub-title class="mb-2">
        {{ taxRecord.vatin }} | {{ $dateFns.format(taxRecord.start_date, 'MMMM dd, yyyy') }} – {{ $dateFns.format(taxRecord.end_date, 'MMMM dd, yyyy') }}
      </b-card-sub-title>

      <b-card-text>
        <b-row>
          <b-col cols="auto">
            <b>Taxable Turnover Amount:</b>
            <br />
            <b>Payable Vat Amount:</b>
          </b-col>
          <b-col>
            {{ Number.parseFloat(taxRecord.taxable_turnover_amount).toFixed(2) }} {{ taxRecord.currency_code }}
            <br />
            {{ Number.parseFloat(taxRecord.payable_vat_amount).toFixed(2) }} {{ taxRecord.currency_code }}
          </b-col>
        </b-row>
      </b-card-text>
    </b-card>
  </div>
</template>

<script>
import { mapState } from "vuex"

export default {
    name: 'CardTaxRecord',

    data() {
        return {
            buttonDisabled: false,


        }
    },

    computed: {
        ...mapState({
            taxRecord: state => state.tax_record.tax_record,
            countries: state => state.country.countries,
            currencies: state => state.currency.currencies
        }),


        taxJurisdiction() {
            return this.countries.find(country => country.code == this.taxRecord.tax_jurisdiction_code)
        },


    },

    methods: {
        async remove(taxRecordPublicId) {
            this.buttonDisabled = true
            try {
                await this.$store.dispatch("tax_record/delete_by_public_id", taxRecordPublicId)
                await this.$store.dispatch("seller_firm/get_by_public_id", this.taxRecord.seller_firm_public_id)
                this.$router.push(`/tax/clients/${this.taxRecord.seller_firm_public_id}`)

            } catch (error) {
                this.$toast.error(error, { duration: 5000 })
                this.buttonDisabled = false
                return []
            }
        }
    }


}
</script>

<style>

</style>
