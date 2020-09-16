<template>
    <b-button :disabled="buttonDisabled" variant="primary" @click="uploadFiles">
        <b-icon v-if="!buttonDisabled" icon="box-arrow-in-right" />
        <b-spinner v-else small label="Spinning"></b-spinner>
         Upload
    </b-button>
</template>

<script>
    import { BIcon } from "bootstrap-vue";

    export default {
        name: 'ButtonUpload',
        components: {
            BIcon
        },
        props: {
            urlEndpointUpload: {
                type: String,
                required: true
            },

            files: {
                type: Array,
                required: true
            }
        },
        data() {
            return {
                progress: 0,
                progressBarStyle: "success",
                buttonDisabled: false
            };
        },
        methods: {
            async uploadFiles() {
                this.buttonDisabled = true

                // FormData is a standard JS object
                const data = new FormData();
                for (var i = 0; i < this.files.length; i++) {
                    let file = this.files[i];
                    data.append("files", file);
                }
                // https://github.com/axios/axios/blob/master/examples/upload/index.html
                var config = {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    },
                    // onUploadProgress: function(progressEvent) {
                    //     this.progress = parseInt(
                    //         Math.round(
                    //             (progressEvent.loaded / progressEvent.total) * 100
                    //         )
                    //     );
                    // }.bind(this)
                };

                await this.$axios
                    .post(this.urlEndpointUpload, data, config)

                    .then(response => {
                        let response_object = response.data;

                        if (response_object.status == "success") {

                            this.$toast.success(response_object.message, {
                                duration: 5000
                            });

                            this.$emit('resetFileList')

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

                    this.buttonDisabled = false

            }
        }
    };
</script>

<style>
</style>
