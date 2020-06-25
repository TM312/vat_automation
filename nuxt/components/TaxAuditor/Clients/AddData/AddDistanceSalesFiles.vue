<template>
    <template-card :title="title" :urlEndpointTemplate="urlEndpointTemplate" :templateItems="templateItems" />
</template>

<script>
export default {
    name: 'AddDistanceSalesFiles',
    data() {
        return {
            title: 'Distance Sales Template',
            urlEndpointTemplate: '/utils/template/distance_sales',
            templateItems: [
                { field_name: 'seller_firm_public_id', example: '1c24d175-c3a3-4611-be24-2b7537f5b62e', field_formatting: 'Text', required: 'true', complementary_information: 'This information is being used for identification purposes of your clients, for instance in the tax record files.' },
                { field_name: 'valid_from', example: '01.06.2018', field_formatting: 'Date', required: 'true', complementary_information: 'This information is being used for identification purposes of your clients, for instance in the tax record files.' },
                { field_name: 'valid_to', example: '31.12.2025', field_formatting: 'Date', required: 'false', complementary_information: "This information is used when processing client's transaction reports." },
                { field_name: 'arrival_country_code', example: 'FR', field_formatting: 'Text', required: 'true', complementary_information: "Is being used for instance for a convenient naming of your clients' tax records." },
                { field_name: 'status', example: 'TRUE', field_formatting: 'Text', required: 'false', complementary_information: "Is being used for instance for a convenient naming of your clients' tax records." }
            ]
        }
    }
}
</script>

<style>

</style>
