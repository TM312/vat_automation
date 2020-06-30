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
        name: "CardTotalCountFunction",
        props: {
            counterFunction: {
                type: Function,
                required: true,
            },

            subTitle: {
                type: String,
                required: false,
                default: ''
            }
        },
        // data() {
        //     return {
        //         counter: this.counterNumber.toString()
        //     }
        // },
        computed: {
            counter() {
                return this.counterFunction().toString()
            }

        }


    };
</script>

<style>
</style>
