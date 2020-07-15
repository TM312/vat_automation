<template>
    <b-table :fields="fields" :items="employees" hover />

</template>

<script>
import { mapState } from "vuex";

export default {
    name: 'TableColleaguesTax',

    data() {
        return {
            fields: [
                {
                    key: 'name',
                    sortable: true
                },
                {
                    key: 'role',
                    sortable: true,
                    formatter: (value) => {
                        return value.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
                    }
                },
                {
                    key: 'last_seen',
                    sortable: true,
                    formatter: (value, key, item) => {
                        return this.$dateFns.formatDistanceToNow(new Date(item.last_seen))
                        // this.$dateFns.format(new Date(), 'yyyy-MM-dd')
                        // return new Date(item.last_seen).toLocaleString();
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
