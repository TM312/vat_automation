<template>
  <section id="vat-compliance-company-information">
    <h6 class="text-primary">
      Step 2
    </h6>
    <h2>Company Overview</h2>
    <p class="lead my-2">
      Set up your company account within minutes by filling out the
      provided templates. You receive live updates if everything worked.
      Your company information is updated on the fly.
    </p>
    <b-tabs pills>
      <b-tab title="Company" active class="py-3">
        <p class="text-dark">
          Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed
          diam nonumy eirmod tempor invidunt ut labore et dolore magna
          aliquyam erat, sed diam voluptua. At vero eos et accusam et
          justo duo dolores et ea rebum.
        </p>
        <card-client />
      </b-tab>
      <b-tab title="Accounts" class="py-3">
        <p class="text-dark">
          Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed
          diam nonumy eirmod tempor invidunt ut labore et dolore.
        </p>
        <card-accounts showcase />
      </b-tab>
      <b-tab title="Vat Numbers" class="py-3">
        <p class="text-dark">
          Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed
          diam nonumy eirmod tempor invidunt ut labore et dolore.
        </p>
        <card-vat-numbers showcase />
      </b-tab>
      <b-tab title="Distance Sales" class="py-3">
        <p class="text-dark">
          Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed
          diam nonumy eirmod tempor invidunt ut labore et dolore.
        </p>
        <card-distance-sales showcase />
      </b-tab>
      <b-tab title="Items" class="py-3">
        <p class="text-dark">
          Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed
          diam nonumy eirmod tempor invidunt ut labore et dolore.
        </p>
        <card-items showcase :per-page="5" />
      </b-tab>
    </b-tabs>
  </section>
</template>

<script>
export default {
  name: "SectionVatComplianceCompanyInformation",
}
</script>
