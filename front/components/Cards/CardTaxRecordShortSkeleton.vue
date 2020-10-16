<template>
  <b-card>
    <b-card-title><b-skeleton /></b-card-title>
    <b-card-sub-title class="mb-2">
      <b-skeleton /> – <b-skeleton />
    </b-card-sub-title>

    <b-card-text>
      <b-row>
        <b-col cols="auto">
          <b>Taxable Turnover Amount:</b>
          <br />
          <b>Payable Vat Amount:</b>
        </b-col>
        <b-col>
          <b-skeleton />
          <br />
          <b-skeleton />
        </b-col>
      </b-row>
      <b-row class="mt-2">
        <b-col>
          <p class="text-muted">
            Details
          </p>
        </b-col>
      </b-row>
    </b-card-text>
  </b-card>
</template>

<script>
    export default {
        name: 'CardTaxRecordShortSkeleton'
    }
</script>
