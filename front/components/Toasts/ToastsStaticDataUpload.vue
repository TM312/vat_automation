<template>
    <div>

        <hr>
        <p>status_account_files_lowest: {{ status_account_files_lowest }}</p>
        <h2>status_account_lowest: {{ status_account_lowest }}</h2>

        <hr>
        <p>Distance Sales</p>
        <p>status_distance_sale_lowest: {{ status_distance_sale_lowest }}</p>

        <hr>

        percStatusAccountFiles: {{ percStatusAccountFiles }} <br>
        percStatusItemFiles: {{ percStatusItemFiles }} <br>
        percStatusVatNumberFiles: {{ percStatusVatNumberFiles }} <br>
        percStatusDistanceSaleFiles: {{ percStatusDistanceSaleFiles }} <br>
        percStatusTransactionInputFiles: {{ percStatusTransactionInputFiles }} <br>


        statusAccountFiles: {{ statusAccountFiles }} <br>
        lenStatusAccount: {{ lenStatusAccount }} <br>
        statusItemFiles: {{ statusItemFiles }} <br>
        lenStatusItem: {{ lenStatusItem }} <br>
        statusVatNumberFiles: {{ statusVatNumberFiles }} <br>
        lenStatusVatNumber: {{ lenStatusVatNumber }} <br>
        statusDistanceSaleFiles: {{ statusDistanceSaleFiles }} <br>
        lenStatusDistanceSale: {{ lenStatusDistanceSale }} <br>
        statusTransactionInputFiles: {{ statusTransactionInputFiles }} <br>
        lenStatusTransactionInput: {{ lenStatusTransactionInput }} <br>


        <b-toast
            no-auto-hide
            :title="status_account_lowest ? status_account_lowest.title : ''"
            :variant="status_account_lowest ? status_account_lowest.variant : ''"
            v-model="toastAccount"
        >
            <div v-if="lenStatusAccount === 1">
                <b-progress :value="statusAccountFiles[0].current" :max="statusAccountFiles[0].total" animated></b-progress>
            </div>
            <div v-else>
                <div v-for="(accountFile, i) in statusAccountFiles" :key="i">
                    <b-progress :value="statusAccountFiles[i].current" :max="statusAccountFiles[i].total" animated></b-progress>
                    <p><i>Filename: {{ statusAccountFiles[i].original_filename }}</i></p>
                    <hr>
                </div>

            </div>
        </b-toast>

        <b-toast
            no-auto-hide
            :title="status_item_lowest ? status_item_lowest.title : ''"
            :variant="status_item_lowest ? status_item_lowest.variant : ''"
            v-model="toastItem"
        >
            <div v-if="lenStatusItem === 1">
                <b-progress :value="statusItemFiles[0].current" :max="statusItemFiles[0].total" animated></b-progress>
            </div>
            <div v-else>
                <div v-for="(itemFile, i) in statusItemFiles" :key="i">
                    <b-progress :value="statusItemFiles[i].current" :max="statusItemFiles[i].total" animated></b-progress>
                    <p><i>Filename: {{ statusItemFiles[i].original_filename }}</i></p>
                    <hr>
                </div>

            </div>
        </b-toast>

        <b-toast
            no-auto-hide
            :title="status_vat_number_files_lowest.title"
            :variant="status_vat_number_files_lowest.variant"
            v-model="toastVatNumber"
        >
            <div v-if="lenStatusVatNumber === 1">
                <b-progress :value="statusVatNumberFiles[0].current" :max="statusVatNumberFiles[0].total" animated></b-progress>
            </div>
            <div v-else>
                <div v-for="(vatNumberFile, i) in statusVatNumberFiles" :key="i">
                    <b-progress :value="statusVatNumberFiles[i].current" :max="statusVatNumberFiles[i].total" animated></b-progress>
                    <p><i>Filename: {{ statusVatNumberFiles[i].original_filename }}</i></p>
                    <hr>
                </div>

            </div>
        </b-toast>

          <b-toast
            no-auto-hide
            :title="status_distance_sale_lowest ? status_distance_sale_lowest.title : ''"
            :variant="status_distance_sale_lowest ? status_distance_sale_lowest.variant : ''"
            v-model="toastDistanceSale"
        >
            <div v-if="lenStatusDistanceSale === 1">
                <b-progress :value="statusDistanceSaleFiles[0].current" :max="statusDistanceSaleFiles[0].total" animated></b-progress>
            </div>
            <div v-else>
                <div v-for="(distanceSaleFile, i) in statusDistanceSaleFiles" :key="i">
                    <b-progress :value="statusDistanceSaleFiles[i].current" :max="statusDistanceSaleFiles[i].total" animated></b-progress>
                    <p><i>Filename: {{ statusDistanceSaleFiles[i].original_filename }}</i></p>
                    <hr>
                </div>

            </div>
        </b-toast>


        <b-toast
            no-auto-hide
            :title="status_transaction_input_files_lowest.title"
            :variant="status_transaction_input_files_lowest.variant"
            v-model="toastTransactionInput"
        >
            <div v-if="lenStatusTransactionInput === 1">
                <b-progress :value="statusTransactionInputFiles[0].current" :max="statusTransactionInputFiles[0].total" animated></b-progress>
            </div>
            <div v-else>
                <div v-for="(transactionInputFile, i) in statusTransactionInputFiles" :key="i">
                    <b-progress :value="statusTransactionInputFiles[i].current" :max="statusTransactionInputFiles[i].total" animated></b-progress>
                    <p><i>Filename: {{ statusTransactionInputFiles }}</i></p>
                    <hr>
                </div>

            </div>
        </b-toast>


    </div>

</template>

<script>
import { mapState } from 'vuex'

export default {
    name: 'ToastsStaticDataUpload',

    data() {
        return {
            toastAccount: false,
            toastItem: false,
            toastVatNumber: false,
            toastDistanceSale: false,
            toastTransactionInput: false
        }
    },

    computed: {
        ...mapState({
            sellerFirm: state => state.seller_firm.seller_firm,

            statusAccountFiles: state => state.status.status_account_files,
            lenStatusAccount: state => state.status.status_account_files.length,

            statusItemFiles: state => state.status.status_item_files,
            lenStatusItem: state => state.status.status_item_files.length,

            statusVatNumberFiles: state => state.status.status_vat_number_files,
            lenStatusVatNumber: state => state.status.status_vat_number_files.length,

            statusDistanceSaleFiles: state => state.status.status_distance_sale_files,
            lenStatusDistanceSale: state => state.status.status_distance_sale_files.length,

            statusTransactionInputFiles: state => state.status.status_transaction_input_files,
            lenStatusTransactionInput: state => state.status.status_transaction_input_files.length
        }),

        percStatusAccountFiles() {
            return this.$store.getters['status/percStatusAccountFiles']
        },
        percStatusItemFiles() {
            return this.$store.getters['status/percStatusItemFiles']
        },
        percStatusVatNumberFiles() {
            return this.$store.getters['status/percStatusVatNumberFiles']
        },
        percStatusDistanceSaleFiles() {
            return this.$store.getters['status/percStatusDistanceSaleFiles']
        },
        percStatusTransactionInputFiles() {
            return this.$store.getters['status/percStatusTransactionInputFiles']
        },

        status_account_files_lowest() {
            return this.$store.getters['status/status_account_files_lowest']
        },

        status_item_files_lowest() {
            return this.$store.getters['status/status_item_files_lowest']
        },

        status_vat_number_files_lowest() {
            return this.$store.getters['status/status_vat_number_files_lowest']
        },

        status_distance_sale_files_lowest() {
            return this.$store.getters['status/status_distance_sale_files_lowest']
        },

        status_transaction_input_files_lowest() {
            return this.$store.getters['status/status_transaction_input_files_lowest']
        },

        status_account_lowest() {
            return this.$store.getters['status/status_account_lowest']
        },

        status_item_lowest() {
            return this.$store.getters['status/status_item_lowest']
        },

        status_vat_number_lowest() {
            return this.$store.getters['status/status_vat_number_lowest']
        },

        status_distance_sale_lowest() {
            return this.$store.getters['status/status_distance_sale_lowest']
        },

        status_transaction_input_lowest() {
            return this.$store.getters['status/status_transaction_input_lowest']
        },


    },

    methods: {
        sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        },
    },

    watch: {
        // https://stackoverflow.com/questions/43270159/vue-js-2-how-to-watch-store-values-from-vuex
        /*eslint-disable */

        lenStatusAccount (newLength, oldLength) {
            if (oldLength === 0) {
                // this.$bvToast.show('toastAccount')
                this.toastAccount = true
            } else if (newLength === 0) {
                this.toastAccount = false
            }
        },
        lenStatusItem (newLength, oldLength) {
            if (oldLength === 0) {
                // this.$bvToast.show('toastItem')
                this.toastItem = true
            } else if (newLength === 0) {
                this.toastItem = false
            }
        },
        lenStatusVatNumber (newLength, oldLength) {
            if (oldLength === 0) {
                // this.$bvToast.show('toastVatNumber')
                this.toastVatNumber = true
            } else if (newLength === 0) {
                this.toastVatNumber = false
            }
        },
        lenStatusDistanceSale (newLength, oldLength) {
            if (oldLength === 0) {
                // this.$bvToast.show('toastDistanceSale')
                this.toastDistanceSale = true
            } else if (newLength === 0) {
                this.toastDistanceSale = false
            }
        },
        lenStatusTransactionInput (newLength, oldLength) {
            if (oldLength === 0) {
                // this.$bvToast.show('toastTransactionInput')
                this.toastTransactionInput = true
            } else if (newLength === 0) {
                this.toastTransactionInput = false
            }
        },

        percStatusAccountFiles: {
            handler: async function(val, oldVal) {
                if (Math.min(...this.percStatusAccountFiles) === 1) {
                    await this.sleep(10000)
                    const { store } = this.$nuxt.context
                    store.commit('status/CLEAR_STATUS_ACCOUNT_FILES')
                }
            }
        },
        percStatusItemFiles: {
            handler: async function(val, oldVal) {
                if (Math.min(...this.percStatusItemFiles) === 1) {
                    await this.sleep(10000)
                    const { store } = this.$nuxt.context
                    store.commit('status/CLEAR_STATUS_ITEM_FILES')
                }
            },
        },
        percStatusVatNumberFiles: {
            handler: async function(val, oldVal) {
                if (Math.min(...this.percStatusVatNumberFiles) === 1) {
                    await this.sleep(10000)
                    const { store } = this.$nuxt.context
                    store.commit('status/CLEAR_STATUS_VAT_NUMBER_FILES')
                }
            }
        },
        percStatusDistanceSaleFiles: {
            handler: async function(val, oldVal) {
                if (Math.min(...this.percStatusDistanceSaleFiles) === 1) {
                    await this.sleep(10000)
                    const { store } = this.$nuxt.context
                    store.commit('status/CLEAR_STATUS_DISTANCE_SALE_FILES')
                }
            }
        },
        percStatusTransactionInputFiles: {
            handler: async function(val, oldVal) {
                if (Math.min(...this.percStatusTransactionInputFiles) === 1) {
                    await this.sleep(5000)
                    const { store } = this.$nuxt.context
                    store.commit('status/CLEAR_STATUS_TRANSACTION_INPUT_FILES')
                }
            }
       }
        /*eslint-disable */

    }


}
</script>

<style>

</style>
