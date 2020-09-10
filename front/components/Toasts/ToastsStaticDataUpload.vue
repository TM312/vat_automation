<template>
    <div>

        <hr>
        <p>status_account_targets_lowest: {{ status_account_targets_lowest }}</p>
        <h2>status_account_lowest: {{ status_account_lowest }}</h2>

        <hr>
        <p>Distance Sales</p>
        <p>status_distance_sale_lowest: {{ status_distance_sale_lowest }}</p>

        <hr>

        percStatusAccountTargets: {{ percStatusAccountTargets }} <br>
        percStatusItemTargets: {{ percStatusItemTargets }} <br>
        percStatusVatNumberTargets: {{ percStatusVatNumberTargets }} <br>
        percStatusDistanceSaleTargets: {{ percStatusDistanceSaleTargets }} <br>
        percStatusTransactionInputTargets: {{ percStatusTransactionInputTargets }} <br>


        statusAccountTargets: {{ statusAccountTargets }} <br>
        lenStatusAccount: {{ lenStatusAccount }} <br>
        statusItemTargets: {{ statusItemTargets }} <br>
        lenStatusItem: {{ lenStatusItem }} <br>
        statusVatNumberTargets: {{ statusVatNumberTargets }} <br>
        lenStatusVatNumber: {{ lenStatusVatNumber }} <br>
        statusDistanceSaleTargets: {{ statusDistanceSaleTargets }} <br>
        lenStatusDistanceSale: {{ lenStatusDistanceSale }} <br>
        statusTransactionInputTargets: {{ statusTransactionInputTargets }} <br>
        lenStatusTransactionInput: {{ lenStatusTransactionInput }} <br>


        <b-toast
            :title="status_account_lowest ? status_account_lowest.title : ''"
            :variant="status_account_lowest ? status_account_lowest.variant : ''"
            v-model="toastAccount"
        >
            <div v-for="(accountTarget, i) in statusAccountTargets" :key="i" class="py-2">
                <div v-if="accountTarget.target === 'infobox'">
                    <b-card border-variant="info">
                        <b-card-text>{{ accountTarget.message }}</b-card-text>
                    </b-card>
                </div>
                <div v-else>
                    <b-progress :value="statusAccountTargets[i].current" :max="statusAccountTargets[i].total" animated></b-progress>
                    <p class="mt-2">Filename: <i>{{ statusAccountTargets[i].target }}</i></p>
                    <hr v-if="statusAccountTargets.length > 1">
                </div>
            </div>
        </b-toast>

        <b-toast
            :title="status_item_lowest ? status_item_lowest.title : ''"
            :variant="status_item_lowest ? status_item_lowest.variant : ''"
            v-model="toastItem"
        >
            <div v-for="(itemTarget, i) in statusItemTargets" :key="i" class="py-2">
                <div v-if="itemTarget.target === 'infobox'">
                    <b-card border-variant="info">
                        <b-card-text>{{ itemTarget.message }}</b-card-text>
                    </b-card>
                </div>
                <div v-else>
                    <b-progress :value="statusItemTargets[i].current" :max="statusItemTargets[i].total" animated></b-progress>
                    <p class="mt-2">Filename: <i>{{ statusItemTargets[i].target }}</i></p>
                    <hr v-if="statusItemTargets.length > 1">
                </div>
            </div>
        </b-toast>

        <b-toast
            :title="status_vat_number_lowest.title"
            :variant="status_vat_number_lowest.variant"
            v-model="toastVatNumber"
        >
            <div v-for="(vatNumberTarget, i) in statusVatNumberTargets" :key="i" class="py-2">
                <div v-if="vatNumberTarget.target === 'infobox'">
                    <b-card border-variant="info">
                        <b-card-text>{{ vatNumberTarget.message }}</b-card-text>
                    </b-card>
                </div>
                <div v-else>
                    <b-progress :value="statusVatNumberTargets[i].current" :max="statusVatNumberTargets[i].total" animated></b-progress>
                    <p class="mt-2">Filename: <i>{{ statusVatNumberTargets[i].target }}</i></p>
                    <hr v-if="statusVatNumberTargets.length > 1">
                </div>
            </div>

        </b-toast>

        <b-toast
            :title="status_distance_sale_lowest ? status_distance_sale_lowest.title : ''"
            :variant="status_distance_sale_lowest ? status_distance_sale_lowest.variant : ''"
            v-model="toastDistanceSale"
        >
            <div v-for="(distanceSaleTarget, i) in statusDistanceSaleTargets" :key="i" class="py-2">
                <div v-if="distanceSaleTarget.target === 'infobox'">
                    <b-card border-variant="info">
                        <b-card-text>{{ distanceSaleTarget.message }}</b-card-text>
                    </b-card>
                </div>
                <div v-else>
                    <b-progress :value="statusDistanceSaleTargets[i].current" :max="statusDistanceSaleTargets[i].total" animated></b-progress>
                    <p class="mt-2">Filename: <i>{{ statusDistanceSaleTargets[i].target }}</i></p>
                    <hr v-if="statusDistanceSaleTargets.length > 1">
                </div>

            </div>

        </b-toast>


        <b-toast
            :title="statis_transaction_input_lowest ? status_transaction_input_lowest.title : ''"
            :variant="statis_transaction_input_lowest ? status_transaction_input_lowest.variant : ''"
            v-model="toastTransactionInput"
        >
            <div v-for="(transactionInputTarget, i) in statusTransactionInputTargets" :key="i">
                <div v-if="transactionInputTarget.target === 'infobox'">
                    <b-card border-variant="info">
                        <b-card-text>{{ transactionInputTarget.message }}</b-card-text>
                    </b-card>
                </div>
                <div v-else>
                    <b-progress :value="statusTransactionInputTargets[i].current" :max="statusTransactionInputTargets[i].total" animated></b-progress>
                    <p class="mt-2">Filename: <i>{{ statusTransactionInputTargets }}</i></p>
                    <hr v-if="statusTransactionInputTargets.length > 1">
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

            statusAccountTargets: state => state.status.status_account_targets,
            lenStatusAccount: state => state.status.status_account_targets.length,

            statusItemTargets: state => state.status.status_item_targets,
            lenStatusItem: state => state.status.status_item_targets.length,

            statusVatNumberTargets: state => state.status.status_vat_number_targets,
            lenStatusVatNumber: state => state.status.status_vat_number_targets.length,

            statusDistanceSaleTargets: state => state.status.status_distance_sale_targets,
            lenStatusDistanceSale: state => state.status.status_distance_sale_targets.length,

            statusTransactionInputTargets: state => state.status.status_transaction_input_targets,
            lenStatusTransactionInput: state => state.status.status_transaction_input_targets.length
        }),

        percStatusAccountTargets() {
            return this.$store.getters['status/percStatusAccountTargets']
        },
        percStatusItemTargets() {
            return this.$store.getters['status/percStatusItemTargets']
        },
        percStatusVatNumberTargets() {
            return this.$store.getters['status/percStatusVatNumberTargets']
        },
        percStatusDistanceSaleTargets() {
            return this.$store.getters['status/percStatusDistanceSaleTargets']
        },
        percStatusTransactionInputTargets() {
            return this.$store.getters['status/percStatusTransactionInputTargets']
        },

        status_account_targets_lowest() {
            return this.$store.getters['status/status_account_targets_lowest']
        },

        status_item_targets_lowest() {
            return this.$store.getters['status/status_item_targets_lowest']
        },

        status_vat_number_targets_lowest() {
            return this.$store.getters['status/status_vat_number_targets_lowest']
        },

        status_distance_sale_targets_lowest() {
            return this.$store.getters['status/status_distance_sale_targets_lowest']
        },

        status_transaction_input_targets_lowest() {
            return this.$store.getters['status/status_transaction_input_targets_lowest']
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

        percStatusAccountTargets: {
            handler: async function(val, oldVal) {
                if (Math.min(...this.percStatusAccountTargets) === 1) {
                    await this.sleep(10000)
                    const { store } = this.$nuxt.context
                    store.commit('status/CLEAR_STATUS_ACCOUNT_TARGETS')
                }
            }
        },
        percStatusItemTargets: {
            handler: async function(val, oldVal) {
                if (Math.min(...this.percStatusItemTargets) === 1) {
                    await this.sleep(10000)
                    const { store } = this.$nuxt.context
                    store.commit('status/CLEAR_STATUS_ITEM_TARGETS')
                }
            },
        },
        percStatusVatNumberTargets: {
            handler: async function(val, oldVal) {
                if (Math.min(...this.percStatusVatNumberTargets) === 1) {
                    await this.sleep(10000)
                    const { store } = this.$nuxt.context
                    store.commit('status/CLEAR_STATUS_VAT_NUMBER_TARGETS')
                }
            }
        },
        percStatusDistanceSaleTargets: {
            handler: async function(val, oldVal) {
                if (Math.min(...this.percStatusDistanceSaleTargets) === 1) {
                    await this.sleep(10000)
                    const { store } = this.$nuxt.context
                    store.commit('status/CLEAR_STATUS_DISTANCE_SALE_TARGETS')
                }
            }
        },
        percStatusTransactionInputTargets: {
            handler: async function(val, oldVal) {
                if (Math.min(...this.percStatusTransactionInputTargets) === 1) {
                    await this.sleep(5000)
                    const { store } = this.$nuxt.context
                    store.commit('status/CLEAR_STATUS_TRANSACTION_INPUT_TARGETS')
                }
            }
       },
    //    doneStatusAccountTargets (newV, oldV) {
    //         if (newV === true) {
    //             await this.sleep(10000)
    //             const { store } = this.$nuxt.context
    //             store.commit('status/CLEAR_STATUS_ACCOUNT_TARGETS')
    //         }
    //     },

    //     doneStatusItemTargets (newV, oldV) {
    //         if (newV === true) {
    //             await this.sleep(10000)
    //             const { store } = this.$nuxt.context
    //             store.commit('status/CLEAR_STATUS_ITEM_TARGETS')
    //         }
    //     },

    //     doneStatusVatNumberTargets (newV, oldV) {
    //         if (newV === true) {
    //             await this.sleep(10000)
    //             const { store } = this.$nuxt.context
    //             store.commit('status/CLEAR_STATUS_VAT_NUMBER_TARGETS')
    //         }
    //     },

    //     doneStatusDistanceSaleTargets (newV, oldV) {
    //         if (newV === true) {
    //             await this.sleep(10000)
    //             const { store } = this.$nuxt.context
    //             store.commit('status/CLEAR_STATUS_DISTANCE_SALE_TARGETS')
    //         }
    //     },

    //     doneStatusTransactionInputTargets (newV, oldV) {
    //         if (newV === true) {
    //             await this.sleep(5000)
    //             const { store } = this.$nuxt.context
    //             store.commit('status/CLEAR_STATUS_TRANSACTION_INPUT_TARGETS')
    //         }
    //     }
        /*eslint-disable */

    }


}
</script>

<style>

</style>
