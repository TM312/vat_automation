<template>
<div>
    <template-card :title="title" :urlEndpointTemplate="urlEndpointTemplate" :templateItems="templateItems" />
    <br>
    <card-data-upload :urlEndpointUpload="urlEndpointUpload" />
</div>
</template>

<script>
export default {
    name: 'AddVatNumbersFiles',
    data() {
        return {
            title: 'Vat Number Template',
            urlEndpointTemplate: '/utils/template/seller_firm_vat_numbers',
            templateItems: [
                { field_name: 'seller_firm_public_id', example: '1c24d175-c3a3-4611-be24-2b7537f5b62e', field_formatting: 'Text', required: 'true', complementary_information: 'tbd' },
                { field_name: 'valid_from', example: '01.06.2016', field_formatting: 'Date', required: 'true', complementary_information: 'tbd' },
                { field_name: 'valid_to', example: '31.12.2099', field_formatting: 'Date', required: 'false', complementary_information: 'tbd' },
                { field_name: 'country_code', example: 'ES', field_formatting: 'Text', required: 'true', complementary_information: 'tbd' },
                { field_name: 'vatin', example: 'ESA81405219', field_formatting: 'Text', required: 'true', complementary_information: 'tbd' }
            ],
            urlEndpointUpload: '/tax/vatin/csv'
        }
    }
}
</script>

<style>

</style>
