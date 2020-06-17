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
        v-for="(tax_record, index) in self_tax_records"
        :key="index" columns
      >
        <b-card>
          <b-card-title>{{ tax_record.accountentifier }}</b-card-title>
          <b-card-text>
            <b>Platform: </b>{{ tax_record.platform }}
          </b-card-text>
          <b-card-text class="small text-muted">
            <b>Created on: </b>{{ tax_record.created_on }}
          </b-card-text>
          <b-button
            size="sm"
            variant="outline-success"
            class="remove-file"
            @click="downloadFile(tax_record.activity_period, tax_record.formatted_input_name)"
          >
            <b-icon icon="box-arrow-in-down" />
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

// import file-system from 'file-system'

export default {
  name: 'DownloadField',
  components: {
    BIcon
  },
  data() {
    return {
      progress: 0,
      progressBarStyle: 'success'
    }
  },
  computed: {
    ...mapState(["self_tax_records"])
  },
  methods: {
    async downloadFile(activity_period, filename) {

    this.$axios(
      {
        method: 'GET',
        url: `/media/tax_record/download/${ activity_period }/${ filename }`,
        // params: params,
        responseType: 'blob'
      }
    ).then(res => {
        const blob = new Blob([res.data], { type: res.data.type })
        let url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        const contentDisposition = res.headers['content-disposition']
        let fileName = 'unknown'
        if (contentDisposition) {
            const fileNameMatch = contentDisposition.match(/filename="(.+)"/)
            if (fileNameMatch.length === 2)
                fileName = fileNameMatch[1]
        }
        link.setAttribute('download', fileName)

        document.body.appendChild(link)
        link.click()
        link.remove()

        window.URL.revokeObjectURL(url)
    }).catch(err => {
        console.log(err)
    })







    //   await this.$axios({
    //     method: 'get',
    //     url: `/media/tax_record/download/${ activity_period }/${ filename }`,
    //     responseType: 'stream'
    //   })
    //   .then(function (response) {
    //     response.data.pipe(fs.createWriteStream(filename))
    //   })
    //   .catch (err => {
    //     console.log(err)
    //     this.$toast.error('An error occured. The requested file is currently unavailable. Please try again later', {duration: 5000,})
    //     this.progressBarStyle = 'danger'
    //     // this.$toast.error(err.message, {duration: 5000,}))
    //   })
    }
  }
}
</script>
