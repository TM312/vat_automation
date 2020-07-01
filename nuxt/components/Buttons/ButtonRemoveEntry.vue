<template>
    <!-- <b-button
        size="sm"
        variant="outline-danger"
        class="remove-file"
        @click="removeFile(data.index)"
    > -->
    <b-button>
        <b-icon icon="trash" variant="error" font-scale="1"/>
    </b-button>

</template>

<script>
    import { BIcon } from "bootstrap-vue";
    export default {
        name: "ButtonRemoveEntry",

        components: {
            BIcon
        },

        // props: {
        //     data: {
        //         type: String,
        //         required: true
        //     }

        // },

        // methods: {
        //     async refresh() {
        //         const { store } = this.$nuxt.context;
        //         await store.dispatch("accounting_firm/get_by_public_id", this.accounting_firm.public_id);
        //     }
        // }
    };
</script>



<style>
</style>
