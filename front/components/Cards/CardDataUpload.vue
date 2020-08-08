
<template>
    <b-card>
        <b-card-title>Upload</b-card-title>
        <b-card-sub-title class="my-2">
            {{ files.length }}
            <span v-show="files.length==1">files </span>
            <span v-show="files.length>1">file </span>
            selected
        </b-card-sub-title>

        <b-card-text>
            <!-- <b-progress v-show="progress>0" striped :value="progress" :variant="progressBarStyle" /> -->

            <div class="my-3">
                <input
                    id="files"
                    ref="files"
                    style="display: none"
                    type="file"
                    multiple
                    @change="onFilesSelected"
                />

                <b-button id="selectButton" variant="outline-primary" @click="$refs.files.click()">
                    <b-icon icon="file-plus" /> Files
                </b-button>

                <b-button v-show="files.length>0" variant="outline-secondary" @click="files = []">
                    <b-icon icon="arrow-counterclockwise" /> Reset
                </b-button>

                 <!-- for adding clients as file uploads -->
                <button-upload v-if="urlEndpointUpload" v-show="files.length>0" :urlEndpointUpload="urlEndpointUpload" :files="files" @removeFile="removeFile" />

                <!-- for data uploads relating to a specific seller -->
                <button-upload-seller-firm v-else v-show="files.length>0" :files="files" @removeFile="removeFile" />

            </div>

            <div v-show="files.length>0" class="mt-3">
                <b-table striped hover :items="files" :fields="fields">
                    <template v-slot:cell(#)="data">{{ data.index + 1 }}</template>

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
    // Validation1: not uploading the same file multiple times.
    // Validation2: not uploading no file at all
    import { BIcon } from "bootstrap-vue";

    export default {
        name: "CardDataUpload",
        components: {
            BIcon
        },
        props: {
            // eslint-disable-next-line
            urlEndpointUpload: {
                type: String,
                required: false
            }
        },
        data() {
            return {
                // selected: null,
                // options: [
                //   // { value: null, text: 'Please select an option' },
                //   // { value: 'Amazon', text: 'Amazon' }
                // ],
                progress: 0,
                progressBarStyle: "success",
                files: [],
                fields: [
                    "#",
                    "name",
                    {
                        key: "lastModified",
                        label: "Last Modified",
                        formatter: (value, key, item) => {
                            return new Date(item.lastModified).toLocaleString();
                        }
                    },
                     {
                        key: "button",
                        label: ""
                    },
                ]
            };
        },

        methods: {
            onFilesSelected() {
                let selectedFiles = this.$refs.files.files;

                for (var i = 0; i < selectedFiles.length; i++) {
                    this.files.push(selectedFiles[i]);
                }
            },

            removeFile(key) {
                this.files.splice(key, 1);
            }
        }
    };
</script>
