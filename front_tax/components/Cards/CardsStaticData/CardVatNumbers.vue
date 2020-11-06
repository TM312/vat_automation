<template>
  <b-card :border-variant="cardBorder">
    <b-card-title>
      <b-row>
        <b-col cols="auto" class="mr-auto">
          Vat Numbers
          <b-badge pill :variant="!flashCounter ? 'primary':'success'" class="ml-2">
            {{ vatNumbers.length }}
          </b-badge>
        </b-col>
        <b-col cols="auto">
          <b-form-checkbox v-model="editMode" name="check-button" switch />
        </b-col>
      </b-row>
    </b-card-title>

    <b-card-text>
      <h5 v-if="vatNumbers.length === 0 && !editMode" class="text-muted text-center m-5">
        No Data Available Yet
      </h5>
      <div v-else>
        <div v-if="editMode===false">
          <b-table borderless :items="vatNumbers" :fields="fields" hover>
            <template v-slot:cell(vatin)="data">
              {{ data.item.country_code }} - {{ data.item.number }}
            </template>

            <template v-slot:cell(valid)="data">
              <b-icon v-if="data.value === true" icon="check-circle" variant="success" />
              <b-icon v-else-if="data.value === false" icon="x-circle" variant="danger" />
              <span v-else>
                <b-button
                  size="sm"
                  variant="outline-primary"
                  :disabled="buttonValidateBusy"
                  @click="validate(data.item)"
                >
                  Retry Validation
                </b-button>
              </span>
            </template>

            <template v-slot:head(validity)="data">
              <span>
                {{ data.label }}
                <b-icon id="popover-validity" icon="info-circle" variant="info" class="ml-2" />
              </span>

              <b-popover
                target="popover-validity"
                triggers="hover"
                variant="info"
                placement="right"
              >
                We regularly check the validity of the vat numbers below to provide up to date information on their status. Once checked the vat numbers are considered valid for 30 days.
              </b-popover>
            </template>

            <template v-slot:cell(validity)="data">
              <span v-if="data.item.valid">
                {{ data.item.valid_from }}
                <b-icon icon="arrow-right" variant="primary" class="mx-2" />
                {{ data.item.valid_to }}
              </span>
              <span v-else-if="data.item.valid === null"></span>
            </template>


            <template v-slot:cell(initial_tax_date)="data">
              <span v-if="data.value && typeof(data.value) === 'string'"> {{ data.value }}</span>
              <span v-else><i>Not yet used.</i></span>
            </template>
          </b-table>
        </div>

        <div v-else>
          <b-tabs content-class="mt-3">
            <b-tab title="Create" active>
              <lazy-form-add-seller-firm-vat-number @flash="flashCount" />
            </b-tab>

            <b-tab title="Delete" :disabled="vatNumbers.length === 0">
              <lazy-table-delete-seller-firm-vat-number :fields="fieldsEditable" @flash="flashCount" />
            </b-tab>
          </b-tabs>
        </div>
      </div>
    </b-card-text>
  </b-card>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "CardVatNumbers",
  // eslint-disable-next-line

  data() {
    return {
      editMode: false,
      flashCounter: false,
      buttonValidateBusy: false,

      fields: [
        { key: "vatin", label: "VATIN", sortable: false },
        { key: "valid", sortable: false },
        { key: "request_date", sortable: false },
        { key: "validity", sortable: false },
        { key: "initial_tax_date", sortable: false },
      ]
    }
  },

  computed: {
    ...mapState({
      vatNumbers: state => state.seller_firm.seller_firm.vat_numbers,
    }),

    cardBorder() {
      return this.editMode ? "info" : ""
    },

    fieldsEditable() {
      return this.fields.concat({
        key: "edit",
        label: "",
        sortable: false
      })
    }


  },

  methods: {
    flashCount() {
      this.flashCounter = true
      setTimeout(() => this.flashCounter = false, 1000)

    },

    async evaluateRefresh() {
      await this.$store.dispatch("seller_firm/get_by_public_id", this.$route.params.public_id)
    },

    async validate(item) {
      this.buttonValidateBusy = true

      const payload = {
        country_code: item.country_code,
        number: item.number
      }

      await this.$store.dispatch("vatin/validate", payload)

      await this.evaluateRefresh()

      this.buttonValidateBusy = false
    },


  }
}
</script>
