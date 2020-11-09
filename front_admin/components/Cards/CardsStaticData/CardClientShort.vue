<template>
  <b-card :border-variant="getCardColor">
    <b-card-title>{{ business.name }}</b-card-title>
    <b-card-sub-title class="mt-1">
      <b-form-row>
        <b-col cols="auto">
          <b>Address:</b>
        </b-col>
        <b-col cols="auto" class="mr-auto">
          {{ business.address }}
        </b-col>
      </b-form-row>
    </b-card-sub-title>

    <b-card-text class="pt-3">
      <nuxt-link :to="`/seller-firms/${business.public_id}`">
        Details
      </nuxt-link>
    </b-card-text>
  </b-card>
</template>

<script>
export default {
  name: 'CardClientShort',
  // eslint-disable-next-line
        props: { business: { type: [Array, Object] } },

  computed: {
    getCardColor() {
      return '' //this.business.transaction_ready ? //'' : 'danger'
    }
  },
}
</script>
