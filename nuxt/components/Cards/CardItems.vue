<template>
    <b-card>
        <b-card-text>
            <b-table hover sortable :items="items"></b-table>
        </b-card-text>
    </b-card>
</template>

<script>
    // import { BIcon } from "bootstrap-vue";

    export default {
        name: 'CardItems',
        // eslint-disable-next-line
        props: { items: { type: [Array, Object] } },

        // components: {
        //     BIcon
        // }
    }
</script>
