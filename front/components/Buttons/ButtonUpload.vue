<template>
    <b-button :disabled="buttonDisabled" variant="primary" @click="uploadFiles">
        <b-icon v-if="!uploadInProgress" icon="box-arrow-in-right" />
        <b-spinner v-else small label="Spinning"></b-spinner>
        Upload
    </b-button>
</template>

<script>

    export default {
        name: 'ButtonUpload',

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
                uploadInProgress: false
            };
        },
        computed: {
            buttonDisabled() {
                if (this.files.length == 0 || this.uploadInProgress) {
                    return true
                } else {
                    return false
                }

            },
        },

        mounted() {
            this.socket = this.$nuxtSocket({
                name: 'home',
                reconnection: false
            })
        },

        methods: {

            async uploadFiles() {
                this.uploadInProgress = true
                var config = {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    },
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
                            // !!! delete later below
                            let taskId = response.data;
                            console.log('taskId:', taskId)

                            this.$emit('removeFile', i)
                        })

                    } catch(err) {
                        console.log(err);

                        i = this.files.length
                    }

                    await this.sleep(1000)
                }
                this.uploadInProgress = false


            }
        }
    }
</script>
