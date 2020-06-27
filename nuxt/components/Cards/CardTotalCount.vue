<template>
    <b-card
        :title="counter"
        :sub-title="subTitle"
        border-variant="primary"

    >
    </b-card>
</template>

<script>
    export default {
        name: "CardTotalCount",

        props: {
            counterNumber: {
                type: Number,
                required: true
            },
            subTitle: {
                type: String,
                required: false
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
