<template>

    <b-button variant="primary" @click="downloadFile()">
        <b-icon icon="download" /> Download
    </b-button>

</template>

<script>
import { BIcon } from "bootstrap-vue";

export default {
    name: 'ButtonDownload',
    props: {
        urlEndpointTemplate: {
            type: String,
            required: true
        }
    },

    components: {
        BIcon
    },

    methods: {

        async downloadFile() {

            this.$axios({
                method: 'GET',
                url: this.urlEndpointTemplate,
                // params: params,
                responseType: 'blob'
                })

            .then(res => {
                const blob = new Blob([res.data], { type: res.data.type })
                let url = window.URL.createObjectURL(blob)
                const link = document.createElement('a')
                link.href = url
                const contentDisposition = res.headers['content-disposition']
                if (contentDisposition) {
                    const fileNameMatch = contentDisposition.match(/this.templateName="(.+)"/)
                    if (fileNameMatch.length === 2)
                        this.fileName = fileNameMatch[1]
                }
                link.setAttribute('download', this.fileName)

                document.body.appendChild(link)
                link.click()
                link.remove()

                window.URL.revokeObjectURL(url)
                })

            .catch(err => {
                console.log(err);
                this.$bvToast.toast('An error occured. Please try again later or contact one of the admins.', {
                    autoHideDelay: 5000,
                    variant: 'danger'
                })
            })
        }
    }
}

</script>

<style></style>
