<template>
    <div>
        <b-card>
            <b-card-title>
                <b-row>
                    <b-col cols="auto" class="mb-2">{{ taxJurisdiction.name }}</b-col>
                    <b-col cols="auto ml-auto"><b-button variant="outline-danger" :disabled="buttonDisabled" @click="remove(taxRecord.public_id)">Delete</b-button></b-col>
                </b-row>
            </b-card-title>
            <b-card-sub-title>
                {{ $dateFns.format(taxRecord.start_date, 'MMMM dd, yyyy') }} – {{ $dateFns.format(taxRecord.end_date, 'MMMM dd, yyyy') }} <br>
                {{ taxRecord.vatin }}

            </b-card-sub-title>

            <b-card-text>
                <b>Taxable Turnover Amount:</b>{{ Number.parseFloat(taxRecord.taxable_turnover_amount).toFixed(2) }} {{ taxRecord.currency_code }} <br>
                <b>Payable Vat Amount:</b>{{ Number.parseFloat(taxRecord.taxable_turnover_amount).toFixed(2) }} {{ taxRecord.currency_code }}
            </b-card-text>

        </b-card>

    </div>
</template>

<script>
import { mapState } from "vuex";

export default {
    name: 'CardTaxRecord',

    data() {
        return {
            buttonDisabled: false,


        }
    },

    computed: {
        ...mapState({
            taxRecord: state => state.tax_record.tax_record,
            countries: state => state.country.countries,
            currencies: state => state.currency.currencies
        }),


        taxJurisdiction() {
            return this.countries.find(country => country.code == this.taxRecord.tax_jurisdiction_code)
        },


    },

    methods: {
        async remove(taxRecordPublicId) {
            this.buttonDisabled = true;
            try {
                await this.deleteFile(taxRecordPublicId);
                await this.$store.dispatch(
                    "seller_firm/get_by_public_id",
                    this.$route.params.public_id
                );
                this.buttonDisabled = false;
            } catch (error) {
                this.$toast.error(error, { duration: 5000 });
                this.buttonDisabled = false;
                return [];
            }
        },

        async deleteFile(taxRecordPublicId) {
            await this.$store.dispatch(
                "tax_record/delete_by_public_id",
                taxRecordPublicId
            );
        }
    },


}
</script>

<style>

</style>
