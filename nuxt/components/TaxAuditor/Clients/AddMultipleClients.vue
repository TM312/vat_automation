<template>
    <b-container fluid>
        <b-card>
            <b-card-title class="text-center">
            Multiple Clients
            </b-card-title>
            <b-card-body>
                <TemplateDownload
                    templateName="seller_firm_information.csv"
                    templateCardTitle="Seller Firm Template"
                />
                <FileUpload />
            </b-card-body>
        </b-card>
    </b-container>
</template>

<script>
import TemplateDownload from '@/components/Shared/TemplateDownload'
import FileUpload from '@/components/Shared/FileUpload'

export default {
    components: {
        TemplateDownload,
        FileUpload
    }

}
</script>

<style>

</style>
