<template>
    <b-card header="Accounts">
        <b-card-text>
            <b-table borderless :items="accounts"></b-table>
        </b-card-text>
    </b-card>
</template>

<script>
    // import { BIcon } from "bootstrap-vue";

    export default {
        name: 'CardAccounts',
        // eslint-disable-next-line
        props: { accounts: { type: [Array, Object] } },

        // components: {
        //     BIcon
        // }
    }
</script>
