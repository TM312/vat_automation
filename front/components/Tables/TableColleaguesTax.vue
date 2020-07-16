<template>
    <b-table :fields="fields" :items="employees" :busy="$fetchState.pending && !accountingFirm" hover>
        <template v-slot:table-busy>
            <div class="text-center text-secondary my-2">
                <b-spinner class="align-middle"></b-spinner>
                <strong>Loading...</strong>
            </div>
        </template>
    </b-table>

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
                    formatter: value => {
                        return value.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
                    }
                },
                {
                    key: 'last_seen',
                    sortable: true,
                    formatter: (value, key, item) => {
                        return this.$dateFns.formatDistanceToNow(new Date(item.last_seen))
                    }
                },
                {
                    key: 'registered_on',
                    sortable: true
                }
            ],
        }
    },

    async fetch() {
        const { store } = this.$nuxt.context
        await store.dispatch("accounting_firm/get_by_public_id", this.$auth.user.employer_public_id);
    },


    computed: {
        ...mapState({
            employees: state => state.accounting_firm.accounting_firm.employees,
            accountingFirm: state => state.accounting_firm
        }),


    }
}
</script>

<style>

</style>
