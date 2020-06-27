<template>
    <b-container fluid>
        <div class="row">
            <card-tax-auditor :taxAuditor="self" />
        </div>
        <hr />
    </b-container>
</template>

<script>
    // import { mapState } from "vuex";

    export default {
        layout: "tax",
        middleware: "auth-tax",


        // async fetch({ store }) {
        //     await store.dispatch("tax_auditor/get_self");
        // },

        computed: {
            // ...mapState({
            //     self: state => {
            //         return state.tax_auditor.self_tax_auditor;
            //     }
            // }),
            self() {
                return this.$auth.user;
            }
        }
    };
</script>

<style>
</style>
