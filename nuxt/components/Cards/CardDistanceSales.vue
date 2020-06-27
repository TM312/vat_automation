<template>
    <b-card header="Distance Sales">
        <b-card-text>
            <b-table borderless :items="distance_sales"></b-table>
        </b-card-text>
    </b-card>
</template>

<script>
    // import { BIcon } from "bootstrap-vue";

    export default {
        name: 'CardDistanceSales',
        // eslint-disable-next-line
        props: { distance_sales: { type: [Array, Object] } },

        // components: {
        //     BIcon
        // }
    }
</script>
