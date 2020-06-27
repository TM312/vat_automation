<template>
    <b-col cols="4" md="3">
        <b-card :title="tax_record.seller_firm" border-variant="success">
            <b-card-text>
                <b>Period: </b>{{ tax_record.start_date }} – {{ tax_record.end_date }} <br>
                <b>Tax Jurisdiction: </b>{{ tax_record.tax_jurisdiction }} <br>
                <b>Created On: </b>{{ tax_record.created_on }} <br>
                <b>Created By: </b>{{ tax_record.created_by }} <br>
            </b-card-text>
        </b-card>
    </b-col>
</template>

<script>
    export default {
        name: 'CardTaxRecord',
        // eslint-disable-next-line
        props: { tax_record: { type: [Array, Object] } }
    }
</script>
