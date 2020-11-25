
<template>
  <div>
    <div>
      <input
        id="files"
        ref="files"
        style="display: none"
        type="file"
        multiple
        @change="onFilesSelected"
      />

      <b-button
        id="selectButton"
        variant="outline-primary"
        :disabled="files.length === 4"
        pill
        @click="fillFiles"
      >
        <b-icon icon="file-plus" /> Files
      </b-button>

      <b-button variant="outline-secondary" pill @click="files = []">
        <b-icon icon="arrow-counterclockwise" /> Reset
      </b-button>

      <b-button
        id="upload-showcase"
        class="neuphormism"
        variant="primary"
        :disabled="buttonDisabled"
        pill
        @click="uploadFilesShowcase"
      >
        <b-icon v-if="!uploadInProgress" icon="box-arrow-in-right" />
        <b-spinner v-else small label="Spinning" />
        Upload
      </b-button>
    </div>

    <div class="mt-3 neuphormism p-2" style="border-radius: 10px">
      <b-table
        v-show="files.length > 0"
        hover
        borderless
        :items="files"
        :fields="fields"
      >
        <template v-slot:cell(button)="data">
          <b-button
            size="sm"
            variant="outline-danger"
            class="remove-file"
            @click="removeFile(data.index)"
          >
            <b-icon icon="trash" />
          </b-button>
        </template>
      </b-table>
      <div v-show="files.length === 0" class="text-center p-5">
        <h5 class="text-muted">
          No Files Selected
        </h5>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "CardDataUploadShowcase",

  data() {
    return {
      uploadInProgress: false,
      files: [
        {
          name: "accounts.csv",
          lastModified: new Date(),
          type: "accounts",
          number: 2,
        },
        {
          name: "items.csv",
          lastModified: new Date(),
          type: "items",
          number: 23,
        },
        {
          name: "vat_numbers.csv",
          lastModified: new Date(),
          type: "VAT numbers",
          number: 7,
        },
        {
          name: "distance_sales.csv",
          lastModified: new Date(),
          type: "distance sales",
          number: 5,
        },
        {
          name: "Sales Tax Transaction Report_M-2020-01",
          lastModified: new Date(),
          type: "transactions",
          number: 285,
        },
      ],
      fields: [
        "name",
        {
          key: "lastModified",
          label: "Last Modified",
          formatter: (value, key, item) => {
            return new Date(item.lastModified).toLocaleString()
          },
        },
        {
          key: "button",
          label: "",
        },
      ],

      uploadedFiles: [],
    }
  },

  computed: {
    ...mapState({
      sellerFirm: (state) => state.seller_firm.seller_firm,
      channels: (state) => state.channel.channels,
      countries: (state) => state.country.countries,
      currencies: (state) => state.currency.currencies,
      taxTreatments: (state) => state.tax_treatment.tax_treatments,
      taxRateTypes: (state) => state.tax_rate_type.tax_rate_types,
      vatThresholds: (state) => state.vat_threshold.vat_thresholds,
      transactionInputs: (state) => state.transaction_input.transaction_inputs,
    }),

    buttonDisabled() {
      if (this.files.length == 0 || this.uploadInProgress) {
        return true
      } else {
        return false
      }
    },
  },

  methods: {
    async fetchData() {
      const { store } = this.$nuxt.context

      if (this.countries.length === 0) {
        await store.dispatch("country/get_all")
      }

      if (this.currencies.length === 0) {
        await store.dispatch("currency/get_all")
      }

      if (this.taxTreatments.length === 0) {
        await store.dispatch("tax_treatment/get_all")
      }

      if (this.taxRateTypes.length === 0) {
        await store.dispatch("tax_rate_type/get_all")
      }

      if (this.channels.length === 0) {
        await store.dispatch("channel/get_all")
      }

      if (this.vatThresholds.length === 0) {
        await store.dispatch("vat_threshold/get_all")
      }

      if (this.sellerFirm.length === 0) {
        await store.dispatch("seller_firm/get_sample")
      }

      if (this.transactionInputs.length === 0) {
        const params = {
          seller_firm_public_id: this.sellerFirm.public_id,
          page: 1,
        }
        await store.dispatch("transaction_input/get_sample", params)
      }
    },

    async uploadFilesShowcase() {
      this.uploadInProgress = true
      for (var i = 0; i != this.files.length; ) {
        await this.fetchData()
        await this.sleep(1800)
        const index = this.uploadedFiles.findIndex(
          (e) => e.name === this.files[i].name
        )

        this.makeToast(index, this.files[i])
        this.commitToShowcaseStore(index, this.files[i].type)
        this.uploadedFiles.push(this.files[i])
        this.removeFile(i)
      }
      this.uploadInProgress = false
    },

    commitToShowcaseStore(index, type) {
      const { store } = this.$nuxt.context
      if (type === "accounts" && index === -1) {
        store.commit("showcase/SET_SHOWCASE_ACCOUNTS")
      } else if (type === "distance sales" && index === -1) {
        store.commit("showcase/SET_SHOWCASE_DISTANCE_SALES")
      } else if (type === "VAT numbers" && index === -1) {
        store.commit("showcase/SET_SHOWCASE_VAT_NUMBERS")
      } else if (type === "items" && index === -1) {
        store.commit("showcase/SET_SHOWCASE_ITEMS")
      }
    },

    makeToast(index, file) {
      if (index === -1) {
        this.$bvToast.toast(`Successfully processed ${file.name}!`, {
          title: `${file.number} new ${file.type}`,
          autoHideDelay: 5000,
          variant: "success",
        })
      } else {
        this.$bvToast.toast(
          `The file ${file.name} has been successfully processed! ${file.number} ${file.type} had been uploaded earlier.`,
          {
            title: `Duplicates In Uploaded ${this.capitalize(
              file.type
            )} `,
            autoHideDelay: 10000,
            variant: "light",
          }
        )
      }
    },

    fillFiles() {
      this.files = [
        {
          name: "accounts.csv",
          lastModified: new Date(),
          type: "accounts",
          number: 2,
        },
        {
          name: "items.csv",
          lastModified: new Date(),
          type: "items",
          number: 23,
        },
        {
          name: "vat_numbers.csv",
          lastModified: new Date(),
          type: "VAT numbers",
          number: 7,
        },
        {
          name: "distance_sales.csv",
          lastModified: new Date(),
          type: "distance sales",
          number: 5,
        },
        {
          name: "Sales Tax Transaction Report_M-2020-01",
          lastModified: new Date(),
          type: "transactions",
          number: 285,
        },
      ]
    },

    onFilesSelected() {
      let selectedFiles = this.files

      for (var i = 0; i < selectedFiles.length; i++) {
        this.files.push(selectedFiles[i])
      }
    },

    removeFile(i) {
      this.files.splice(i, 1)
    },
  },
}
</script>
<style scoped>
    .card-upload {
        padding-bottom: 1rem;
        padding-left: 3rem;
        padding-right: 3rem;
        padding-top: 3rem;
        border-radius: 15px;
        box-shadow: 6px 6px 12px #bdbcbc, -6px -6px 12px #ffffff !important;
    }

    .neuphormism {
        box-shadow: 6px 6px 12px #bdbcbc, -6px -6px 12px #ffffff !important;
    }
</style>
