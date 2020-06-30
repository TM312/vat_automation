<template>
    <b-table :fields="fields" :items="employees" hover />

</template>

<script>
import { mapState } from "vuex";

export default {
    name: 'TableColleaguesTax',

    data() {
        return {
            colleagues: [
                {
                    'name': '',
                    'role': '',
                    'last_seen': '',
                    'registered_on': ''
                }
            ],

            fields: [
                {
                    key: 'name',
                    sortable: true
                },
                {
                    key: 'role',
                    sortable: true,
                    formatter: (value) => {
                        return value.replace(/\b\w/g, c => c.toUpperCase());
                    }
                },
                {
                    key: 'last_seen',
                    sortable: true,
                    formatter: (value, key, item) => {
                        return new Date(item.last_seen).toLocaleString();
                    }
                },
                {
                    key: 'registered_on',
                    sortable: true
                }
            ],
        }
    },

    computed: {
        ...mapState({
            employees: state => state.accounting_firm.accounting_firm.employees
        }),


    }
}
</script>

<style>

</style>
