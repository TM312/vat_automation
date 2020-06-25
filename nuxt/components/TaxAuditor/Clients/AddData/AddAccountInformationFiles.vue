<template>
    <template-card :title="title" :urlEndpointTemplate="urlEndpointTemplate" :templateItems="templateItems" />
</template>

<script>
export default {
    name: 'AddAccountInformationFiles',
    data() {
        return {
            title: 'Account Information Template',
            urlEndpointTemplate: '/utils/template/account_information',
            templateItems: [
                { field_name: 'seller_firm_public_id', example: '1c24d175-c3a3-4611-be24-2b7537f5b62e', field_formatting: 'Text', required: 'true', complementary_information: 'tbd' },
                { field_name: 'channel_code', example: 'MFN', field_formatting: 'Text', required: 'true', complementary_information: 'tbd' },
                { field_name: 'account_id', example: 'A2UTOJEVH3PSRA', field_formatting: 'Text', required: 'true', complementary_information: 'tbd' },
            ]
        }
    }
}
</script>

<style>

</style>
