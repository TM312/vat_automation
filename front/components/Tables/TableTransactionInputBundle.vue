<template>
    <div>
        <h1>transactionInputs: {{ transactionInputsBundle }}</h1>
        <b-table :fields="fields" :items="transactionInputsBundle" hover :busy="$fetchState.pending && !transactionInputsBundle">
            <template v-slot:table-busy>
                <div class="text-center text-secondary my-2">
                    <b-spinner class="align-middle"></b-spinner>
                    <strong>Loading...</strong>
                </div>
            </template>

            <template v-slot:cell(transaction_type_public_code)="data">
                <nuxt-link
                    v-if="data.item.public_id != $route.params.public_id"
                    :to="`/tax/transactions/${data.item.public_id}`"
                >{{ data.value }}</nuxt-link>
                <span v-else>{{ data.value }}</span>
            </template>

            <template v-slot:cell(processed)="data">
                <b-icon v-if="data.value" icon="check-circle" variant="success"></b-icon>
                <span v-else><button-validate-transaction-input :transactionInputPublicId="data.item.public_id"/></span>
            </template>

            <template v-slot:cell(sale_total_value_gross)="data">
                <span v-if="data.value === null"></span>
                <span v-else>{{ data.value }} {{ data.item.currency_code }}</span>
            </template>

        </b-table>
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: 'TableTransactionInputBundle',

    props: {
        bundlePublicId: {
            type: String,
            required: true
        }
    },

    data() {
        return {
            fields: [
                 {
                    key: 'complete_date',
                    sortable: true,
                },
                {
                    key: 'transaction_type_public_code',
                    label: 'Public Type',
                    sortable: true,
                },
                {
                    key: 'item_sku',
                    label: 'SKU',
                    sortable: true,
                },
                {
                    key: 'marketplace',
                    sortable: true,
                },
                {
                    key: 'item_quantity',
                    label: 'Quantity',
                    sortable: true,
                },
                {
                    key: 'sale_total_value_gross',
                    label: 'Total Value Gross',
                    formatter: value => {
                            return value ? Number.parseFloat(value).toFixed(2) : null
                    },
                    sortable: true,
                },
                {
                    key: 'departure_country_code',
                    lable: 'Departure Country',
                    sortable: true,
                },
                {
                    key: 'arrival_country_code',
                    lable: 'Arrival Country',
                    sortable: true,
                },

                {
                    key: 'processed',
                    sortable: false,
                },

            ]
        }
    },

    async fetch() {
        if (this.transactionInputsBundle.length === 0) {
            const { store } = this.$nuxt.context;
            await store.dispatch("transaction_input/get_by_bundle_public_id", this.bundlePublicId);
        }
    },

    computed: {
        ...mapState({
            transactionInputsBundle: state => state.transaction_input.transaction_inputs_bundle
        })
    }
}
</script>

<style>

</style>
