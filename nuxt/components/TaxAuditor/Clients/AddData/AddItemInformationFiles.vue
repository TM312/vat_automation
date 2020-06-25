<template>
    <template-card :title="title" :urlEndpointTemplate="urlEndpointTemplate" :templateItems="templateItems" />

</template>

<script>

export default {
    name: 'AddItemInformationFiles',

    data() {
        return {
            title: 'Item Information Template',
            urlEndpointTemplate: '/utils/template/item_information',
            templateItems: [
                { field_name: 'seller_firm_public_id', example: '1c24d175-c3a3-4611-be24-2b7537f5b62e', field_formatting: 'Text', required: 'true', complementary_information: 'tbd' },
                { field_name: 'valid_from', example: '01.06.2016', field_formatting: 'Date', required: 'true', complementary_information: 'tbd' },
                { field_name: 'valid_to', example: '01.06.2025', field_formatting: 'Date', required: 'false', complementary_information: 'tbd' },
                { field_name: 'SKU', example: 'WE-01-02-01-01-01-01-41', field_formatting: 'Text', required: 'true', complementary_information: 'tbd' },
                { field_name: 'brand_name', example: 'weltenmann', field_formatting: 'Text', required: 'false', complementary_information: 'tbd' },
                { field_name: 'name', example: 'WELTENMANN Classic Men Cotton Slip-on Espadrilles, Marine, 41', field_formatting: 'Text', required: 'false', complementary_information: 'tbd' },
                { field_name: 'ean', example: '8440000000000', field_formatting: 'Text', required: 'false', complementary_information: 'tbd' },
                { field_name: 'asin', example: 'B07DFKN4TM', field_formatting: 'Text', required: 'false', complementary_information: 'tbd' },
                { field_name: 'fnksu', example: 'X000UUSGXL', field_formatting: 'Text', required: 'false', complementary_information: 'tbd' },
                { field_name: 'weight_kg', example: '0.57', field_formatting: 'Number', required: 'false', complementary_information: 'tbd' },
                { field_name: 'tax_code_code', example: 'A_GEN_STANDARD', field_formatting: 'Text', required: 'true', complementary_information: 'tbd' },
                { field_name: 'unit_cost_price_currency_code', example: 'EUR', field_formatting: 'Text', required: 'true', complementary_information: 'tbd' },
                { field_name: 'unit_cost_price_net', example: '12.4', field_formatting: 'Number', required: 'true', complementary_information: 'tbd' },
            ]
        }
    }
}
</script>

<style>

</style>
