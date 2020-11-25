<template>
  <b-card bg-variant="white" lg="6" xl="4" style="max-width: 80rem">
    <b-form-group
      label-cols-lg="2"
      label="New Tax Record"
      label-size="lg"
      label-class="font-weight-bold pt-0"
      class="mb-2"
    >
      <b-form-group
        label-cols-sm="3"
        label-align-sm="right"
        label="Tax Jurisdiction"
      >
        <b-form-select
          id="tax_jurisdiction_code"
          v-model="payload.tax_jurisdiction_code"
          :options="optionsCountryCode"
          required
        />
      </b-form-group>


      <b-form-group
        v-show="!!payload.tax_jurisdiction_code"
        label-cols-sm="3"
        label-align-sm="right"
        label="Validity"
      >
        <!-- year selection -->
        <b-row class="mb-2">
          <b-col>
            <b-button variant="outline-primary" :pressed="yearString === currentYearString" block @click="setYear('current')">
              {{ currentYearString }}
            </b-button>
          </b-col>
          <b-col>
            <b-button variant="outline-primary" :pressed="yearString === currentYearString - 1" block @click="setYear('past')">
              {{ currentYearString - 1 }}
            </b-button>
          </b-col>
        </b-row>

        <!-- in-year selection by quarters -->
        <b-row v-show="!!yearString" cols="1" cols-md="2" cols-lg="4">
          <b-col class="mb-2">
            <b-button :disabled="test('Q1')" :variant="test('Q1') ? 'outline-secondary' : 'outline-primary'" :pressed="selectedTimePeriod == 'Q1'" block @click="setQ(1)">
              Q1
            </b-button>
          </b-col>
          <b-col class="mb-2">
            <b-button :disabled="test('Q2')" :variant="test('Q2') ? 'outline-secondary' : 'outline-primary'" :pressed="selectedTimePeriod == 'Q2'" block @click="setQ(2)">
              Q2
            </b-button>
          </b-col>
          <b-col class="mb-2">
            <b-button :disabled="test('Q3')" :variant="test('Q3') ? 'outline-secondary' : 'outline-primary'" :pressed="selectedTimePeriod == 'Q3'" block @click="setQ(3)">
              Q3
            </b-button>
          </b-col>
          <b-col class="mb-2">
            <b-button :disabled="test('Q4')" :variant="test('Q4') ? 'outline-secondary' : 'outline-primary'" :pressed="selectedTimePeriod == 'Q4'" block @click="setQ(4)">
              Q4
            </b-button>
          </b-col>
        </b-row>

        <!-- in-year selection by months -->
        <b-row v-show="!!yearString" class="mt-2" cols="1" cols-md="3" cols-lg="4" cols-xl="6">
          <b-col class="mb-2">
            <b-button :disabled="test(0)" :variant="test(0) ? 'outline-secondary' : 'outline-primary'" :pressed="selectedTimePeriod == 'Jan'" block @click="setM(0)">
              Jan
            </b-button>
          </b-col>
          <b-col class="mb-2">
            <b-button :disabled="test(1)" :variant="test(1) ? 'outline-secondary' : 'outline-primary'" :pressed="selectedTimePeriod == 'Feb'" block @click="setM(1)">
              Feb
            </b-button>
          </b-col>
          <b-col class="mb-2">
            <b-button :disabled="test(2)" :variant="test(2) ? 'outline-secondary' : 'outline-primary'" :pressed="selectedTimePeriod == 'March'" block @click="setM(2)">
              March
            </b-button>
          </b-col>
          <b-col class="mb-2">
            <b-button :disabled="test(3)" :variant="test(3) ? 'outline-secondary' : 'outline-primary'" :pressed="selectedTimePeriod == 'April'" block @click="setM(3)">
              April
            </b-button>
          </b-col>
          <b-col class="mb-2">
            <b-button :disabled="test(4)" :variant="test(4) ? 'outline-secondary' : 'outline-primary'" :pressed="selectedTimePeriod == 'May'" block @click="setM(4)">
              May
            </b-button>
          </b-col>
          <b-col class="mb-2">
            <b-button :disabled="test(5)" :variant="test(5) ? 'outline-secondary' : 'outline-primary'" :pressed="selectedTimePeriod == 'June'" block @click="setM(5)">
              June
            </b-button>
          </b-col>

          <b-col class="mb-2">
            <b-button :disabled="test(6)" :variant="test(6) ? 'outline-secondary' : 'outline-primary'" :pressed="selectedTimePeriod == 'July'" block @click="setM(6)">
              July
            </b-button>
          </b-col>
          <b-col class="mb-2">
            <b-button :disabled="test(7)" :variant="test(7) ? 'outline-secondary' : 'outline-primary'" :pressed="selectedTimePeriod == 'Aug'" block @click="setM(7)">
              Aug
            </b-button>
          </b-col>
          <b-col class="mb-2">
            <b-button :disabled="test(8)" :variant="test(8) ? 'outline-secondary' : 'outline-primary'" :pressed="selectedTimePeriod == 'Sep'" block @click="setM(8)">
              Sep
            </b-button>
          </b-col>
          <b-col class="mb-2">
            <b-button :disabled="test(9)" :variant="test(9) ? 'outline-secondary' : 'outline-primary'" :pressed="selectedTimePeriod == 'Oct'" block @click="setM(9)">
              Oct
            </b-button>
          </b-col>
          <b-col class="mb-2">
            <b-button :disabled="test(10)" :variant="test(10) ? 'outline-secondary' : 'outline-primary'" :pressed="selectedTimePeriod == 'Nov'" block @click="setM(10)">
              Nov
            </b-button>
          </b-col>
          <b-col class="mb-2">
            <b-button :disabled="test(11)" :variant="test(11) ? 'outline-secondary' : 'outline-primary'" :pressed="selectedTimePeriod == 'Dec'" block @click="setM(11)">
              Dec
            </b-button>
          </b-col>
        </b-row>


        <b-row class="mt-4" cols="1" cols-lg="2">
          <b-col class="mb-2">
            <b-form-group
              label-align-sm="right"
              label-for="start_date"
              description="From"
            >
              <b-form-datepicker
                id="start_date"
                v-model="payload.start_date"
                cols-sm="3"
                description="From"
                required
              />
            </b-form-group>
          </b-col>
          <b-col class="mb-2">
            <b-form-group
              label-align-sm="right"
              label-for="end_date"
              description="To"
            >
              <b-form-datepicker
                id="end_date"
                v-model="payload.end_date"
                cols-sm="3"
                required
              />
            </b-form-group>
          </b-col>
        </b-row>
      </b-form-group>
    </b-form-group>


    <b-button
      variant="primary"
      block
      :disabled="payload.tax_jurisdiction_code == null || payload.start_date == null || payload.end_date == null"
      @click="submitPayload()"
    >
      <b-icon icon="box-arrow-in-up" />
      <!-- <span v-if="sellerFirm.transactions.length === 0">There are no processed transactions available for this seller firm</span> -->
      <span>Generate New Tax Record</span>
    </b-button>
  </b-card>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: 'FormAddSellerFirmTaxRecord',

  async fetch() {
    const { store } = this.$nuxt.context
    if (this.countries.length == 0) {
      await store.dispatch("country/get_all")
    }
  },

  data() {
    return {
      payload: {
        tax_jurisdiction_code: null,
        start_date: null,
        end_date: null
      },
      yearString: null
    }
  },

  computed: {
    ...mapState({
      countries: state => state.country.countries,
      sellerFirm: state => state.seller_firm.seller_firm,
      vatCountries: state => state.seller_firm.seller_firm.vat_numbers.map(vatin => vatin.country_code)
    }),


    currentYearString() {
      return this.$dateFns.format(new Date(), 'yyyy')
    },

    pastMonthDate() {
      var d = new Date()
      return d.setMonth(d.getMonth() - 1)
    },

    optionsCountryCode() {
      const countriesShortTotal = this.countries.filter(country => (country.vat_country_code !== undefined && country.vat_country_code !== null))
      const countryCodesShortTotal = countriesShortTotal.map(country => country.vat_country_code)
      const countryIntersection = this.getCountryIntersection(this.vatCountries, countryCodesShortTotal)

      let options = countryIntersection.map(vat_country_code => {
        let country = countriesShortTotal.find(country => country.vat_country_code === vat_country_code)
        let formTuple = {
          value: country.code,
          text: country.name
        }
        return formTuple
      })

      return options

    },

    selectedTimePeriod() {
      var selected = null

      if (
        this.payload.start_date == this.yearString + '-01-01' &&
                    this.payload.end_date == this.yearString + '-03-31'
      ) {
        selected = 'Q1'
      } else if (
        this.payload.start_date == this.yearString + '-04-01' &&
                    this.payload.end_date == this.yearString + '-06-30'
      ) {
        selected = 'Q2'
      } else if (
        this.payload.start_date == this.yearString + '-07-01' &&
                        this.payload.end_date == this.yearString + '-09-30'
      ) {
        selected = 'Q3'
      } else if (
        this.payload.start_date == this.yearString + '-10-01' &&
                        this.payload.end_date == this.yearString + '-12-31'
      ) {
        selected = 'Q4'
      } else if (
        this.payload.start_date == this.yearString + '-01-01' &&
                    this.payload.end_date == this.yearString + '-01-31'
      ) {
        selected = 'Jan'
      } else if (
        this.payload.start_date == this.yearString + '-02-01' &&
                    this.payload.end_date == this.yearString + ('-02-28' || '-02-29')
      ) {
        selected = 'Feb'
      } else if (
        this.payload.start_date == this.yearString + '-03-01' &&
                    this.payload.end_date == this.yearString + '-03-31'
      ) {
        selected = 'March'
      } else if (
        this.payload.start_date == this.yearString + '-04-01' &&
                    this.payload.end_date == this.yearString + '-04-30'
      ) {
        selected = 'April'
      } else if (
        this.payload.start_date == this.yearString + '-05-01' &&
                    this.payload.end_date == this.yearString + '-05-31'
      ) {
        selected = 'May'
      } else if (
        this.payload.start_date == this.yearString + '-06-01' &&
                    this.payload.end_date == this.yearString + '-06-30'
      ) {
        selected = 'June'
      } else if (
        this.payload.start_date == this.yearString + '-07-01' &&
                    this.payload.end_date == this.yearString + '-07-31'
      ) {
        selected = 'July'
      } else if (
        this.payload.start_date == this.yearString + '-08-01' &&
                    this.payload.end_date == this.yearString + '-08-31'
      ) {
        selected = 'Aug'
      } else if (
        this.payload.start_date == this.yearString + '-09-01' &&
                    this.payload.end_date == this.yearString + '-09-30'
      ) {
        selected = 'Sep'
      } else if (
        this.payload.start_date == this.yearString + '-10-01' &&
                    this.payload.end_date == this.yearString + '-10-31'
      ) {
        selected = 'Oct'
      } else if (
        this.payload.start_date == this.yearString + '-11-01' &&
                    this.payload.end_date == this.yearString + '-11-30'
      ) {
        selected = 'Nov'
      } else if (
        this.payload.start_date == this.yearString + '-12-01' &&
                    this.payload.end_date == this.yearString + '-12-31'
      ) {
        selected = 'Dec'
      }

      return selected

    },
  },

  methods: {

    getCountryIntersection(countriesVat, countries) {
      var t
      if (countriesVat.length > countries.length) t = countries, countries = countriesVat, countriesVat = t // indexOf to loop over shorter
      return countriesVat.filter(function (e) {
        return countries.indexOf(e) > -1
      })
    },


    test(timespan) {
      if (typeof(timespan) === 'string') {
        if (timespan === 'Q1') {
          return new Date() < new Date(this.yearString, 2, 31)
        } else if (timespan === 'Q2') {
          return new Date() < new Date(this.yearString, 5, 30)
        } else if (timespan === 'Q3') {
          return new Date() < new Date(this.yearString, 8, 30)
        } else if (timespan === 'Q4') {
          return new Date() < new Date(this.yearString, 11, 31)
        }
      } else if (typeof(timespan) === 'number') {
        return new Date() < new Date(this.yearString, timespan, 0)
      }

    },

    setYear(year) {
      if (year === 'current') {
        this.yearString = this.$dateFns.format(new Date(), 'yyyy')
        this.payload.start_date = this.yearString + '-01-01'
        this.payload.end_date = this.yearString + '-12-31'
      } else if(year === 'past') {
        this.yearString = this.$dateFns.format(new Date(), 'yyyy') - 1
        this.payload.start_date = this.yearString + '-01-01'
        this.payload.end_date = this.yearString + '-12-31'
      }

    },


    setQ(quarter) {
      // https://en.wikipedia.org/wiki/Calendar_year
      // First quarter, Q1: 1 January – 31 March (90 days or 91 days in leap years)
      // Second quarter, Q2: 1 April – 30 June (91 days)
      // Third quarter, Q3: 1 July – 30 September (92 days)
      // Fourth quarter, Q4: 1 October – 31 December (92 days)

      switch (quarter) {
      case 1:
        this.payload.start_date = this.yearString + '-01-01'
        this.payload.end_date = this.yearString + '-03-31'
        break
      case 2:
        this.payload.start_date = this.yearString + '-04-01'
        this.payload.end_date = this.yearString + '-06-30'
        break
      case 3:
        this.payload.start_date = this.yearString + '-07-01'
        this.payload.end_date = this.yearString + '-09-30'
        break
      case 4:
        this.payload.start_date = this.yearString + '-10-01'
        this.payload.end_date = this.yearString + '-12-31'
        break
      }

    },

    dateStringEndMonth(month) {
      var dateEndMonth = new Date(this.yearString, month+1, 0 )
      return this.$dateFns.format(dateEndMonth, 'yyyy-MM-dd')
    },

    dateStringBeginningMonth(month) {
      var dateBeginningMonth = new Date(this.yearString, month, 1 )
      return this.$dateFns.format(dateBeginningMonth, 'yyyy-MM-dd')
    },

    setM(month) {
      this.payload.start_date = this.dateStringBeginningMonth(month)
      this.payload.end_date = this.dateStringEndMonth(month)
    },

    reset() {
      this.payload = {
        tax_jurisdiction_code: null,
        start_date: null,
        end_date: null
      }
    },

    async submitPayload() {
      const seller_firm_public_id = this.sellerFirm.public_id
      var tax_record_data = this.payload
      await this.$repositories.tax_record.create_by_seller_firm_public_id(seller_firm_public_id, tax_record_data)
      this.makeToast()

    },

    makeToast() {
      this.$bvToast.toast(`Successfully created a new tax record (${this.payload.tax_jurisdiction_code}: ${this.payload.valid_from}-${this.payload.valid_from}).`, {
        title: 'New Tax Record',
        variant: 'success',
        autoHideDelay: 10000,
      })
    }
  }
}
</script>

<style>

</style>
