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
            )

        } catch(err) {
          this.uploadInProgress = false
          i = this.files.length
        }

        await this.sleep(2500)

      }
      this.uploadInProgress = false

    }
  }
}
</script>

<style>
</style>
