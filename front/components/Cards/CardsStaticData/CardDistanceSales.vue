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


    <b-card-text>
      <h5 v-if="distanceSales.length === 0 && !editMode" class="text-muted text-center m-5">
        No Data Available Yet
      </h5>
      <div v-else>
        <!-- <b-row cols="1" cols-lg="2">
          <b-col v-for="distanceSale in distanceSales" :key="distanceSale.arrival_country" class="mb-2">
            <b-card :title="distanceSale.active" :sub-title="distanceSale.arrival_country">
              <b-card-text>
                <b-button size="sm" variant="outline-primary">
                  Details
                </b-button>
              </b-card-text>
            </b-card>
          </b-col>
        </b-row> -->




        <div v-if="editMode===false">
          <b-table borderless :items="distanceSales" :fields="fields" :busy="!distanceSales" hover>
            <template v-slot:table-busy>
              <div class="text-center text-secondary my-2">
                <b-spinner class="align-middle" />
                <strong>Loading...</strong>
              </div>
            </template>

            <template v-slot:cell(active)="data">
              <div :id="`popover-target-distance-sale-history-${data.item.arrival_country}`">
                <b-icon v-if="data.value === true" icon="check-circle" variant="success" />
                <b-icon v-else icon="x-circle" variant="danger" />
              </div>
              <b-popover :target="`popover-target-distance-sale-history-${data.item.arrival_country}`" triggers="hover" placement="top" class="ml-2" title="History">
                <div>Test {{ data.item.arrival_country }}</div>
              </b-popover>
            </template>

            <template v-slot:cell(vat_taxable_turnover_amount_12m)>
              <b-progress max="12" class="mb-3">
                <b-progress-bar variant="primary" value="9" />
                <!-- <b-progress-bar variant="warning" value="1" />
                <b-progress-bar variant="danger" value="2" /> -->
              </b-progress>
            </template>
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

                fields: [
                    { key: "arrival_country", sortable: false },
                    { key: "active", sortable: false },
                    { key: 'vat_taxable_turnover_amount_12m', label: 'Taxable Turnover Amount (past 12 months)' }
                ]
            }
        },

        computed: {
            ...mapState({
                distanceSales: state => state.seller_firm.seller_firm.distance_sales,
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

            }


        }
    }
</script>
