<template>
  <div>
    {{ token }}
    {{ token_valid }}
  </div>
</template>

<script>
export default {
  data() {
    return {
      token: this.$route.params.token,
      token_valid: null,
    }
  },
  created() {
    this.$axios
      .post('/email/confirm', { token: this.token })

      .then(function (response) {
        console.log(response.data)
      })

      .catch(function (error) {
        console.log(error)
      })
  },
}
</script>

<style></style>
