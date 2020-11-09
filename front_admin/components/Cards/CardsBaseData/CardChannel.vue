<template>
  <b-card class="h-100">
    <b-card-title>
      <b-row>
        <b-col cols="auto">
          <b-form-input
            v-if="edit"
            v-model="form.name"
            :placeholder="channel.name"
          />
          <span v-else>{{ channel.name }}</span>
        </b-col>
        <b-col cols="auto ml-auto">
          <b-button
            variant="outline-warning"
            size="sm"
            :pressed.sync="edit"
          >
            <b-icon icon="pencil-square" /> Edit
          </b-button>
        </b-col>
      </b-row>
    </b-card-title>
    <b-card-sub-title>
      <b-row>
        <b-col cols="auto">
          <b-form-input
            v-if="edit"
            v-model="form.code"
            :placeholder="channel.code"
          />
          <span v-else>{{ channel.code }}</span>
        </b-col>
        <b-col cols="auto ml-auto">
          <b-button v-show="edit" variant="success" size="sm">
            Submit
          </b-button>
        </b-col>
      </b-row>
    </b-card-sub-title>
    <b-card-text class="mt-3">
      <b-form-textarea
        v-if="edit"
        v-model="form.description"
        :placeholder="channel.description"
        rows="3"
        max-rows="6"
      />
      <span v-else>{{ channel.description }}</span>
    </b-card-text>
  </b-card>
</template>

<script>
export default {
  name: 'CardChannel',

  props: {
    channel: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      edit: false,
      form: {
        name: null,
        code: null,
        description: null,
      },
    }
  },

}
</script>

<style>

</style>
