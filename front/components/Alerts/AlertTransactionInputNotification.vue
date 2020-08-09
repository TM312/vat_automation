<template>
    <b-alert :variant="notification.status" show>
        <b>Subject:</b> {{ notification.subject }} <br>
        <p>Calculated Value: {{ notification.calculated_value }}</p>
        <p>Reference Value: {{ notification.reference_value }}</p>
        <p v-if="notification.message">{{ notification.message }}</p>
        <hr>
        <p class="mb-0 text-muted text-right"><small>{{ createdOnDistance }}</small></p>
    </b-alert>
</template>

<script>
export default {
    name: 'AlertTransactionNotification',
    props: {
        notification: {
            type: [Array, Object],
            required: true
        }
    },
    computed: {
        createdOnDistance() {
            return this.$dateFns.formatDistanceToNow(new Date(this.notification.created_on))
        }
    },

}
</script>

<style>

</style>
