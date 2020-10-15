<template>
  <b-card border-variant="primary">
    <b-card-title>
      <b-row>
        <b-col cols="auto" class="mr-auto">
          {{ sellerFirm.name }}
        </b-col>
        <b-col cols="auto">
          <button-follow-seller-firm :seller-firm="sellerFirm" />
          <b-button v-if="$auth.user.role === 'admin'" size="sm" variant="outline-danger" :disabled="buttonDisabled" @click="remove(sellerFirm.public_id)">
            Delete
          </b-button>
        </b-col>
      </b-row>
    </b-card-title>
    <b-card-sub-title class="mb-3">
      {{ sellerFirm.address }} | Establishment: {{ sellerFirmEstablishmentCountry }}
    </b-card-sub-title>

    <b-card-text>
      <b-row v-if="sellerFirm.tax_auditors.length > 0">
        <b-col cols="auto">
          <b>Tax Auditors: </b>
        </b-col>
        <b-col cols="auto" class="mr-auto">
          <div v-if="sellerFirm.tax_auditors.length === 1">
            <b-avatar
              v-for="taxAuditor in sellerFirm.tax_auditors"
              :id="`popover-target-${taxAuditor.public_id}`"
              :key="taxAuditor.public_id"
              :variant="(taxAuditor.role === 'admin') ? 'success' : 'info'"
              :text="taxAuditor.initials"
            />
          </div>
          <div v-else>
            <b-avatar-group>
              <b-avatar
                v-for="taxAuditor in sellerFirm.tax_auditors"
                :id="`popover-target-${taxAuditor.public_id}`"
                :key="taxAuditor.public_id"
                :variant="(taxAuditor.role === 'admin') ? 'success' : 'info'"
                :text="taxAuditor.initials"
              />
            </b-avatar-group>
          </div>

          <b-popover
            v-for="(taxAuditor, index) in sellerFirm.tax_auditors"
            :key="index"
            :target="`popover-target-${taxAuditor.public_id}`"
            triggers="hover"
            variant="info"
            placement="top"
          >
            <template v-slot:title>
              {{ taxAuditor.name }}
            </template>
            <b>Role: </b> {{ capitalize(taxAuditor.role) }}
          </b-popover>
        </b-col>
      </b-row>
      <br />
      <b-row>
        <b-col cols="auto">
          <b>Created On:</b>
        </b-col>
        <b-col cols="auto" class="mr-auto">
          {{ sellerFirm.created_on }}
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="auto">
          <b>Created By:</b>
        </b-col>
        <b-col cols="auto" class="mr-auto">
          {{ sellerFirm.created_by }}
        </b-col>
      </b-row>
    </b-card-text>
  </b-card>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        name: 'CardClient',

        data() {
            return {
                buttonDisabled: false
            }
        },

        computed: {
            ...mapState({
                sellerFirm: state => state.seller_firm.seller_firm
            }),
            sellerFirmEstablishmentCountry() {
              return this.$store.getters['country/countryNameByCode'](this.sellerFirm.establishment_country_code)
            }
        },

        methods: {
            async remove(sellerFirmPublicId) {
                this.buttonDisabled = true
                try {
                    await this.$store.dispatch("seller_firm/delete_by_public_id", sellerFirmPublicId)
                    await this.$store.dispatch("accounting_firm/get_by_public_id", this.$auth.user.employer_public_id)
                    await this.$auth.fetchUser()


                    this.$router.push('/tax/clients')
                } catch (error) {
                    this.$toast.error(error, { duration: 5000 })
                    this.buttonDisabled = false
                    return []
                }
            },
        }


            // function() {
            //     var taxAuditors = this.seller_firm.tax_auditors
            //     return taxAuditors.map(function(index) {
            //         console.log('index:', index, 'index % 2 == 0:', index % 2 == 0)
            //         return (index % 2 == 0) ? 'success' : 'info'
            //     })
    }
</script>
