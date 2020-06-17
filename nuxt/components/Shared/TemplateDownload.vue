<template>
    <b-container fluid>
        <b-row>
            <b-col cols="12" md="6">
                <p>You can also upload information for several seller companies at once.</p>
                <p>Just use the <b>Template</b> on the right.</p>
            </b-col>
            <b-col cols="12" md="6">
                <b-card :title="templateCardTitle">
                    <b-card-body>
                        <p>Hello</p>
                        <b-button
                            size="md"
                            variant="outline-success"
                            class="remove-file"
                            @click="downloadFile()"
                        >
                            <b-icon icon="box-arrow-in-down" />
                            Get Template
                        </b-button>
                    </b-card-body>
                </b-card>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
export default {
    name: 'TemplateDownload',
    props: {
        templateName: {
            type: String,
            required: true
        },
        templateCardTitle: {
            type: String,
            required: true
        },
        // templateCardInformation: {
        //     type: String,
        //     required: true
        // }
    },
    methods: {
        async downloadFile() {

        this.$axios({
            method: 'GET',
            url: `/utils/template/${ this.templateName }`,
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
            console.log(err)
            })
        }
    }
}

</script>

<style></style>
