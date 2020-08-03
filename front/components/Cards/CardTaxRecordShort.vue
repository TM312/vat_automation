<template>
    <b-col cols="4" md="3">
        <p>"Test"</p>
        <b-card :title="tax_record.seller_firm" border-variant="success">
            <b-card-text>
                <b>Period: </b>{{ tax_record.start_date }} – {{ tax_record.end_date }} <br>
                <b>Tax Jurisdiction: </b>{{ tax_record.tax_jurisdiction_code }} <br>
                <nuxt-link :to="`/tax/tax_records/${tax_record.public_id}`">Details</nuxt-link>
            </b-card-text>
        </b-card>
    </b-col>
</template>

<script>
    export default {
        name: 'CardTaxRecordShort',
        // eslint-disable-next-line
        props: { tax_record: { type: [Array, Object] } }
    }
</script>
