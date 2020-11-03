<template>
  <div>
    <b-row>
      <b-col cols="12" lg="6" xl="4">
        <card-transaction-base-data :transaction="transaction" />


        <div class="mt-5">
          <b-card
            v-if="transaction.tax_treatment_code === 'INTRA_COMMUNITY_ACQUISITION' ||
              transaction.tax_treatment_code === 'LOCAL_ACQUISITION'"
            title="Supplier"
          >
            <b-row>
              <b-col cols="5" xl="4">
                <b>Transaction Relationship:</b>
              </b-col>
              <b-col
                cols="7"
                xl="8"
                style="white-space: pre-wrap word-wrap:break-word"
                class="mr-auto"
              >
                <b-button-group size="sm" class="ml-2">
                  <b-button
                    :variant="transaction.supplier_relationship === 'B2B' ? 'success' : 'outline-secondary' "
                  >
                    B2B
                  </b-button>
                  <b-button
                    :variant="
                      transaction.supplier_relationship === 'B2C' ? 'success' : 'outline-secondary' "
                  >
                    B2C
                  </b-button>
                </b-button-group>
              </b-col>
            </b-row>
            <b-row
              v-if="transaction.supplier_relationship === 'B2B'"
            >
              <b-col cols="5" xl="4">
                <b>Vat Number:</b>
              </b-col>
              <b-col
                cols="7"
                xl="8"
                style="white-space: pre-wrap"
                class="mr-auto"
              >
                <span>{{
                  transaction.supplier_vatin.country_code
                }}
                  -
                  {{
                    transaction.supplier_vatin.number
                  }}</span>
                <!-- <span v-if="transaction.supplier_vatin.name"><b-icon icon="info-circle" @hover="getVatInfo()"/></span> -->
              </b-col>
            </b-row>
            <b-row v-if="transaction.supplier_vatin.name">
              <b-col cols="5" xl="4">
                <b>Name:</b>
              </b-col>
              <b-col
                cols="7"
                xl="8"
                style="white-space: pre-wrap"
                class="mr-auto"
              >
                {{ transaction.supplier_vatin.name }}
              </b-col>
            </b-row>
          </b-card>

          <b-card v-else title="Customer">
            <b-row>
              <b-col cols="5" xl="4">
                <b>Transaction Relationship:</b>
              </b-col>
              <b-col
                cols="7"
                xl="8"
                style="white-space: pre-wrap word-wrap:break-word"
                class="mr-auto"
              >
                <b-button-group size="sm" class="ml-2">
                  <b-button
                    :variant="
                      transaction.customer_relationship ===
                        'B2B'
                        ? 'success'
                        : 'outline-secondary'
                    "
                  >
                    B2B
                  </b-button>
                  <b-button
                    :variant="
                      transaction.customer_relationship ===
                        'B2C'
                        ? 'success'
                        : 'outline-secondary'
                    "
                  >
                    B2C
                  </b-button>
                </b-button-group>
              </b-col>
            </b-row>
            <b-row
              v-if="transaction.customer_relationship === 'B2B'"
            >
              <b-col cols="5" xl="4">
                <b>Vat Number:</b>
              </b-col>
              <b-col
                cols="7"
                xl="8"
                style="white-space: pre-wrap"
                class="mr-auto"
              >
                <span>{{
                  transaction.customer_vatin.country_code
                }}
                  -
                  {{
                    transaction.customer_vatin.number
                  }}</span>
                <span v-if="transaction.customer_vatin.number"><b-icon
                  icon="info-circle"
                  @hover="getVatInfo()"
                /></span>
              </b-col>
            </b-row>
            <div v-if="transaction.customer_vatin">
              <b-row v-if="transaction.customer_vatin.name">
                <b-col cols="5" xl="4">
                  <b>Name:</b>
                </b-col>
                <b-col
                  cols="7"
                  xl="8"
                  style="white-space: pre-wrap"
                  class="mr-auto"
                >
                  {{ transaction.customer_vatin.name }}
                </b-col>
              </b-row>
              <b-row v-if="transaction.customer_vatin.address">
                <b-col cols="5" xl="4">
                  <b>Address:</b>
                </b-col>
                <b-col
                  cols="7"
                  xl="8"
                  style="white-space: pre-wrap"
                  class="mr-auto"
                >
                  {{ transaction.customer_vatin.address }}
                </b-col>
              </b-row>
            </div>
          </b-card>
        </div>
      </b-col>
      <b-col cols="12" lg="6" xl="8">
        <card-transaction-prices :transaction="transaction" />

        <!-- <b-card title="Prices">
          <div class="mt-3">
            <b-table
              hover
              fixed
              :items="itemsItem"
              :fields="fieldsItemPrices"
              class="mb-4"
            />
          </div>
          <div class="my-3">
            <b-table
              hover
              fixed
              :items="itemsShipment"
              :fields="fieldsShipmentPrices"
              class="mb-4"
            />
          </div>
          <div>
            <b-table
              hover
              fixed
              :items="itemsGiftWrap"
              :fields="fieldsGiftWrapPrices"
              class="mb-4"
            />
          </div>
          <div class="mt-2">
            <b-table
              hover
              fixed
              :items="itemsTotal"
              :fields="fieldsTotalPrices"
              class="mb-4"
            />
          </div>
        </b-card> -->
      </b-col>
    </b-row>

    <b-row cols="1" cols-lg="2" cols-xl="3" class="mt-5">
      <b-col
        v-for="notification in transaction.notifications"
        :key="notification.public_id"
      >
        <card-transaction-input-notification
          :notification="notification"
          style="max-width: 50rem"
          class="h-100"
        />
      </b-col>
    </b-row>
  </div>
</template>

<script>
export default {
  name: "CardTransaction",
  props: {
    transaction: {
      type: [Array, Object],
      required: true,
    },
  },

  methods: {
    getVatInfo() {
      console.log("test")
    },
    // getPopupDetail(code, position) {
    //   return this.taxRateTypes.find((el) => el.code === code)[position]
    // },
  },
}
</script>

<style>
</style>
