<template>
    <b-card
        :title="counter"
        :sub-title="subTitle"
        border-variant="info"

    >
    </b-card>
</template>

<script>
    export default {
        name: "CardTotalCount",
        props: {
            counterNumber: {
                type: Number,
                required: true,
                default: 0
            },

            subTitle: {
                type: String,
                required: false,
                default: ''
            }
        },
        data() {
            return {
                counter: this.counterNumber.toString()
            }
        },


    };
</script>

<style>
</style>
