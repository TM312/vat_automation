
<template>
  <b-container class="my-5 py-5">
    <b-progress
      v-show="progress>0"
      striped
      :value="progress"
      :variant="progressBarStyle"
    />

    <div class="my-3">
      <input
        id="files"
        ref="files"
        style="display: none"
        type="file"
        multiple
        @change="onFilesSelected"
      />
      <b-button
        id="selectButton"
        variant="outline-primary"
        @click="$refs.files.click()"
      >
        <b-icon icon="file-plus" />
        Files
      </b-button>

      <b-button
        variant="outline-secondary"
        @click="files = []"
      >
        <b-icon icon="arrow-counterclockwise" />
        Reset
      </b-button>

      <b-button
        variant="primary"
        @click="submitFiles"
      >
        <b-icon icon="box-arrow-in-right" />
        Submit
      </b-button>
    </div>
    <div class="mt-5">
      <p class="lead">
        Selected Files
      </p>
      <b-table
        striped
        hover
        :items="files"
        :fields="fields"
      >
        <template v-slot:cell(#)="data">
          {{ data.index + 1 }}
        </template>

        <template v-slot:cell(type)="data">
          {{ data.index + 1 }}
        </template>

        <template v-slot:cell(keep?)="data">
          <b-button
            size="sm"
            variant="outline-danger"
            class="remove-file"
            @click="removeFile(data.index)"
          >
            <b-icon icon="trash" />
          </b-button>
        </template>
      </b-table>
    </div>
  </b-container>
</template>

<script>
// Validation1: not uploading the same file multiple times.
// Validation2: not uploading no file at all
import { BIcon } from 'bootstrap-vue'

export default {
  name: 'UploadField',
  components: {
    BIcon
  },
  data() {
    return {
      progress: 0,
      progressBarStyle: 'success',
      files: [],
      fields: [
        '#',
        'name',
        // {
        //   // A virtual column with custom formatter
        //   key: 'size',
        //   label: 'Size',
        //   formatter: (value, _, _) => {
        //     return str(value/)
        //   }
        // },
        {
          key: 'lastModified',
          label: 'Last Modified',
          formatter: (value, key, item) => {
            return new Date(item.lastModified).toLocaleString()
          }
        },
        'keep?'
      ]
    }
  },
  methods: {
    async sendTestRequest() {
      try {
        await this.$axios.get('/media/tax_data')

        await function(res) {
          console.log(res)
        }
      } catch (err) {
          console.log('NOT SUCCESSFUL')
          console.log(err)
      }
    },

    onFilesSelected() {
      let selectedFiles = this.$refs.files.files
      console.log(selectedFiles)

      for(var i = 0; i < selectedFiles.length; i++){
        this.files.push(selectedFiles[i])
      }
    },

    removeFile(key) {
      this.files.splice(key, 1)
      console.log(this.files)
    },
    async submitFiles() {

      // FormData is a standard JS object
      const data = new FormData()
      for (var i = 0; i < this.files.length; i++) {
        let file = this.files[i]
        data.append('files', file)
      }
      // https://github.com/axios/axios/blob/master/examples/upload/index.html
      var config =
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: function(progressEvent) {
          this.progress = parseInt(Math.round ( ( progressEvent.loaded / progressEvent.total) * 100 ))
        }.bind(this)
      }

      // this.$axios.setHeader('Content-Type', 'multipart/form-data', ['post'])
      await this.$axios.post(
        '/media/tax_data/upload',
        data,
        config
        )

      .then( response => this.$toast.success(response.data.message, {duration: 5000,}))

      .catch (err => {
        console.log(err)
        this.$toast.error('An error occured. Please make sure you have tried to submit valid data.', {duration: 5000,})
        this.progressBarStyle = 'danger'
        })
      // console.log(err))
      // this.$toast.error(err.message, {duration: 5000,}))


      this.files = []
    }
  }
}
</script>
