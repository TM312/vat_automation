<template>
  <b-card :title="taxJurisdictionName">
    <b-card-sub-title class="mb-2">
      {{ $dateFns.format(taxRecord.start_date, 'MMMM dd, yyyy') }} – {{ $dateFns.format(taxRecord.end_date, 'MMMM dd, yyyy') }}
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

      <b-button variant="link" class="mt-2 pl-0" @click="$emit('single-view', taxRecord.public_id)">
        Details
      </b-button>
    </b-card-text>
  </b-card>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'CardTaxRecordShort',
  // eslint-disable-next-line
        props: { taxRecord: { type: [Array, Object] } },

  computed: {
    ...mapState({
      countries: state => state.country.countries
    }),

    taxJurisdictionName() {
      if (this.countries.length !== 0) {
        return this.countries.find(country => country.code == this.taxRecord.tax_jurisdiction_code).name
      } else {
        return null
      }
    }
  },
}
</script>
