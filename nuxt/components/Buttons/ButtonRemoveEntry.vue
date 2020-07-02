<template>
    <b-button
        size="sm"
        variant="outline-danger"
        class="remove-file"
    >

        <b-icon icon="trash" scale="1"/>
        Delete {{ publicID }}
    </b-button>

</template>

<script>
    import { BIcon } from "bootstrap-vue";
    export default {
        name: "ButtonRemoveEntry",

        components: {
            BIcon
        },

        props: {
            object: {
                type: [Object, Array],
                required: true
            }

        },
        data() {
            return {
                publicID: this.object.public_id
            }
        },

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
