<template>
    <b-table :fields="fields" :items="clients" hover />
    <!-- <nuxt-link :to="business.public_id" append>Details <b-icon icon="arrow-right" /></nuxt-link> -->

</template>

<script>
import { mapState } from "vuex";

export default {
    name: 'TableClientsTax',

    data() {
        return {

            fields: [
                {
                    key: 'name',
                    sortable: true
                },
                {
                    key: 'address',
                    sortable: false
                },
                {
                    key: 'created_on',
                    sortable: true
                },
                {
                    key: 'created_by',
                    sortable: true
                },
                {
                    key: 'public_id',
                    sortable: false
                }
            ],
        }
    },

    computed: {
        ...mapState({
            clients: state => state.accounting_firm.accounting_firm.clients
        }),
    }
}
</script>

<style>

</style>
