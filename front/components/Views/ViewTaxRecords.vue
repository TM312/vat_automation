<template>
  <div>
    <div v-if="taxRecords.length === 0">
      <b-card>
        <b-card-text>
          <h5 class="text-muted text-center m-5">
            No Tax Records Created Yet
          </h5>
        </b-card-text>
      </b-card>
    </div>
    <div v-else>
      <b-row class="mb-3" cols="1" cols-md="2" :cols-xl="showcase ? 2 : 4">
        <b-col
          v-for="(taxRecord, i) in taxRecords"
          :key="i"
          class="mb-2"
        >
          <card-tax-record-short
            :tax-record="taxRecord"
            :client-public-id="sellerFirm.public_id"
            :showcase="showcase"
          />
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ViewTaxRecords',
  props: {
    sellerFirm: {
      type: Object,
      required: true
    },
    taxRecords: {
      type: Array,
      required: true
    },
    showcase: {
      type: Boolean,
      required: false,
      default: false
    }

  }
}
</script>

<style>
</style>
