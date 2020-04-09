
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

        <template v-slot:cell(platform)>
          <p>Amazon</p>
          <!-- <b-form-select v-model="selected" :options="options"></b-form-select> -->
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
      // selected: null,
      // options: [
      //   // { value: null, text: 'Please select an option' },
      //   // { value: 'Amazon', text: 'Amazon' }
      // ],
      progress: 0,
      progressBarStyle: 'success',
      files: [],
      fields: [
        '#',
        'name',
        'platform',
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
        '/media/tax_record/upload',
        data,
        config
        )

      .then( response => {
        let response_objects = response.data
        response_objects.map((data) => {
          if (data.status == 'success') {
            console.log(data)
            this.$toast.success(data.message, {duration: 5000,})
          } else {
            this.$toast.error(data.message, {duration: 5000,})
          }
        })
      })

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
