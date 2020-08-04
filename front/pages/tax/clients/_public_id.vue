<template>
    <div>
        <b-row align-h="start">
            <b-col cols="auto"><container-route-back /></b-col>
            <b-col><h3 class="text-muted text-center">{{ seller_firm.name }}</h3></b-col>
        </b-row>
        <hr>
        <b-container fluid>
            <b-tabs pills card vertical>
                <b-tab title='Overview' active>
                    <overview-base-data-loading v-if="$fetchState.pending && (seller_firm.public_id != $route.params.public_id || seller_firm.length === 0)" />
                    <overview-base-data v-else />
                </b-tab>

                <b-tab title='Tax Records'>
                    <lazy-overview-tax-records :business="seller_firm" />
                </b-tab>
                <b-tab title='Upload Files' :disabled="$fetchState.pending && seller_firm.public_id != $route.params.public_id || seller_firm.length === 0">
                    <lazy-add-data-files :seller_firm_public_id="seller_firm.public_id" />
                </b-tab>

            </b-tabs>
        </b-container>
    </div>
</template>

<script>
    import { mapState } from 'vuex'
    export default {
        layout: "tax",
        middleware: "auth-tax",

        async fetch() {
            const { store } = this.$nuxt.context
            if (this.seller_firm.length == 0 || this.seller_firm.public_id !== this.$route.params.public_id) {
                await store.dispatch('seller_firm/get_by_public_id', this.$route.params.public_id)
            }
        },

        computed: {
            ...mapState({
                seller_firm: state => state.seller_firm.seller_firm
            }),
        }
    };
</script>

<style></style>
