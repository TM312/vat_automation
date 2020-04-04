<template>
  <b-container class="my-5 py-5">
    <b-progress
      v-show="progress>0"
      striped
      :value="progress"
      :variant="progressBarStyle"
    />
    <div class="mt-5">
      <p class="lead">
        The following tax reports are available for download.
      </p>

      <b-card-group
        columns
      >
        <b-card>
          <b-card-title>Title</b-card-title>
          <b-card-text>
            <b></b>
          </b-card-text>
          <b-card-text class="small text-muted">
            Last updated 3 mins ago
          </b-card-text>
          <b-button
            size="sm"
            variant="outline-success"
            class="remove-file"
            @click="downloadFile()"
          >
            <b-icon icon="cloud-download" />
            Download
          </b-button>
        </b-card>
      </b-card-group>
    </div>
  </b-container>
</template>


<script>
import { BIcon } from 'bootstrap-vue'
import { mapState } from 'vuex'

export default {
  name: 'UploadField',
  components: {
    BIcon,
    ...mapState
  },
  data() {
    return {
      progress: 0,
      progressBarStyle: 'success'
    }
  },
  methods: {
    async downloadFiles() {
      // this.$axios.setHeader('Content-Type', 'multipart/form-data', ['post'])
      await this.$axios.get(
        '/media/tax_data/download',
        "data"
        )

      .then( response => this.$toast.success(response.data.message, {duration: 5000,}))

      .catch (err => {
        console.log(err)
        this.$toast.error('An error occured. The requested file is currently unavailable. Please try again later', {duration: 5000,})
        this.progressBarStyle = 'danger'
        })
      // console.log(err))
      // this.$toast.error(err.message, {duration: 5000,}))
    }
  }
}
</script>
