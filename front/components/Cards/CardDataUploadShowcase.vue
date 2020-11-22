
<template>
  <b-card class="card-sample">
    <b-card-title>Upload</b-card-title>
    <b-card-sub-title class="my-2">
      {{ files.length }}
      <span v-show="files.length != 1">files </span>
      <span v-show="files.length == 1">file </span>
    </b-card-sub-title>

    <b-card-text>
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
          :disabled="files.length === 4"
          @click="fillFiles"
        >
          <b-icon icon="file-plus" /> Files
        </b-button>

        <b-button
          variant="outline-secondary"
          @click="files = []"
        >
          <b-icon icon="arrow-counterclockwise" /> Reset
        </b-button>

        <b-button
          id="upload-showcase"
          variant="outline-primary"
          :disabled="buttonDisabled"
          @click="uploadFilesShowcase"
        >
          <b-icon
            v-if="!uploadInProgress"
            icon="box-arrow-in-right"
          />
          <b-spinner v-else small label="Spinning" />
          Upload
        </b-button>
      </div>

      <div v-show="files.length > 0" class="mt-3">
        <b-table striped hover :items="files" :fields="fields">
          <template v-slot:cell(#)="data">
            {{ data.index + 1 }}
          </template>
          <template v-slot:cell(button)="data">
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
    </b-card-text>
  </b-card>
</template>

<script>

export default {
  name: "CardDataUploadShowcase",

  data() {
    return {
      uploadInProgress: false,
      files: [],
      fields: [
        "#",
        "name",
        {
          key: "lastModified",
          label: "Last Modified",
          formatter: (value, key, item) => {
            return new Date(item.lastModified).toLocaleString()
          },
        },
        {
          key: "button",
          label: "",
        },
      ],
    }
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

  methods: {
    async uploadFilesShowcase() {
      this.uploadInProgress = true
      for (var i = 0; i != this.files.length; ) {
        await this.sleep(2500)
        this.removeFile(i)
      }
      this.uploadInProgress = false
    },

    fillFiles() {
      this.files = [
        {
          name: "accounts.csv",
          lastModified: new Date(),
        },
        {
          name: "items.csv",
          lastModified: new Date(),
        },
        {
          name: "vat_numbers.csv",
          lastModified: new Date(),
        },
        {
          name: "distance_sales.csv",
          lastModified: new Date(),
        },
      ]
    },

    onFilesSelected() {
      let selectedFiles = this.files

      for (var i = 0; i < selectedFiles.length; i++) {
        this.files.push(selectedFiles[i])
      }
    },

    removeFile(key) {
      this.files.splice(key, 1)
    },
  },
}
</script>
