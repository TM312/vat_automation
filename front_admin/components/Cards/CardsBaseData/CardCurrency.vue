<template>
  <b-card class="h-100">
    <b-card-title>
      <b-row>
        <b-col cols="auto">
          <b-form-input
            v-if="edit"
            v-model="form.name"
            :placeholder="currency.name"
          />
          <span v-else>{{ currency.name }}</span>
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
            :placeholder="currency.code"
          />
          <span v-else>{{ currency.code }}</span>
        </b-col>
        <b-col cols="auto ml-auto">
          <b-button v-show="edit" variant="success" size="sm">
            Submit
          </b-button>
        </b-col>
      </b-row>
    </b-card-sub-title>
  </b-card>
</template>

<script>
export default {
  name: "CardCurrency",

  props: {
    currency: {
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
      },
    }
  },
}
</script>

<style>
</style>
