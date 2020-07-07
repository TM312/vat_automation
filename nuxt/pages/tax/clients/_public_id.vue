<template>
    <div>
        <b-container class="my-2" fluid>
            <nuxt-link to="/tax/clients" ><b-icon icon="arrow-left" /> Back To Clients</nuxt-link>
        </b-container>
        <b-card no-body>
            <b-tabs pills card vertical>
                <b-tab title='Base Data' active @click="$fetch">
                    <overview-base-data-loading v-if="$fetchState.pending" />
                    <overview-base-data v-else />
                </b-tab>
                <b-tab title='Tax Records'>
                    <lazy-overview-tax-records :business="seller_firm" />
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
    import { mapState } from 'vuex'
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

            }
        },

        async fetch() {
            const { store } = this.$nuxt.context
            await store.dispatch('seller_firm/get_by_public_id', this.public_id);
        },

        computed: {
            ...mapState({
                seller_firm: state => state.seller_firm.seller_firm
            }),
        },
    };
</script>

<style></style>
