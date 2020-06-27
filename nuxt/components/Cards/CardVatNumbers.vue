<template>
    <b-card header="Vat Numbers">
        <b-card-text>
            <b-table borderless :items="vat_numbers"></b-table>
        </b-card-text>
    </b-card>
</template>

<script>

    export default {
        name: 'CardVatNumbers',
        // eslint-disable-next-line
        props: { vat_numbers: { type: [Array, Object] } },

    }
</script>
