<template>
    <b-col class="px-1">
        <b-card :border-variant="getCardColor">
            <b-card-title>{{ business.name }}</b-card-title>
            <b-card-sub-title class="mt-1">{{ business.len_vat_numbers}} Vat Numbers</b-card-sub-title>

            <b-card-text class="pt-3">
                <b-form-row>
                    <b-col cols="auto"><b>Client ID:</b></b-col>
                    <b-col cols="auto" class="mr-auto">
                        <span v-if="business.accounting_firm_client_id">{{ business.accounting_firm_client_id }}</span>
                        <span v-else><i>No ID assigned</i></span>
                    </b-col>
                </b-form-row>
                <b-form-row>
                    <b-col cols="auto"><b>Address:</b></b-col>
                    <b-col cols="auto" class="mr-auto">{{ business.address  }}</b-col>
                </b-form-row>
            </b-card-text>
            <b-row cols="2">
                <b-col cols="auto" class="mr-auto"><nuxt-link :to="`clients/${business.public_id}`">Details</nuxt-link></b-col>
            </b-row>
        </b-card>
    </b-col>
</template>

<script>
    export default {
        name: 'CardClientShort',
        // eslint-disable-next-line
        props: { business: { type: [Array, Object] } },

        computed: {
            getCardColor() {
                return this.business.transaction_ready ? '' : 'danger'
            }
        },
    }
</script>
