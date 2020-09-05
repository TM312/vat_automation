<template>
    <div>
        <b-toast
            id='toastAccount'
            :title="statusAccount.title"
            :variant="statusAccount.variant"
            :auto-hide-delay="Math.max(10000, statusAccount.total * 500)"
        >
            <b-progress :value="statusAccount.current" :max="statusAccount.total" animated></b-progress>
        </b-toast>

        <b-toast
            id='toastItem'
            :title="statusItem.title"
            :variant="statusItem.variant"
            :auto-hide-delay="Math.max(10000, statusItem.total * 500)"
        >
            <b-progress :value="statusItem.current" :max="statusItem.total" animated></b-progress>
        </b-toast>

        <b-toast
            id='toastVatNumber'
            :title="statusVatNumber.title"
            :variant="statusVatNumber.variant"
            :auto-hide-delay="Math.max(10000, statusVatNumber.total * 500)"
        >
            <b-progress :value="statusVatNumber.current" :max="statusVatNumber.total" animated></b-progress>
        </b-toast>

        <b-toast
            id='toastDistanceSale'
            :title="statusDistanceSale.title"
            :variant="statusDistanceSale.variant"
            :auto-hide-delay="Math.max(10000, statusDistanceSale.total * 500)"
        >
            <b-progress :value="statusDistanceSale.current" :max="statusDistanceSale.total" animated></b-progress>
        </b-toast>
    </div>

</template>

<script>
import { mapState } from 'vuex'

export default {
    name: 'ToastsStaticDataUpload',

    computed: {
        ...mapState({
            sellerFirm: state => state.seller_firm.seller_firm,

            statusAccount: state => state.status.status_account,
            lenStatusAccount: state => state.status.status_account.length,

            statusItem: state => state.status.status_item,
            lenStatusItem: state => state.status.status_item.length,

            statusVatNumber: state => state.status.status_vat_number,
            lenStatusVatNumber: state => state.status.status_vat_number.length,

            statusDistanceSale: state => state.status.status_distance_sale,
            lenStatusDistanceSale: state => state.status.status_distance_sale.length
        }),

    },

    watch: {
        // https://stackoverflow.com/questions/43270159/vue-js-2-how-to-watch-store-values-from-vuex
        /*eslint-disable */

        lenStatusAccount (newLength, oldLength) {
            this.$bvToast.show('toastAccount')
        },
        lenStatusItem (newLength, oldLength) {
            this.$bvToast.show('toastItem')
        },
        lenStatusVatNumber (newLength, oldLength) {
            this.$bvToast.show('toastVatNumber')
        },
        lenStatusDistanceSale (newLength, oldLength) {
            this.$bvToast.show('toastDistanceSale')
        }
        /*eslint-disable */

    },


}
</script>

<style>

</style>
