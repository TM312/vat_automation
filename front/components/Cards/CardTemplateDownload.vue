<template>
  <b-card :header="header" class="text-center">
    <b-card-text>
      <p>{{ text }}</p>
      <button-download :url-endpoint-template="downloadUrl" small />
    </b-card-text>
  </b-card>
</template>

<script>
export default {
  name: "CardTemplateDownload",
  props: {
    header: {
      type: String,
      required: true
    },
    text: {
      type: String,
      required: true
    },
    downloadUrl: {
      type: String,
      required: true
    }
  }

}
</script>

<style>

</style>
