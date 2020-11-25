<template>
  <div class="card-sample">
    <b-row>
      <b-col v-if="illustration!==''" cols="4">
        <b-img
          v-if="illustration === 'data_upload.svg'"
          src="@/assets/img/illustrations/data_upload.svg"
          fluid
        />
        <b-img
          v-else-if="illustration === 'processing.svg'"
          src="@/assets/img/illustrations/processing.svg"
          fluid
        />
        <b-img
          v-else-if="illustration === 'seller.svg'"
          src="@/assets/img/illustrations/seller.svg"
          fluid
        />
        <b-img
          v-else-if="illustration === 'data.svg'"
          src="@/assets/img/illustrations/data.svg"
          fluid
        />
      </b-col>
      <b-col cols="8">
        <h6 class="text-primary">
          <!-- {{ primer }} -->
          Sample Case
        </h6>
        <h4 class="text-dark">
          {{ primer }}
        </h4>
      </b-col>
    </b-row>
    <div>
      <p class="my-2 text-dark">
        {{ description }}
      </p>
    </div>
    <b-row align-h="between" class="text-muted">
      <b-col cols="auto">
        <!-- <small>Sample Case</small> -->
      </b-col>
      <b-col cols="auto">
        <small>{{ page }}/{{ total }}</small>
      </b-col>
    </b-row>
  </div>
</template>

<script>
export default {
  name: "CardSample",
  props: {
    page: {
      type: Number,
      required: true,
    },
    total: {
      type: Number,
      required: true,
    },
    primer: {
      type: String,
      required: true,
    },
    // heading: {
    //   type: String,
    //   required: true,
    // },
    description: {
      type: String,
      required: true,
    },
    illustration: {
      type: String,
      required: false,
      default: ''
    },
  },

  computed: {
    src() {
      return `@/assets/img/illustrations/${this.illustration}`
    },
  },
}
</script>

<style>
    .card-sample {
        background-color: rgb(166, 241, 241);
        padding-bottom: 1rem;
        padding-left: 3rem;
        padding-right: 3rem;
        padding-top: 3rem;
        border-radius: 15px;
        box-shadow: 6px 6px 12px #bdbcbc, -6px -6px 12px #ffffff !important;
    }
</style>
