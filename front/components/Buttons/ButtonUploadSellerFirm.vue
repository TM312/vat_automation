<template>
  <b-button :disabled="buttonDisabled" variant="primary" @click="uploadFiles">
    <b-icon v-if="!uploadInProgress" icon="box-arrow-in-right" />
    <b-spinner v-else small label="Spinning" />
    Upload
  </b-button>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        name: 'ButtonUploadSellerFirm',

        props: {
            files: {
                type: Array,
                required: true
            }
        },

        data() {
            return {
                uploadInProgress: false
            }
        },

        computed: {
            ...mapState({
                sellerFirmPublicId: state => state.seller_firm.seller_firm.public_id
            }),

            urlEndpointUpload() {
                return `/business/seller_firm/${this.sellerFirmPublicId}/upload`
            },

            buttonDisabled() {
                if (this.files.length == 0 || this.uploadInProgress) {
                    return true
                } else {
                    return false
                }
            }
        },


        methods: {
            enableButton() {
                if (this.files.length == 0) {
                    this.buttonDisabled = false
                }
            },

            async uploadFiles() {
                this.uploadInProgress = true
                var config = {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    },
                }

                // FormData is a standard JS object
                for (var i = 0; i != this.files.length;) {
                    let file = this.files[i]
                    const data = new FormData()
                    data.append('file', file)

                    // https://github.com/axios/axios/blob/master/examples/upload/index.html
                    try {
                        await this.$axios
                        .post(this.urlEndpointUpload, data, config)

                        .then(
                            this.$emit('removeFile', i)
                            // response => {
                            // let responseObjects = response.data;

                            // for (var j = 0; j < responseObjects.length; j++) {
                            //     let responseObject = responseObjects[j]

                            //     if (responseObject.status == "success") {

                            //         this.$toast.success(responseObject.message, {
                            //             duration: 10000
                            //         });


                            //     } else {
                            //         this.$toast.error(responseObject.message, { duration: 10000 });
                            //     }
                            // }

                        // }
                        )

                    } catch(err) {
                        // console.log(err);
                        // this.$toast.error(
                        //     "An error occured. Please make sure you have tried to submit valid data.",
                        //     { duration: 10000 }
                        // );
                        this.uploadInProgress = false
                        i = this.files.length
                    }

                    await this.sleep(1000)
                }
                this.uploadInProgress = false

            }
        }
    }
</script>

<style>
</style>
