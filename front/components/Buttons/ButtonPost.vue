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
            };
        },
        methods: {
            async submitPayload() {
                await this.$axios
                    .post(this.urlEndpointUpload, this.payload)

                    .then(response => {
                        let response_object = response.data;

                        if (response_object.status == "success") {

                            this.$bvToast.toast(response_object.message, {
                                autoHideDelay: 5000,
                                variant: 'success'
                            })

                        } else {
                            this.$bvToast.toast(response_object.message, {
                                autoHideDelay: 5000,
                                variant: 'danger'
                            })
                        }
                    })

                    .catch(err => {
                        console.log(err);
                        this.$bvToast.toast('An error occured. Please make sure you have tried to submit valid data.', {
                            autoHideDelay: 5000,
                            variant: 'danger'
                        })
                    });




                // this.files = [];
            }
        }
    };
</script>

<style>
</style>
