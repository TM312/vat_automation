<template>
    <b-container fluid>
        <div>Notifications</div>
        <div class="row">
            <ul>
                <li>Public ID: {{ user.public_id }}</li>
                <li>Email: {{ user.email }}</li>
                <li>Test: {{ $auth.user.id }}</li>
            </ul>
        </div>
        <div class="row">
            <!-- <tax-auditor v-for="(tax_auditor, i) in tax_auditors" :key="i" :taxAuditor="tax_auditor" /> -->
            <tax-auditor :taxAuditor="tax_auditor" />
        </div>
        <!-- <p>{{ tax_auditor.email }}</p> -->
        <hr />
        <DashboardMetrics />
    </b-container>
</template>

<script>
    import { mapState } from "vuex";

    export default {
        layout: "tax",

        async fetch({ store }) {
            await store.dispatch("tax_auditor/get_by_id", 2);
        },

        computed: {
            ...mapState({
                tax_auditor: state => {
                    return state.tax_auditor.tax_auditor;
                }
            }),
            user() {
                return this.$auth.user;
            }
        }
    };
</script>

<style>
</style>
