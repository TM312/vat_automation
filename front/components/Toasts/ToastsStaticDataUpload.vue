<template>
    <div>
        <toast-data-upload-invalid-file />
        <b-toast
            no-auto-hide
            :title="titleAccount"
            :variant="doneStatusAccountTargets ? 'success' : ''"
            v-model="toastAccount"
        >
            <div v-for="(accountTarget, i) in statusAccountTargets" :key="i" class="pt-2">
                <div v-if="accountTarget.target !== 'errorbox' && accountTarget.target !== 'infobox'">
                    <div v-if="statusAccountTargets[i].done">
                        <b-row no-gutters>
                            <b-col cols="1"><b-icon icon="check-circle" variant="success" /></b-col>
                            <b-col cols="11"><p lead>{{statusAccountTargets[i].message }}</p></b-col>
                        </b-row>

                    </div>

                    <div v-else>
                        <b-progress :value="statusAccountTargets[i].current" :max="statusAccountTargets[i].total" animated></b-progress>
                    </div>
                    <small class="text-muted mt-1">Source: <i>{{ statusAccountTargets[i].target }}</i></small>
                </div>

                <div v-else-if="accountTarget.target === 'errorbox'">
                    <b-card border-variant="danger">
                        <b-card-text>{{ accountTarget.message }}</b-card-text>
                    </b-card>
                </div>

                <div v-else-if="accountTarget.target === 'infobox'">
                    <b-card border-variant="info">
                        <b-card-text>
                            {{ accountTarget.message }}
                            <span v-if="doneStatusAccountTargets && accountTarget.duplicate_list && accountTarget.duplicate_list.length > 2">
                                <b-icon v-b-modal.account-duplicates icon="info-circle" variant="outline-info" class="ml-1"/>
                                <b-modal id="account-duplicates" title="Account Duplicates">
                                    <ul>
                                        <li v-for="(duplicate, index) in accountTarget.duplicate_list" :key="index">{{ duplicate}}</li>
                                    </ul>
                                </b-modal>
                            </span>
                        </b-card-text>
                    </b-card>
                </div>

                <hr v-if="statusAccountTargets.length > 1">

            </div>
        </b-toast>

        <b-toast
            no-auto-hide
            :title="titleItem"
            :variant="doneStatusItemTargets ? 'success' : ''"
            v-model="toastItem"
        >
            <div v-for="(itemTarget, i) in statusItemTargets" :key="i" class="pt-2">
                <div v-if="itemTarget.target !== 'errorbox' && itemTarget.target !== 'infobox'">
                    <div v-if="statusItemTargets[i].done">
                        <b-row no-gutters>
                            <b-col cols="1"><b-icon icon="check-circle" variant="success" /></b-col>
                            <b-col cols="11"><p lead>{{statusItemTargets[i].message }}</p></b-col>
                        </b-row>

                    </div>

                    <div v-else>
                        <b-progress :value="statusItemTargets[i].current" :max="statusItemTargets[i].total" animated></b-progress>
                    </div>
                    <small class="text-muted mt-1">Source: <i>{{ statusItemTargets[i].target }}</i></small>
                </div>

                <div v-else-if="itemTarget.target === 'errorbox'">
                    <b-card border-variant="danger">
                        <b-card-text>{{ itemTarget.message }}</b-card-text>
                    </b-card>
                </div>

                <div v-else-if="itemTarget.target === 'infobox'">
                    <b-card border-variant="info">
                        <b-card-text>
                            {{ itemTarget.message }}
                            <span v-if="doneStatusItemTargets && itemTarget.duplicate_list && itemTarget.duplicate_list.length > 2">
                                <b-icon v-b-modal.item-duplicates icon="info-circle" variant="outline-info" class="ml-1"/>
                                <b-modal id="item-duplicates" title="Item Duplicates">
                                    <ul>
                                        <li v-for="(duplicate, index) in itemTarget.duplicate_list" :key="index">{{ duplicate}}</li>
                                    </ul>
                                </b-modal>
                            </span>
                        </b-card-text>
                    </b-card>
                </div>

                <hr v-if="statusItemTargets.length > 1">

            </div>
        </b-toast>

        <b-toast
            no-auto-hide
            :title="titleVatNumber"
            :variant="doneStatusVatNumberTargets ? 'success' : ''"
            v-model="toastVatNumber"
        >
            <div v-for="(vatNumberTarget, i) in statusVatNumberTargets" :key="i" class="pt-2">
                <div v-if="vatNumberTarget.target !== 'errorbox' && vatNumberTarget.target !== 'infobox'">
                    <div v-if="statusVatNumberTargets[i].done">
                        <b-row no-gutters>
                            <b-col cols="1"><b-icon icon="check-circle" variant="success" /></b-col>
                            <b-col cols="11"><p lead>{{statusVatNumberTargets[i].message }}</p></b-col>
                        </b-row>

                    </div>

                    <div v-else>
                        <b-progress :value="statusVatNumberTargets[i].current" :max="statusVatNumberTargets[i].total" animated></b-progress>
                    </div>
                    <small class="text-muted mt-1">Source: <i>{{ statusVatNumberTargets[i].target }}</i></small>
                </div>

                <div v-else-if="vatNumberTarget.target === 'errorbox'">
                    <b-card border-variant="danger">
                        <b-card-text>{{ vatNumberTarget.message }}</b-card-text>
                    </b-card>
                </div>

                <div v-else-if="vatNumberTarget.target === 'infobox'">
                    <b-card border-variant="info">
                        <b-card-text>
                            {{ vatNumberTarget.message }}
                            <span v-if="doneStatusVatNumberTargets && vatNumberTarget.duplicate_list && vatNumberTarget.duplicate_list.length > 2">
                                <b-icon v-b-modal.vat-number-duplicates icon="info-circle" variant="outline-info" class="ml-1"/>
                                <b-modal id="vat-number-duplicates" title="Vat Number Duplicates">
                                    <ul>
                                        <li v-for="(duplicate, index) in vatNumberTarget.duplicate_list" :key="index">{{ duplicate}}</li>
                                    </ul>
                                </b-modal>
                            </span>
                        </b-card-text>
                    </b-card>
                </div>

                <hr v-if="statusItemTargets.length > 1">

            </div>
        </b-toast>

        <b-toast
            no-auto-hide
            :title="titleDistanceSale"
            :variant="doneStatusDistanceSaleTargets ? 'success' : ''"
            v-model="toastDistanceSale"
        >
            <div v-for="(distanceSaleTarget, i) in statusDistanceSaleTargets" :key="i" class="pt-2">
                <div v-if="distanceSaleTarget.target !== 'errorbox' && distanceSaleTarget.target !== 'infobox'">
                    <div v-if="statusDistanceSaleTargets[i].done">
                        <b-row no-gutters>
                            <b-col cols="1"><b-icon icon="check-circle" variant="success" /></b-col>
                            <b-col cols="11"><p lead>{{statusDistanceSaleTargets[i].message }}</p></b-col>
                        </b-row>

                    </div>

                    <div v-else>
                        <b-progress :value="statusDistanceSaleTargets[i].current" :max="statusDistanceSaleTargets[i].total" animated></b-progress>
                    </div>
                    <small class="text-muted mt-1">Source: <i>{{ statusDistanceSaleTargets[i].target }}</i></small>
                </div>

                <div v-else-if="distanceSaleTarget.target === 'errorbox'">
                    <b-card border-variant="danger">
                        <b-card-text>{{ distanceSaleTarget.message }}</b-card-text>
                    </b-card>
                </div>

                <div v-else-if="distanceSaleTarget.target === 'infobox'">
                    <b-card border-variant="info">
                        <b-card-text>
                            {{ distanceSaleTarget.message }}
                            <span v-if="doneStatusDistanceSaleTargets && distanceSaleTarget.duplicate_list && distanceSaleTarget.duplicate_list.length > 2">
                                <b-icon v-b-modal.distance-sale-duplicates icon="info-circle" variant="outline-info" class="ml-1"/>
                                <b-modal id="distance-sale-duplicates" title="Distance Sale Duplicates">
                                    <ul>
                                        <li v-for="(duplicate, index) in distanceSaleTarget.duplicate_list" :key="index">{{ duplicate}}</li>
                                    </ul>
                                </b-modal>
                            </span>
                        </b-card-text>
                    </b-card>
                </div>

                <hr v-if="statusItemTargets.length > 1">

            </div>
        </b-toast>

        <b-toast
            no-auto-hide
            :title="titleTransactionInput"
            :variant="doneStatusTransactionInputTargets ? 'success' : ''"
            v-model="toastTransactionInput"
        >
            <div v-for="(transactionInputTarget, i) in statusTransactionInputTargets" :key="i" class="pt-2">
                <div v-if="transactionInputTarget.target !== 'errorbox' && transactionInputTarget.target !== 'infobox'">
                    <div v-if="statusTransactionInputTargets[i].done">
                        <b-row no-gutters>
                            <b-col cols="1"><b-icon icon="check-circle" variant="success" /></b-col>
                            <b-col cols="11"><p lead>{{statusTransactionInputTargets[i].message }}</p></b-col>
                        </b-row>

                    </div>

                    <div v-else>
                        <b-progress :value="statusTransactionInputTargets[i].current" :max="statusTransactionInputTargets[i].total" animated></b-progress>
                    </div>
                    <small class="text-muted mt-1">Source: <i>{{ statusTransactionInputTargets[i].target }}</i></small>
                </div>

                <div v-else-if="transactionInputTarget.target === 'errorbox'">
                    <b-card border-variant="danger">
                        <b-card-text>{{ transactionInputTarget.message }}</b-card-text>
                    </b-card>
                </div>

                <div v-else-if="transactionInputTarget.target === 'infobox'">
                    <b-card border-variant="info">
                        <b-card-text>
                            {{ transactionInputTarget.message }}
                            <span v-if="doneStatusTransactionInputTargets && transactionInputTarget.duplicate_list && transactionInputTarget.duplicate_list.length > 2">
                                <b-icon v-b-modal.transaction-input-duplicates icon="info-circle" variant="outline-info" class="ml-1"/>
                                <b-modal id="transaction-input-duplicates" title="Transaction Duplicates">
                                    <ul>
                                        <li v-for="(duplicate, index) in transactionInputTarget.duplicate_list" :key="index">{{ duplicate}}</li>
                                    </ul>
                                </b-modal>
                            </span>
                        </b-card-text>
                    </b-card>
                </div>

                <hr v-if="statusItemTargets.length > 1">

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
            toastTransactionInput: false,
            toastSellerFirm: false
        }
    },

    computed: {
        ...mapState({
            // sellerFirm: state => state.seller_firm.seller_firm,

            statusAccountTargets: state => state.status.account_targets,
            lenStatusAccount: state => state.status.account_targets.length,

            statusItemTargets: state => state.status.item_targets,
            lenStatusItem: state => state.status.item_targets.length,

            statusVatNumberTargets: state => state.status.vat_number_targets,
            lenStatusVatNumber: state => state.status.vat_number_targets.length,

            statusDistanceSaleTargets: state => state.status.distance_sale_targets,
            lenStatusDistanceSale: state => state.status.distance_sale_targets.length,

            statusTransactionInputTargets: state => state.status.transaction_input_targets,
            lenStatusTransactionInput: state => state.status.transaction_input_targets.length,

        }),

        doneStatusAccountTargets() {
            return this.$store.getters['status/doneStatusAccountTargets']
        },
        doneStatusItemTargets() {
            return this.$store.getters['status/doneStatusItemTargets']
        },
        doneStatusVatNumberTargets() {
            return this.$store.getters['status/doneStatusVatNumberTargets']
        },
        doneStatusDistanceSaleTargets() {
            return this.$store.getters['status/doneStatusDistanceSaleTargets']
        },
        doneStatusTransactionInputTargets() {
            return this.$store.getters['status/doneStatusTransactionInputTargets']
        },

        totalStatusAccountTargets() {
            return this.$store.getters['status/totalStatusAccountTargets']
        },
        totalStatusItemTargets() {
            return this.$store.getters['status/totalStatusItemTargets']
        },
        totalStatusVatNumberTargets() {
            return this.$store.getters['status/totalStatusVatNumberTargets']
        },
        totalStatusDistanceSaleTargets() {
            return this.$store.getters['status/totalStatusDistanceSaleTargets']
        },
        totalStatusTransactionInputTargets() {
            return this.$store.getters['status/totalStatusTransactionInputTargets']
        },

        titleAccount() {
            if (this.doneStatusAccountTargets) {
                return (this.lenStatusAccount === 1) ? 'Uploaded accounts processed' : `${this.totalStatusAccountTargets} uploaded accounts processed`
            } else {
                return 'New accounts are being registered...'
            }
        },
        titleItem() {
            if (this.doneStatusItemTargets) {
                return (this.lenStatusItem === 1) ? 'Uploaded items processed' : `${this.totalStatusItemTargets} uploaded items processed`
            } else {
                return 'New items are being registered...'
            }
        },
        titleVatNumber() {
            if (this.doneStatusVatNumberTargets) {
                return (this.lenStatusVatNumber === 1) ? 'Uploaded vat numbers processed' : `${this.totalStatusVatNumberTargets} uploaded vat numbers processed`
            } else {
                return 'New items are being registered...'
            }
        },
        titleDistanceSale() {
            if (this.doneStatusDistanceSaleTargets) {
                return (this.lenStatusDistanceSale === 1) ? 'Uploaded distance sales processed' : `${this.totalStatusDistanceSaleTargets} uploaded distance sales processed`
            } else {
                return 'New distance sales are being registered...'
            }
        },
        titleTransactionInput() {
            if (this.doneStatusTransactionInputTargets) {
                return (this.lenStatusTransactionInput === 1) ? 'Uploaded transactions processed' : `${this.totalStatusTransactionInputTargets} uploaded transactions processed`
            } else {
                return 'New transactions are being registered...'
            }
        }

    },

    watch: {
        // https://stackoverflow.com/questions/43270159/vue-js-2-how-to-watch-store-values-from-vuex
        /*eslint-disable */

        lenStatusAccount (newLength, oldLength) {
            if (oldLength === 0) {
                this.toastAccount = true
            }
        },
        lenStatusItem (newLength, oldLength) {
            if (oldLength === 0) {
                this.toastItem = true
            }
        },
        lenStatusVatNumber (newLength, oldLength) {
            if (oldLength === 0) {
                this.toastVatNumber = true
            }
        },
        lenStatusDistanceSale (newLength, oldLength) {
            if (oldLength === 0) {
                this.toastDistanceSale = true
            }
        },
        lenStatusTransactionInput (newLength, oldLength) {
            if (oldLength === 0) {
                this.toastTransactionInput = true
            }
        },


        async doneStatusAccountTargets (val, oldVal) {
            if (val) {
                await this.sleep(11000)
                this.toastAccount = false
                await this.sleep(1000)
                const { store } = this.$nuxt.context
                store.commit('status/CLEAR_STATUS_ACCOUNT_TARGETS')
            }
        },
        async doneStatusItemTargets (val, oldVal) {
            if (val) {
                await this.sleep(11000)
                this.toastItem = false
                await this.sleep(1000)
                const { store } = this.$nuxt.context
                store.commit('status/CLEAR_STATUS_ITEM_TARGETS')
            }
        },
        async doneStatusVatNumberTargets (val, oldVal) {
            if (val) {
                await this.sleep(11000)
                this.toastVatNumber = false
                await this.sleep(1000)
                const { store } = this.$nuxt.context
                store.commit('status/CLEAR_STATUS_VAT_NUMBER_TARGETS')
            }
        },
        async doneStatusDistanceSaleTargets (val, oldVal) {
            if (val) {
                await this.sleep(11000)
                this.toastDistanceSale = false
                await this.sleep(1000)
                const { store } = this.$nuxt.context
                store.commit('status/CLEAR_STATUS_DISTANCE_SALE_TARGETS')
            }
        },
        async doneStatusTransactionInputTargets (val, oldVal) {
            if (val) {
                await this.sleep(11000)
                this.toastTransactionInput = false
                await this.sleep(1000)
                const { store } = this.$nuxt.context
                store.commit('status/CLEAR_STATUS_TRANSACTION_INPUT_TARGETS')
            }
       }

        /*eslint-disable */

    }


}
</script>
