<template>
    <b-tabs content-class="mt-3">
        <b-tab title="Company Data" active>
            <b-row>
                <b-col><card-client :business="business" class="mb-5"/></b-col>
                <b-col><card-vat-numbers :vat_numbers="vat_numbers" class="mb-5"/></b-col>
            </b-row>
            <b-row>
                <b-col><card-accounts :accounts="accounts" class="mb-5"/></b-col>
                <b-col><card-distance-sales :distance_sales="distance_sales" class="mb-5"/></b-col>
            </b-row>


        </b-tab>
        <b-tab title="Items">
            <card-items :items="items" class="mb-5"/>
        </b-tab>
    </b-tabs>
</template>

<script>
    import { mapState } from "vuex";

    export default {
        name:'OverviewBaseData',
        props: {
            business: {
                type: [Array, Object],
                required: true
            }
        },
        data() {
            return {
                distance_sales: [
                    { age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
                    { age: 21, first_name: 'Larsen', last_name: 'Shaw' },
                    { age: 89, first_name: 'Geneva', last_name: 'Wilson' },
                    { age: 38, first_name: 'Jami', last_name: 'Carney' }
                ],
                items: [
                    { age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
                    { age: 21, first_name: 'Larsen', last_name: 'Shaw' },
                    { age: 89, first_name: 'Geneva', last_name: 'Wilson' },
                    { age: 38, first_name: 'Jami', last_name: 'Carney' }
                ],
                // accounts: [
                //     { age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
                //     { age: 21, first_name: 'Larsen', last_name: 'Shaw' },
                //     { age: 89, first_name: 'Geneva', last_name: 'Wilson' },
                //     { age: 38, first_name: 'Jami', last_name: 'Carney' }
                // ],
                vat_numbers: [
                    { age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
                    { age: 21, first_name: 'Larsen', last_name: 'Shaw' },
                    { age: 89, first_name: 'Geneva', last_name: 'Wilson' },
                    { age: 38, first_name: 'Jami', last_name: 'Carney' }
                ]
            }
        },

        computed: {
            ...mapState({
                // items: state => state.seller_firm.seller_firm.items,
                // distance_sales: state => state.seller_firm.seller_firm.distance_sales,
                accounts: state => state.seller_firm.seller_firm.accounts,
                // vat_numbers: state => state.seller_firm.seller_firm.vat_numbers,
            }),
        }
    }
</script>

<style>
</style>
