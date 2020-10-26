<template>
  <b-card :border-variant="cardBorder">
    <b-card-title>
      <b-row>
        <b-col cols="auto" class="mr-auto">
          <div class="text-center">
            Distance Sales
            <b-badge pill :variant="!flashCounter ? 'primary':'success'" class="ml-2">
              {{ distanceSales.length }}
            </b-badge>
          </div>
        </b-col>
        <b-col cols="auto">
          <b-form-checkbox v-model="editMode" name="check-button" switch />
        </b-col>
      </b-row>
    </b-card-title>

    <b-card-text>selected: {{ selected }}</b-card-text>


    <b-card-text>
      <h5 v-if="distanceSales.length === 0 && !editMode" class="text-muted text-center m-5">
        No Data Available Yet
      </h5>
      <div v-else>
        <div v-if="editMode===false">
          <b-table borderless :items="distanceSalesVatThresholdItems" :fields="fields" :busy="!distanceSales" hover selectable select-mode="single" @row-selected="displayItem">
            <template v-slot:table-busy>
              <div class="text-center text-secondary my-2">
                <b-spinner class="align-middle" />
                <strong>Loading...</strong>
              </div>
            </template>

            <template v-slot:cell(active)="data">
              <div>
                <b-icon v-if="data.value === true" :id="`popover-target-distance-sale-history-${data.item.arrival_country}`" icon="check-circle" variant="success" />
                <b-icon v-else :id="`popover-target-distance-sale-history-${data.item.arrival_country}`" icon="x-circle" variant="danger" />
              </div>
              <b-popover :target="`popover-target-distance-sale-history-${data.item.arrival_country}`" triggers="hover" placement="top" class="ml-2" title="History">
                <div>Test {{ data.item.arrival_country }}</div>
              </b-popover>
            </template>

            <template v-slot:cell(taxable_turnover_amount)="data">
              <b-progress :max="vatThresholds.find((el) => el.country_code === data.item.arrival_country_code)['value']" class="mb-3">
                <b-progress-bar variant="primary" :value="data.item.taxable_turnover_amount" class="self-align-center" />
                <!-- <b-progress-bar variant="warning" value="1" />
                        <b-progress-bar variant="danger" value="2" /> -->
              </b-progress>
              <div class="text-muted">
                <span>
                  {{ data.value }} {{ data.item.vat_threshold.currency_code }}
                  <!-- {{ vatThresholds.find((el) => el.country_code === data.item.arrival_country_code) }} /
                  {{ vatThresholds.find((el) => el.country_code === data.item.arrival_country_code)['value'] }}
                  {{ vatThresholds.find((el) => el.country_code === data.item.arrival_country_code)['currency_code'] }} -->
                </span>

                <span class="ml-2">|</span>
                <span class="ml-2">Further information </span>
              </div>
            </template>

            <!-- <template v-slot:cell(details)="data">

              <b-icon :id="`icon-${data.index}`" variant="info" icon="info-circle" @click="toggleIconByIndex(data.index)" />
            </template> -->
          </b-table>
        </div>

        <div v-else>
          <b-tabs content-class="mt-3">
            <b-tab title="Create" active>
              <lazy-form-add-seller-firm-distance-sale @flash="flashCount" />
            </b-tab>

            <b-tab title="Delete" :disabled="distanceSales.length === 0">
              <lazy-table-delete-seller-firm-distance-sale :fields="fieldsEditable" @flash="flashCount" />
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
        name: "CardDistanceSales",
        // eslint-disable-next-line

        data() {
            return {
                editMode: false,
                flashCounter: false,

                // icon: [],
                selected: null,

                fields: [
                    { key: "arrival_country", sortable: false },
                    { key: "active", sortable: false },
                    { key: 'taxable_turnover_amount', label: 'Taxable Turnover (past 12 months) **in progress**', sortable: false },
                    { key: 'details', label: '' }

                ]
            }
        },

        computed: {
            ...mapState({
                distanceSales: state => state.seller_firm.seller_firm.distance_sales,
                vatThresholds: state => state.vat_threshold.vat_thresholds,
            }),

            distanceSalesVatThresholdItems() {
                var news = this.distanceSales.forEach(distanceSale => distanceSale['vat_threshold'] = this.$store.getters["vat_threshold/getByCountryCode"](distanceSale.arrival_country_code))
                return news
            },


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

            displayItem: function(payload) {
                if (payload.length === 0) {
                    this.selected = 'Empty payload'
                } else {
                this.selected = payload[0]
                }
            }

            // toggleIconByIndex(index) {
            //     this.icon[index] = !this.icon[index]
            // }


        }
    }
</script>
