
<template>
    <b-card header="Upload" no-body>
        <b-card-body>
            <b-progress v-show="progress>0" striped :value="progress" :variant="progressBarStyle" />

            <div class="my-3">
                <input
                    id="files"
                    ref="files"
                    style="display: none"
                    type="file"
                    multiple
                    @change="onFilesSelected"
                />

                <!-- <button-upload :urlEndpointUpload="urlEndpointUpload" :files="files" @resetFileList="files=[]" /> -->
                <button-upload-seller-firm :files="files" @resetFileList="files=[]" />


                <b-button id="selectButton" variant="outline-primary" @click="$refs.files.click()">
                    <b-icon icon="file-plus" /> Files
                </b-button>

                <b-button variant="outline-secondary" @click="files = []">
                    <b-icon icon="arrow-counterclockwise" /> Reset
                </b-button>
            </div>

            <div v-show="files.length>0" class="mt-3">
                <b-table striped hover :items="files" :fields="fields">
                    <template v-slot:cell(#)="data">{{ data.index + 1 }}</template>

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
        </b-card-body>
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
            urlEndpointUpload: {
                type: String,
                required: true
            },

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
                    "platform",
                    {
                        key: "lastModified",
                        label: "Last Modified",
                        formatter: (value, key, item) => {
                            return new Date(item.lastModified).toLocaleString();
                        }
                    },
                    ""
                ]
            };
        },
        methods: {
            onFilesSelected() {
                let selectedFiles = this.$refs.files.files;
                console.log(selectedFiles);

                for (var i = 0; i < selectedFiles.length; i++) {
                    this.files.push(selectedFiles[i]);
                }
            },

            removeFile(key) {
                this.files.splice(key, 1);
                console.log(this.files);
            }
        }
    };
</script>
