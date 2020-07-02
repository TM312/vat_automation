<template>
    <b-col>
        <b-card :border-variant="getCardColor">
            <b-card-title>{{ business.name }}</b-card-title>
            <b-card-sub-title class="mt-1">{{ business.len_vat_numbers}} Vat Numbers</b-card-sub-title>

            <b-card-text class="pt-3">
                <b>Address:</b> {{ business.address  }} <br>
                <b>Created On:</b> {{ business.created_on }} <br>
                <b>Created By:</b> {{ business.created_by }}
            </b-card-text>
            <nuxt-link :to="business.public_id" append>Details</nuxt-link>
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
