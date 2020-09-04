<template>
    <div>
        <b-row align-h="start">
            <b-col cols="auto"><container-route-back /></b-col>
            <b-col><h3 class="text-muted text-center">{{ sellerFirm.name }}</h3></b-col>
        </b-row>
        <hr>
        <b-container fluid>
            <b-tabs pills card vertical>
                <b-tab title='Overview' active>
                    <overview-base-data-loading v-if="$fetchState.pending && (sellerFirm.public_id != $route.params.public_id || sellerFirm.length === 0)" />
                    <overview-base-data v-else />
                </b-tab>

                <b-tab title='Tax Records' :disabled="$fetchState.pending && sellerFirm.public_id != $route.params.public_id || sellerFirm.length === 0">
                    <span v-if="$fetchState.pending && (sellerFirm.public_id != $route.params.public_id || sellerFirm.length === 0)"></span>
                    <lazy-overview-tax-records v-else :business="sellerFirm" />
                </b-tab>
                <b-tab title='Upload Files' :disabled="$fetchState.pending && sellerFirm.public_id != $route.params.public_id || sellerFirm.length === 0">
                    <lazy-add-data-files :seller_firm_public_id="sellerFirm.public_id" />
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
            if (this.sellerFirm.length == 0 || this.sellerFirm.public_id !== this.$route.params.public_id) {
                await store.dispatch('seller_firm/get_by_public_id', this.$route.params.public_id)
            }
        },

        computed: {
            ...mapState({
                sellerFirm: state => state.seller_firm.seller_firm,
                status_account: state => state.status.status_account,
                status_item: state => state.status.status_item,
                status_vat_number: state => state.status.status_vat_number,
                status_distance_sale: state => state.status.status_distance_sale
            }),

        },

        watch: {
          displayToast() {
                if (this.status_account > 0) {
                    this.makeToast(this.status_account.current, this.status_account.total, this.status_account.object, this.status_account.title)
                } else if (this.status_item > 0) {
                    this.makeToast(this.status_item.current, this.status_item.total, this.status_item.object, this.status_item.title)
                } else if (this.status_vat_number > 0) {
                    this.makeToast(this.status_vat_number.current, this.status_vat_number.total, this.status_vat_number.object, this.status_vat_number.title)
                } else if (this.status_distance_sale > 0) {
                    this.makeToast(this.status_distance_sale.current, this.status_distance_sale.total, this.status_distance_sale.object, this.status_distance_sale.title)
                }
            }
        },

        mounted() {
            this.socket = this.$nuxtSocket({
                name: 'home',
                reconnection: false
            })
        },

        methods: {
            makeToast(current, total, object, title) {
                this.$bvToast.toast(`${parseInt(current/total * 100)}% : ${current} out of ${total} ${object}s have been added.`, {
                title: title,
                variant: 'success',
                autoHideDelay: 15000,
                appendToast: false
                })
            }
        }

    };
</script>

<style></style>
