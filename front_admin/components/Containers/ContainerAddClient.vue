<template>
  <b-tabs content-class="mt-3">
    <b-tab title="Single Client">
      <form-add-seller-firm />
    </b-tab>
    <b-tab title="Form Upload" active>
      <container-add-multiple-seller-firms />
    </b-tab>
  </b-tabs>
</template>

<script>

export default {
  name: 'ContainerAddClient'

}
</script>

<style>

</style>
