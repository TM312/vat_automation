<template>
    <div>
        <b-card
            v-if="transactionInputs.length === 0 && channelCode"
            sub-title="No transaction have been registered for this channel."
            class="text-center py-5"
        ></b-card>
        <b-table v-else :fields="fieldsBundle" :items="transactionInputs" hover>

            <template v-slot:cell(transaction_type_public_code)="data">
                <nuxt-link :to="`/tax/transactions/${data.item.public_id}`">{{ data.value }}</nuxt-link>
            </template>

            <template v-slot:cell(processed)="data" class="align-center">
                <b-icon v-if="data.value" icon="check-circle" variant="success"></b-icon>
                <span v-else><button-validate-transaction-input :transactionInputPublicId="data.item.public_id"/></span>
            </template>

            <template v-slot:cell(sale_total_value_gross)="data">
                <span v-if="data.value === null"></span>
                <span v-else>{{ data.value }} {{ data.item.currency_code }}</span>
            </template>

            <template v-slot:head(departure_to_arrival)>
                <b-row no-gutters class="justify-content-md-center">
                    <b-col class="text-right">Departure</b-col>
                    <b-col cols="2" class="text-center"><b-icon icon="arrow-right" /></b-col>
                    <b-col class="text-left">Arrival</b-col>
                </b-row>
            </template>

            <template v-slot:cell(departure_to_arrival)="data">
                <b-row no-gutters class="justify-content-md-center">
                    <b-col class="text-right">{{ data.item.departure_country_code }}</b-col>
                    <b-col v-if="data.item.departure_country_code || data.item.arrival_country_code" cols="2" class="text-center"><b-icon icon="arrow-right" /></b-col>
                    <b-col class="text-left">{{ data.item.arrival_country_code }}</b-col>
                </b-row>
            </template>


        </b-table>
    </div>
</template>

<script>

import { mapState } from 'vuex'

export default {
    name: 'TableTransactionInputsChannel',

    props: {
        // eslint-disable-next-line
        channelCode: {
            type: String,
            required: false

        }

    },

    data() {
        return {
            fieldsBundle: [
                 {
                    key: 'complete_date',
                    sortable: false,
                },
                {
                    key: 'transaction_type_public_code',
                    label: 'Public Type',
                    sortable: false,
                    formatter: value => {return this.capitalize(value)},
                },
                {
                    key: 'item_sku',
                    label: 'SKU',
                    sortable: false,
                },
                {
                    key:'given_id',
                    label: 'Transaction ID',
                    sortable: false
                },
                {
                    key: 'marketplace',
                    sortable: false,
                },
                {
                    key: 'item_quantity',
                    label: 'Quantity',
                    sortable: false,
                },
                 {
                    key: 'sale_total_value_gross',
                    label: 'Total Value Gross',
                    formatter: value => {
                            return value ? Number.parseFloat(value).toFixed(2) : null
                    },
                    sortable: false,
                },
                {
                    key: 'departure_to_arrival',
                    // label: 'Departure Country',
                    sortable: false,
                },
                // {
                //     key: 'arrival_country_code',
                //     label: 'Arrival Country',
                //     sortable: true,
                // },
                // {
                //     key: 'arrival_date',
                //     sortable: true,
                // },

                {
                    key: 'processed',
                    sortable: false,
                },

            ]
        }
    },

    computed: {
        ...mapState({
            transaction_inputs_full: state => state.transaction_input.transaction_inputs,
            countries: state => state.country.countries
        }),

        transactionInputs() {
            return this.channelCode ? this.transaction_inputs_full.filter(transaction_input => transaction_input.channel_code === this.channelCode) : this.transaction_inputs_full
        },

    },
    // methods: {
    //     codeToName(countryCode) {
    //         return this.countries.find(country => country.code == countryCode).name
    //     },

    // },

}
</script>

<style>

</style>
