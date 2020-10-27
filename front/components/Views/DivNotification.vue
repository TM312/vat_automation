<template>
  <div :border-variant="cardBorderVariant">
    <div>
      <p v-if="notification.subject === 'Data Upload'">
        <b>{{ notification.created_by }}</b> added new data for
        <nuxt-link
          :to="`/tax/clients/${notification.seller_firm_public_id}`"
          class="mt-2"
        >
          {{ notification.seller_firm }}
        </nuxt-link>
      </p>

      <p v-else-if="notification.subject === 'New Seller Firm'">
        <b>{{ notification.created_by }}</b> added
        <nuxt-link
          :to="`/tax/clients/${notification.seller_firm_public_id}`"
          class="mt-2"
        >
          {{ notification.seller_firm }}
        </nuxt-link>
      </p>

      <p v-else-if="notification.subject === 'New Seller Firms'">
        <b>{{ notification.created_by }}</b> added
        <nuxt-link to="/tax/clients/" class="mt-2">
          {{ notification.message }}
        </nuxt-link>
      </p>


      <b-row v-if="notification.tags && notification.tags.length !== 0" class="mb-2">
        <b-col>
          <b-badge
            v-for="tag in notification.tags"
            :key="tag.code" :variant="tag.code === 'TRANSACTION' ? 'success' : 'primary'"
            class="mr-1"
          >
            {{ capitalize(tag.code) }}
          </b-badge>
        </b-col>
      </b-row>
    </div>

    <div class="small text-muted">
      <b-row>
        <b-col cols="auto" class="mr-auto">
          <span>{{ notification.subject }}</span>
        </b-col>
        <b-col cols="auto">
          <span v-if="notification.modified_at"> updated {{ $dateFns.formatDistanceToNow(new Date(notification.modified_at)) }} ago</span>
          <span v-else> {{ $dateFns.formatDistanceToNow(new Date(notification.created_on)) }} ago</span>
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
export default {
  name: "DivNotification",
  props: {
    notification: {
      type: [Array, Object],
      required: true,
    },
  },

  computed: {
    cardBorderVariant() {
      if (this.notification.subject === 'New Seller Firm' || this.notification.subject === 'New Seller Firms') {
        return 'primary'
      } else {
        return ''
      }
    }

  }
}
</script>

<style>
</style>
