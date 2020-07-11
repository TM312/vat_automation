<template>
    <b-button variant="primary" @click="submitPayload">
        <b-icon icon="box-arrow-in-right" /> Submit
    </b-button>
</template>

<script>
    import { BIcon } from "bootstrap-vue";

    export default {
        name: 'ButtonSubmit',
        components: {
            BIcon
        },
        props: {
            urlEndpointSubmit: {
                type: String,
                required: true
            },

            payload: {
                type: Array,
                required: true
            }
        },
        data() {
            return {
                progress: 0,
                progressBarStyle: "success",
            };
        },
        methods: {
            async submitPayload() {
                await this.$axios
                    .post(this.urlEndpointUpload, this.payload)

                    .then(response => {
                        let response_object = response.data;

                        if (response_object.status == "success") {

                            this.$toast.success(response_object.message, {
                                duration: 5000
                            });


                        } else {
                            this.$toast.error(response_object.message, { duration: 5000 });
                        }
                    })

                    .catch(err => {
                        console.log(err);
                        this.$toast.error(
                            "An error occured. Please make sure you have tried to submit valid data.",
                            { duration: 5000 }
                        );
                        this.progressBarStyle = "danger";
                    });




                // this.files = [];
            }
        }
    };
</script>

<style>
</style>
