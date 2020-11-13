<template>
  <div>
    <h2 class="text-center my-3">
      Platform Support
    </h2>
    <b-row class="my-3">
      <b-col />
      <b-col align-self="center" class="py-3">
        <b-img class="img-logo" src="@/assets/img/logos/amazon_logo_svg.svg" style="max-width: 15rem" />
      </b-col>
      <b-col />
    </b-row>
  </div>
</template>

<script>
export default {
  name: 'SectionSupportedPlatforms'
}
</script>

<style>
.img-logo {
    filter: invert(42%) sepia(50%) saturate(100%);
}

</style>
