<template>
  <b-card>
      <b-card-title>{{ notification.subject }}</b-card-title>
      <b-card-text>
        <p v-if="notification.subject === 'Data Upload'" ><b>{{ notification.user}}</b> added {{ notification.message }} for one of your key accounts.</p>
        <nuxt-link :to="`/tax/clients/${notification.seller_firm_public_id}`" class="mt-2">Go to seller firm</nuxt-link>

      </b-card-text>
      <b-card-text class="small text-muted">{{ $dateFns.formatDistanceToNow(new Date(notification.created_on)) }}</b-card-text>
    </b-card>
</template>

<script>
export default {
    name: 'CardNotification',
    props: {
        notification: {
            type: [Array, Object],
            required: true
        }
    }

}
</script>

<style>

</style>
