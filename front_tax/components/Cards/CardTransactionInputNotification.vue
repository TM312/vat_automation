<template>
  <b-card :border-variant="notification.status" :title="capitalize(notification.status)" :sub-title="notification.subject">
    <b-table :items="items" :fields="fields" borderless>
      <template v-slot:cell(key)="data">
        <b>{{ data.value }}</b>
      </template>
    </b-table>

    <p v-if="notification.message" class="my-2">
      {{ notification.message }}
    </p>

    <b-card-text class="small text-muted">
      <b-row>
        <b-col cols="auto" class="mr-auto">
          <span>{{ notification.original_filename }}</span>
        </b-col>
        <b-col cols="auto">
          <span v-if="notification.modified_at"> updated {{ $dateFns.formatDistanceToNow(new Date(notification.modified_at)) }} ago</span>
          <span v-else> {{ $dateFns.formatDistanceToNow(new Date(notification.created_on)) }} ago</span>
        </b-col>
      </b-row>
    </b-card-text>
  </b-card>
</template>

<script>
export default {
  name: 'CardTransactionNotification',
  props: {
    notification: {
      type: [Array, Object],
      required: true
    }
  },

  computed: {
    fields() {
      return [
        { key: 'key', label:'' },
        { key: 'value', label:'' }
      ]
    },
    items() {
      return [
        { key: 'Calculated Value', value: this.notification.calculated_value },
        { key: 'Reference Value', value: this.notification.reference_value }
      ]
    },

  },

}
</script>

<style>

</style>
