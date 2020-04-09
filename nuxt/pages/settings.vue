<template>
  <b-container class="my-5">
    <b-tabs content-class="mt-3 py-3">
      <b-tab title="General" active>
        <p><b>Email: </b>{{ self.email }}</p>
        <p><b>Registered On: </b>{{ self.registered_on }}</p>
        <p><b>Role: </b>{{ self.role }}</p>
      </b-tab>
    </b-tabs>
  </b-container>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState(['self'])
  }
}
</script>

<style></style>
