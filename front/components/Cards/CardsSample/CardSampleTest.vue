<template>
  <div class="card-sample">
    <b-row>
      <b-col cols="5">
        <b-img src="@/assets/img/illustrations/data_upload.svg" fluid />
      </b-col>
      <b-col cols="7">
        <h6 class="text-primary">
          Sample Company
        </h6>
        <h4>Bond Store Ltd</h4>
        <p class="my-2 text-dark">
          The sample company at hand is the 'Bond Store Ltd' based in London, GB.
        </p>
      </b-col>
    </b-row>
    <p class="text-muted text-right">
      1/XX
    </p>
  </div>
</template>

<script>
export default {
  name: "CardSampleTest",
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
        min-width: 30rem;
        max-width: 50rem;
        box-shadow: 6px 6px 12px #bdbcbc, -6px -6px 12px #ffffff !important;
    }
</style>
