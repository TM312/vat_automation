<template>
    <b-col>
        <b-card :border-variant="getCardColor">
            <b-card-title>{{ business.name }}</b-card-title>
            <b-card-sub-title class="mt-1">{{ business.len_vat_numbers}} Vat Numbers</b-card-sub-title>

            <b-card-text class="pt-3">
                <b-form-row><b-col cols="6" cols-lg="5" cols-xl="4"><b>Client ID:</b></b-col><b-col cols="6" cols-lg="7" cols-xl="8">{{ business.accounting_firm_client_id }}</b-col></b-form-row>
                <b-form-row><b-col cols="6" cols-lg="5" cols-xl="4"><b>Address:</b></b-col><b-col cols="6" cols-lg="7" cols-xl="8">{{ business.address  }}</b-col></b-form-row>
            </b-card-text>
            <b-row cols="2">
                <b-col cols="6" cols-lg="5" cols-xl="4"><nuxt-link :to="`clients/${business.public_id}`">Details</nuxt-link></b-col>
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
