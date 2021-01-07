<template>
  <div>
    <form-create-seller v-show="page == 1" @next="page++ " />
    <form-create-seller-firm v-show="page == 2" :registered="false" />
    <b-button variant="outline-primary" pill @click="page == 1 ? page++ : page--">
      Next Page
    </b-button>
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
