<template>
    <div></div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: 'ToastNewTaxRecord',


    computed: {
        ...mapState({
            statusTaxRecordTargets: state => state.status.tax_record_targets,
            statusTaxRecordTarget: state => state.status.tax_record_target
        }),
        lenStatusTaxRecords() {
            return this.statusTaxRecordTargets.length
        }

    },

    watch: {
        // https://stackoverflow.com/questions/43270159/vue-js-2-how-to-watch-store-values-from-vuex
        /*eslint-disable */

        lenStatusFile (newLength, oldLength) {
            if (oldLength === 0) {
            this.makeToast()
            }
        /*eslint-disable */

        }
    },

    beforeDestroy() {
        this.resetStatusTaxRecord()
    },

    methods: {
        makeToast() {
            this.$store.commit('status/POP_STATUS_TAX_RECORD_TARGETS')

            this.$bvToast.toast(this.statusTaxRecordTarget.message, {
            title: 'New Tax Record',
            variant: this.statusTaxRecordTargets.status,
            autoHideDelay: 10000,
            })
        },
        resetStatusTaxRecord() {
            this.$store.commit('status/CLEAR_STATUS_TAX_RECORD_TARGETS')
        }
    }
}
</script>
