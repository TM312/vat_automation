<template>
    <div>
        <h1>urlEndpointUpload: {{ urlEndpointUpload }}</h1>
        <template-card :title="title" :urlEndpointTemplate="urlEndpointTemplate" :templateItems="templateItems" />
        <br />
        <card-data-upload :urlEndpointUpload="urlEndpointUpload" />
    </div>
</template>

<script>
export default {
    name: 'AddAccountInformationFiles',
    props: {
        sellerFirmPublicId: {
            type: String,
            required: true
        }

    },

    data() {
        return {
            title: 'Templates',
            urlEndpointTemplate: '/utils/template/account_information',
            // urlEndpointUpload: ''
        }
    },

    // beforeCreate() {
    //     urlEndpointUpload = `/business/seller_firm/${this.sellerFirmPublicId}/upload`
    // },
}
</script>

<style>

</style>
