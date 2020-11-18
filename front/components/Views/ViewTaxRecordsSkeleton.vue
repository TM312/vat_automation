<template>
  <b-row class="mb-3" cols="1" cols-md="2" cols-xl="4">
    <b-col v-for="i in 20" :key="i" class="mb-2">
      <card-tax-record-short-skeleton />
    </b-col>
  </b-row>
</template>

<script>
export default {
  name: 'ViewTaxRecordsSkeleton'

}
</script>

<style>

</style>
