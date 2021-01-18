<template>
  <div>
    <b-card
      :title="
        $store.getters['country/countryNameByCode'](
          taxRecord.tax_jurisdiction_code
        )
      "
    >
      <b-card-sub-title class="mb-2">
        {{ $dateFns.format(taxRecord.start_date, "MMMM dd, yyyy") }} –
        {{ $dateFns.format(taxRecord.end_date, "MMMM dd, yyyy") }}
      </b-card-sub-title>

      <b-card-text>
        <b-row>
          <b-col cols="auto">
            <b>Taxable Turnover Amount:</b>
            <br />
            <b>Payable Vat Amount:</b>
          </b-col>
          <b-col>
            {{ Number.parseFloat(taxRecord.taxable_turnover_amount).toFixed(2) }}
            {{ taxRecord.currency_code === 'EUR' ? '€' : taxRecord.currency_code }}
            <br />
            {{ Number.parseFloat(taxRecord.payable_vat_amount).toFixed(2) }}
            {{ taxRecord.currency_code === 'EUR' ? '€' : taxRecord.currency_code }}
          </b-col>
        </b-row>
      </b-card-text>
      <b-card-text class="mt-3">
        <nuxt-link
          v-if="!showcase"
          :to="`/tax-records/${taxRecord.public_id}`"
          exact
        >
          Details
        </nuxt-link>
        <b-button
          v-else
          size="sm"
          pill
          variant="outline-primary"
          @click="fetchTaxRecord()"
          @mouseover="buttonHover = true"
          @mouseleave="buttonHover = false"
        >
          Details
          <b-icon
            :icon="
              buttonHover ? 'arrow-right-short' : 'chevron-right'
            "
            class="ml-1"
          />
        </b-button>
      </b-card-text>
    </b-card>
  </div>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "CardTaxRecordShort",

  props: {
    taxRecord: {
      type: [Array, Object],
      required: true,
    },
    sellerFirmPublicId: {
      type: String,
      required: true,
    },
    showcase: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  data() {
    return {
      buttonHover: false,
    }
  },

  computed: {
    ...mapState({
      taxRecordFull: (state) => state.tax_record.tax_record,
    }),
  },

  methods: {
    async fetchTaxRecord() {
      this.$root.$emit(
        "bv::toggle::collapse",
        "collapse-tax-record-tables"
      )
      if (
        this.taxRecordFull.length === 0 ||
                    this.taxRecordFull.public_id !== this.taxRecord.public_id
      ) {
        const { store } = this.$nuxt.context
        await store.dispatch(
          "tax_record/get_by_public_id",
          this.taxRecord.public_id
        )
      }
    },
  },
}
</script>
