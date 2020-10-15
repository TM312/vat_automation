<template>
  <b-card border-variant="info" header="Template" no-body>
    <!-- <b-card-title class="text-left">Template</b-card-title> -->
    <b-card-body>
      <p>
        For multi-data uploads we provide the template below to allow for a smooth experience.<br />
        If you have not used the template yet, have a look at the details before downloading.<br />
        <b>Notice:</b> Please make sure to save your file as 'csv'.
      </p>
      <button-download :url-endpoint-template="urlEndpointTemplate" />
      <b-button v-b-toggle="titleJoined" variant="outline-secondary">
        <b-icon icon="info" /> Details
      </b-button>
      <br />
      <b-collapse :id="titleJoined">
        <template-information :items="templateItems" />
      </b-collapse>
    </b-card-body>
  </b-card>
</template>



<script>
import { BIcon } from "bootstrap-vue"

export default {
    name:'TemplateCard',
    components: {
        BIcon
    },
    props: {
        title: {
            type: String,
            required: true
        },
        urlEndpointTemplate: {
            type: String,
            required: true
        },
        templateItems: {
                type: [Array, Object],
                required: true
            }
    },
    data() {
        return {
            titleJoined: 'collapse-'+ this.title.replace(/\s+/g, '')
        }
    }
}
</script>

<style></style>
