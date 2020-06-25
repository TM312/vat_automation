<template>
    <b-button variant="primary" @click="uploadFiles">
        <b-icon icon="box-arrow-in-right" /> Upload
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
            };
        },
        methods: {
            async uploadFiles() {
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
                    onUploadProgress: function(progressEvent) {
                        this.progress = parseInt(
                            Math.round(
                                (progressEvent.loaded / progressEvent.total) * 100
                            )
                        );
                    }.bind(this)
                };

                // this.$axios.setHeader('Content-Type', 'multipart/form-data', ['post'])
                await this.$axios
                    .post(this.urlEndpointUpload, data, config)

                    .then(response => {
                        let response_objects = response.data;
                        response_objects.map(data => {
                            if (data.status == "success") {
                                console.log(data);
                                this.$toast.success(data.message, {
                                    duration: 5000
                                });
                            } else {
                                this.$toast.error(data.message, { duration: 5000 });
                            }
                        });
                    })

                    .catch(err => {
                        console.log(err);
                        this.$toast.error(
                            "An error occured. Please make sure you have tried to submit valid data.",
                            { duration: 5000 }
                        );
                        this.progressBarStyle = "danger";
                    });
                // console.log(err))
                // this.$toast.error(err.message, {duration: 5000,}))

                // this.files = [];
            }
        }
    };
</script>

<style>
</style>
