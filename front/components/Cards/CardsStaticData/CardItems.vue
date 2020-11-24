<template>
  <b-card :border-variant="cardBorder">
    <b-card-title>
      <b-row>
        <b-col cols="auto" class="mr-auto">
          Items
          <b-badge
            pill
            :variant="!flashCounter ? 'primary' : 'success'"
            class="ml-2"
          >
            {{ items.length }}
          </b-badge>
        </b-col>
        <b-col v-if="!showcase" cols="auto">
          <b-form-checkbox
            v-model="editMode"
            name="check-button"
            switch
          />
        </b-col>
      </b-row>
    </b-card-title>
    <b-card-text>
      <h5
        v-if="items.length === 0 && !editMode"
        class="text-muted text-center m-5"
      >
        No Data Available Yet
      </h5>
      <div v-else>
        <div v-if="editMode === false">
          <b-pagination
            v-model="currentPage"
            :total-rows="items.length"
            :per-page="perPage"
            aria-controls="table-items"
            pills
            class="my-3"
          />

          <b-table
            id="table-items"
            borderless
            :items="items"
            :fields="fields"
            hover
            :per-page="perPage"
            :current-page="currentPage"
          >
            <template v-slot:cell(unit_cost_price_net)="data">
              <span>{{ data.value }}</span>
              <span>{{ data.item.unit_cost_price_currency_code === 'EUR' ? '€' : data.item.unit_cost_price_currency_code }}</span>
            </template>

            <template v-slot:cell(name)="data">
              <span v-if="data.value.length > 30" v-b-tooltip.hover :title="data.value">{{ data.value.slice(0,20) }}...</span>
              <span v-else>{{ data.value }}</span>
            </template>

            <template v-slot:cell(weight_kg)="data">
              <span v-if="data.value >= 1">{{ data.value }}kg</span>
              <span v-else>{{ parseInt(data.value * 1000) }}g</span>
            </template>
          </b-table>
        </div>

        <div v-else-if="editMode && !showcase">
          <b-tabs content-class="mt-3">
            <b-tab title="Create" active>
              <lazy-form-add-seller-firm-item
                @flash="flashCount"
              />
            </b-tab>

            <b-tab title="Delete" :disabled="items.length === 0">
              <lazy-table-delete-seller-firm-item
                :fields="fieldsEditable"
                @flash="flashCount"
              />
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
  name: "CardItems",

  props: {
    showcase: {
      type: Boolean,
      required: false,
      default: false
    },
    // in parent component pass :per-page="5" https://github.com/vuejs/vue/issues/1704
    perPage: {
      type: Number,
      required: false,
      default: 25
    }
  },


  data() {
    return {
      editMode: false,
      flashCounter: false,
      currentPage: 1,

      fields: [
        { key: "brand_name", sortable: false },
        { key: "sku", label: "SKU", sortable: false },
        { key: "name", sortable: false },
        { key: "tax_code_code", label: "Tax Code", sortable: false },
        {
          key: "weight_kg",
          label: "Weight",
          formatter: (value) => {
            return Number.parseFloat(value).toFixed(3)
          },
          sortable: false,
        },
        {
          key: "unit_cost_price_net",
          label: 'Net Unit Costs',
          sortable: false,
          formatter: (value) => {
            return Number.parseFloat(value).toFixed(2)
          },
        },
      ],
    }
  },

  computed: {
    ...mapState({
      items: (state) => state.seller_firm.seller_firm.items,
      seller_firm: (state) => state.seller_firm.seller_firm,
    }),

    cardBorder() {
      return this.editMode ? "info" : ""
    },

    fieldsEditable() {
      return this.fields.concat({
        key: "edit",
        label: "",
        sortable: false,
      })
    },
  },

  methods: {
    flashCount() {
      this.flashCounter = true
      setTimeout(() => (this.flashCounter = false), 1000)
    },
  },
}
</script>
