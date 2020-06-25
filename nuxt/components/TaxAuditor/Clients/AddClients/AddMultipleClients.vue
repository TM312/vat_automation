<template>
    <template-card :title="title" :urlEndpointTemplate="urlEndpointTemplate" :templateItems="templateItems" />
</template>

<script>

export default {
    name: 'AddMultipleClients',
    data() {
        return {
            title: 'Multiple Clients',
            urlEndpointTemplate: '/utils/template/seller_firm_information',
            templateItems: [
                { field_name: 'seller_firm_name', example: 'ON LINE DESK SA', field_formatting: 'Text', required: 'true', complementary_information: 'This information is being used for identification purposes of your clients, for instance in the tax record files.' },
                { field_name: 'address', example: 'Calle Ferraz 28, 1 Izq, 28008 Madrid, Spain', field_formatting: 'Text', required: 'false', complementary_information: 'This information is being used for identification purposes of your clients, for instance in the tax record files.' },
                { field_name: 'establishment_country_code', example: 'ES', field_formatting: 'Text', required: 'true', complementary_information: "This information is used when processing client's transaction reports." },
                { field_name: 'accounting_firm_client_id', example: '1c24d175-c3a3-4611-be24-2b7537f5b62e', field_formatting: 'Text', required: 'false', complementary_information: "Is being used for instance for a convenient naming of your clients' tax records." }
            ]
        }
     }
}
</script>

<style>
</style>
