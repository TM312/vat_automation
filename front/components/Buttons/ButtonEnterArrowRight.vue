<template>
  <b-button
    :pill="pill"
    :variant="variant"
    :to="to"
    @mouseover="buttonHover = true"
    @mouseleave="buttonHover = false"
  >
    {{ content }}
    <b-icon
      :icon="buttonHover ? 'arrow-right-short' : 'chevron-right'"
      class="ml-1"
    />
  </b-button>
</template>

<script>
export default {
  name: "ButtonEnterArrowRight",

  props: {
    to: {
      type: String,
      required: false,
      default: "/vat-compliance"
    },
    variant: {
      type: String,
      required: false,
      default: 'outline-primary'
    },
    content: {
      type: String,
      required: true,
    }

  },

  data() {
    return {
      buttonHover: false,
    }
  },
  computed: {
    pill() {
      return this.variant !== 'link'
    }
  },
}
</script>

<style>
</style>
