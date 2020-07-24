<template>
    <div>
        <b-table :fields="fields" :items="transactionInputs" hover :busy="$fetchState.pending && !transactionInputs">
            <template v-slot:table-busy>
                <div class="text-center text-secondary my-2">
                    <b-spinner class="align-middle"></b-spinner>
                    <strong>Loading...</strong>
                </div>
            </template>

            <template v-slot:cell(activity_id)="data">

                <nuxt-link v-if="data.item.public_id != $route.params.public_id" :to="`/tax/transactions/${data.item.public_id}`" >{{ data.value }}</nuxt-link>
                <span v-else>{{ data.value }}</span>
            </template>

            <template v-slot:cell(processed)="data">
                <b-button size="sm" variant="outline-primary">Validate</b-button><br>
                {{ data.value }}
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
                    key: 'activity_id',
                    sortable: true,
                },
                {
                    key: 'marketplace',
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
                    key: 'item_quantity',
                    label: 'Quantity',
                    sortable: true,
                },
                {
                    key: 'sale_total_value_gross',
                    label: 'Total Value (gross)',
                    sortable: true,
                },
                {
                    key: 'currency_code',
                    label: 'Currency',
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
                    key: 'arrival_date',
                    sortable: true,
                },
                {
                    key: 'complete_date',
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
            const { store } = this.$nuxt.context;
            console.log('in component: this.bundlePublicId -> ', this.bundlePublicId)
            await store.dispatch("bundle/get_by_public_id", this.bundlePublicId);
        },

    computed: {
        ...mapState({
            transactionInputs: state => state.bundle.bundle.transaction_inputs
        })
    }
}
</script>

<style>

</style>
