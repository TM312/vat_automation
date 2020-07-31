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
            enableButton() {
                if (this.files.length == 0) {
                        this.buttonDisabled = false
                    }
            },

            sleep(ms) {
                return new Promise(resolve => setTimeout(resolve, ms));
            },


            async uploadFiles() {
                this.buttonDisabled = true
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

                // FormData is a standard JS object
                for (var i = 0; i != this.files.length;) {
                    let file = this.files[i];
                    const data = new FormData();
                    data.append('file', file);

                    // https://github.com/axios/axios/blob/master/examples/upload/index.html
                    try {
                        await this.$axios
                        .post(this.urlEndpointUpload, data, config)

                        .then(response => {
                            let response_objects = response.data;

                            for (var j = 0; j < response_objects.length; j++) {
                                let response_object = response_objects[j]

                                if (response_object.status == "success") {

                                    this.$toast.success(response_object.message, {
                                        duration: 10000
                                    });


                                } else {
                                    this.$toast.error(response_object.message, { duration: 10000 });
                                }
                            }
                            this.$emit('removeFile', i)
                        })

                    } catch(err) {
                        console.log(err);
                        this.$toast.error(
                            "An error occured. Please make sure you have tried to submit valid data.",
                            { duration: 10000 }
                        );
                        this.progressBarStyle = "danger";
                        this.buttonDisabled = false
                        i = this.files.length
                    }

                    await this.sleep(1000)
                    this.enableButton()
                }

            }
        }
    };
</script>

<style>
</style>
