<template>
  <div>
    <b-row>
      <b-col cols="12" md="6">
        <UploadField />
      </b-col>
      <b-col cols="12" md="6">
        <DownloadField />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import UploadField from '@/components/UploadField'
import DownloadField from '@/components/DownloadField'
export default {
  // middleware: 'auth',
  components: {
    UploadField,
    DownloadField
  },
}
</script>

<style></style>
