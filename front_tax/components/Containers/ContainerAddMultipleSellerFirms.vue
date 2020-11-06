<template>
  <b-container fluid>
    <toast-seller-firm-data-upload />
    <template-card :title="title" :url-endpoint-template="urlEndpointTemplate" :template-items="templateItems" />
    <br />
    <card-data-upload :url-endpoint-upload="urlEndpointUpload" />
  </b-container>
</template>

<script>

export default {
  name: 'ContainerAddMultipleSellerFirms',

  data() {
    return {
      title: 'Multiple Clients',
      urlEndpointTemplate: '/utils/template/seller_firm_information',
      templateItems: [
        { field_name: 'seller_firm_name', example: 'ON LINE DESK SA', field_formatting: 'Text', required: 'true', complementary_information: 'This information is being used for identification purposes of your clients, for instance in the tax record files.' },
        { field_name: 'address', example: 'Calle Ferraz 28, 1 Izq, 28008 Madrid, Spain', field_formatting: 'Text', required: 'false', complementary_information: 'This information is being used for identification purposes of your clients, for instance in the tax record files.' },
        { field_name: 'establishment_country_code', example: 'ES', field_formatting: 'Text', required: 'true', complementary_information: "This information is used when processing client's transaction reports." },
      ],
      urlEndpointUpload: '/business/seller_firm/csv',
    }
  }
}
</script>

<style>
</style>
