<template>
    <div>
        <b-container class="my-2" fluid>
            <nuxt-link to="/tax/clients" ><b-icon icon="arrow-left" /> Back To Clients</nuxt-link>
        </b-container>
        <b-card no-body>
            <b-tabs pills card vertical>
                <b-tab title='Base Data' active>
                    <overview-base-data :client="client" />
                </b-tab>
                <b-tab title='Tax Records'>
                    <overview-tax-records :client="client" />
                </b-tab>
                <b-tab title='Transactions'>
                    <p>tbd</p>
                    <!-- <p>{{ $route }}</p> -->
                </b-tab>

            </b-tabs>
        </b-card>
    </div>
</template>

<script>
    import { BIcon } from "bootstrap-vue";



    export default {
        layout: "tax",
        middleware: "auth-tax",
        components: {
            BIcon
        },

        data() {
            return {
                public_id: this.$route.params.public_id,
            };
        },

        async fetch({ store }) {
            await store.dispatch("item/get_self");
        },

        computed: {
            client() {
                return this.$store.getters['seller_firm/client_by_public_id'](this.public_id)
            }
        }
    };
</script>

<style></style>
