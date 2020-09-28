<template>
    <div>
        <container-route-back />
        <b-container fluid v-if="!$fetchState.pending && transactionInput.length != 0">
            <b-alert :show="!transactionInput.processed" variant="danger">
                <p>The transaction has not been processed yet due to network errors. Click here to retry: <button-validate-transaction-input :transactionInputPublicId="transactionInput.public_id"/> </p>
            </b-alert>

            <!-- <b-row>
                <b-col cols="1">
                    <b-nav pills vertical v-b-scrollspy:nav-scroller>
                        <b-nav-item to="#file" :active="$route.hash === '#file' || $route.hash === ''">Input File</b-nav-item>
                        <b-nav-item to="#bundle" :active="$route.hash === '#bundle'">Transaction Bundle</b-nav-item>
                        <b-nav-item to="#tax" :active="$route.hash === '#tax'">Tax Processes</b-nav-item>
                    </b-nav>
                </b-col>
                <b-col id="nav-scroller" cols="11">
                    <div class="tab-content">
                        <div :class="['tab-pane', { 'active': $route.hash === '#' || $route.hash === '' || $route.hash === '#file' }]">
                            <card-transaction-input id="file" />
                        </div>
                        <hr>
                        <div :class="['tab-pane', { 'active': $route.hash === '#bundle' }]">
                            <table-transaction-input-bundle id="bundle" :bundlePublicId="transactionInput.bundle_public_id"/>
                        </div>
                        <hr>
                        <div :class="['tab-pane', { 'active': $route.hash === '#tax' }]">
                            <view-transactions id="tax" :transactions="transactionInput.transactions" />
                        </div>
                    </div>
                </b-col>
            </b-row> -->


            <b-card class="mb-1">
                <b-card-title>
                    <b-row>
                        <b-col cols="auto" class="mr-auto">Input File</b-col>
                        <b-col cols="auto">
                            <b-button v-b-toggle.collapse-file size="sm" variant="outline-secondary"><b-icon :icon="iconCollapseFile" /></b-button>
                        </b-col>
                    </b-row>
                </b-card-title>
                <b-collapse id="collapse-file" visible v-model="fileCollapse">
                    <b-card-body>
                        <card-transaction-input id="file"/>
                    </b-card-body>
                </b-collapse>
            </b-card>

            <b-card class="mb-1">
                <b-card-title>
                    <b-row>
                        <b-col cols="auto" class="mr-auto">Transaction Bundle</b-col>
                        <b-col cols="auto">
                            <b-button v-b-toggle.collapse-bundle size="sm" variant="outline-secondary"><b-icon :icon="iconCollapseBundle" /></b-button>
                        </b-col>
                    </b-row>
                </b-card-title>
                <b-card-sub-title>A list of all related transactions</b-card-sub-title>
                <b-collapse id="collapse-bundle" visible v-model="bundleCollapse">
                    <b-card-body>
                        <table-transaction-input-bundle :bundlePublicId="transactionInput.bundle_public_id"/>
                    </b-card-body>
                </b-collapse>
            </b-card>

            <b-card class="mb-1">
                <b-card-title>
                     <b-row>
                        <b-col cols="auto" class="mr-auto">Tax Processes</b-col>
                        <b-col cols="auto">
                            <b-button v-b-toggle.collapse-tax size="sm" variant="outline-secondary"><b-icon :icon="iconCollapseTax" /></b-button>
                        </b-col>
                    </b-row>
                </b-card-title>
                <b-collapse id="collapse-tax" visible v-model="taxCollapse">
                    <b-card-body>
                        <view-transactions :transactions="transactionInput.transactions" />
                    </b-card-body>
                </b-collapse>
            </b-card>

            <b-alert :show="transactionInput.processed" variant="info">
                <p>The transaction has been successfully processed on {{ new Date(transactionInput.processed_on).toLocaleString() }} </p>
            </b-alert>

        </b-container>
    </div>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        layout: "tax",
        middleware: "auth-tax",

        data() {
            return {
                fileCollapse: true,
                bundleCollapse: true,
                taxCollapse: true
            }
        },

        async fetch() {
            const { store } = this.$nuxt.context
            await store.dispatch('transaction_input/get_by_public_id', this.$route.params.public_id);

        },

        computed: {
            ...mapState({
                transactionInput: state => state.transaction_input.transaction_input,
            }),

            iconCollapseFile() {
                return this.fileCollapse ? 'arrows-angle-contract' : 'arrows-angle-expand'
            },
            iconCollapseBundle() {
                return this.bundleCollapse ? 'arrows-angle-contract' : 'arrows-angle-expand'
            },
            iconCollapseTax() {
                return this.taxCollapse ? 'arrows-angle-contract' : 'arrows-angle-expand'
            }
        },


    };
</script>

<style></style>
