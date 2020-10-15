<template>
  <div>
    <b-row cols="1" cols-xl="2" class="my-2">
      <b-col class="my-2 px-2">
        <lazy-card-client class="mb-5 h-100" />
      </b-col>
      <b-col class="my-2 px-2">
        <lazy-card-accounts class="mb-5 h-100" />
      </b-col>
    </b-row>
    <b-row>
      <b-col class="my-2 px-2">
        <lazy-card-vat-numbers class="mb-5 h-100" />
      </b-col>
      <b-col class="my-2 px-2">
        <lazy-card-distance-sales class="mb-5 h-100" />
      </b-col>
    </b-row>
  </div>
</template>

<script>
    export default {
        name: "OverviewBaseData"
    }
</script>

<style>
</style>
