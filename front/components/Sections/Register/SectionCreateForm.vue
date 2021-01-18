<template>
  <div>
    <form-create-seller-firm v-show="page == 1" :registered="false" @next="page++ " />
    <form-create-seller v-show="page == 2" />
  </div>
</template>

<script>
export default {
  name: 'SectionCreateForm',
  data() {
    return {
      page: 1
    }
  },


}
</script>

<style>

</style>
