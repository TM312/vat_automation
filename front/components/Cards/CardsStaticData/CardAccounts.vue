<template>
  <b-card :border-variant="cardBorder">
    <b-card-title>
      <b-row>
        <b-col cols="auto" class="mr-auto">
          <div class="text-center">
            Accounts
            <b-badge pill :variant="!flashCounter ? 'primary':'success'" class="ml-2">
              {{ accounts.length }}
            </b-badge>
          </div>
        </b-col>
        <b-col v-if="!showcase" cols="auto">
          <b-form-checkbox v-model="editMode" name="check-button" switch />
        </b-col>
      </b-row>
    </b-card-title>

    <b-card-text>
      <h5 v-if="accounts.length === 0 && !editMode" class="text-muted text-center m-5">
        No Data Available Yet
      </h5>

      <div v-else-if="accounts.length !== 0 && !editMode">
        <b-table borderless :items="accounts" :fields="fields" hover>
          <template v-slot:cell(platform)>
            <img
              src="@/assets/img/logos/amazon_logo_slim.png"
              class="d-inline-block align-top"
              height="20"
            />
          </template>
        </b-table>
        <small class="text-secondary my-3">
          Under accounts you store and manage your Amazon related IDs.
          When processing we assign each transaction to the respective account to facilitate comparisons of the channel specific sales performance.
        </small>
      </div>

      <div v-else-if="editMode && !showcase">
        <b-tabs content-class="mt-3">
          <b-tab title="Create" active>
            <lazy-form-add-seller-firm-account @flash="flashCount" />
          </b-tab>

          <b-tab title="Delete" :disabled="accounts.length === 0">
            <lazy-table-delete-seller-firm-account :fields="fieldsEditable" @flash="flashCount" />
          </b-tab>
        </b-tabs>
      </div>
    </b-card-text>
  </b-card>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "CardAccounts",
  // eslint-disable-next-line

  props: {
    showcase: {
      type: Boolean,
      required: false,
      default: false
    }
  },

  data() {
    return {
      message: '',
      editMode: false,
      flashCounter: false,

      fields: [
        { key: 'platform', sortable: false },
        { key: 'channel_code', label: "Channel", sortable: false },
        { key: 'given_id', label: "Account ID", sortable: false }
      ],
    }
  },

  computed: {
    ...mapState({
      accounts: state => state.seller_firm.seller_firm.accounts,
      seller_firm: state => state.seller_firm.seller_firm,
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
