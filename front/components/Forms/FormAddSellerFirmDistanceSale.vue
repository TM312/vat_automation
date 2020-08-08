<template>
    <b-card bg-variant="white">
        <b-form-group
            label-cols-lg="3"
            label="New Distance Sale"
            label-size="lg"
            label-class="font-weight-bold pt-0"
            class="mb-2"
        >

            <b-form-group
                label-cols-sm="3"
                label-align-sm="right"
                label-for="arrival_country"
                label="Arrival Country"
            >
                <b-form-select v-if="$fetchState.pending" id="arrival_country" disabled />
                <b-form-select
                    v-else
                    id="arrival_country"
                    :options="optionsArrivalCountry"
                    v-model="payload.arrival_country_code"
                ></b-form-select>
            </b-form-group>

            <b-form-group
                label-cols-sm="3"
                label-align-sm="right"
                label-for="active"
                label="Active"
            >
                <b-form-checkbox
                    id="active"
                    v-model="payload.active"
                    size="lg"
                    class="mt-1"
                    switch
                ></b-form-checkbox>
            </b-form-group>

            <b-form-group
                label-cols-sm="3"
                label-align-sm="right"
                label-for="valid_from"
                label="Valid From"
            >
                <b-form-datepicker
                    id="valid_from"
                    v-model="payload.valid_from"
                ></b-form-datepicker>
            </b-form-group>

            <b-form-group
                label-cols-sm="3"
                label-align-sm="right"
                label-for="valid_to"
                invalid-feedback="'Valid From' needs to predate 'Valid To'"
                :state="validation_valid_to"
                label="Valid To"
                description="If you do not pass a final validity date, it will be considered valid until updated."
            >
                <b-form-datepicker
                    id="valid_to"
                    :state="validation_valid_to"
                    v-model="payload.valid_to"
                ></b-form-datepicker>
            </b-form-group>
        </b-form-group>


        <b-button
                variant="primary"
                @click="submitPayload()"
                :disabled="validation_submit"
                block
            >
                <b-icon icon="box-arrow-in-up" /> Add New Distance Sale
        </b-button>
    </b-card>
</template>

<script>
    import { mapState } from "vuex";

    export default {
        name: 'FormAddSellerFirmDistanceSale',

        data() {
            return {
                payload: {
                        arrival_country_code: null,
                        valid_from: null,
                        valid_to: null,
                        active: false
                    }
            }
        },

        async fetch() {
            const { store } = this.$nuxt.context;
            // https://stackoverflow.com/questions/23593052/format-javascript-date-as-yyyy-mm-dd
            var todayDate = new Date().toISOString().slice(0,10);
            await store.dispatch("country/get_eu_by_date", todayDate);
        },

        computed: {
            ...mapState({
                eu: state => state.country.eu
            }),

            optionsArrivalCountry() {
                let options = this.eu.countries.map(country => {
                    let properties = {
                        value: country.code,
                        text: country.name
                    };
                    return properties;
                });
                return options;
            },

            validation_valid_to() {
                if (this.payload.valid_to !== null) {

                    return this.payload.valid_from <= this.payload.valid_to;

                } else {
                    return null;
                }
            },

            validation_submit() {
                if (
                    this.payload.arrival_country_code !== null &&
                    this.payload.valid_from !== null &&
                    this.validation_valid_to !== false
                ) {
                    return false;
                } else {
                    return true;
                }
            }
        },

        methods: {
            async submitPayload() {
                try {
                    // removes all empty values from object : https://stackoverflow.com/questions/23774231/how-do-i-remove-all-null-and-empty-string-values-from-a-json-object
                    Object.keys(this.payload).forEach(k => (!this.payload[k] && this.payload[k] !== undefined) && delete this.payload[k]);

                    await this.create_by_seller_firm_public_id();

                    this.payload.arrival_country_code = null;

                    await this.$store.dispatch(
                        "seller_firm/get_by_public_id",
                        this.$route.params.public_id
                    );
                    this.$emit('flash')
                    await this.$toast.success('New distance sale succesfully added.', {
                        duration: 5000
                    });
                } catch (error) {
                    this.$toast.error(error, { duration: 5000 });
                }
            },

            async create_by_seller_firm_public_id() {
                const data_array = [this.$route.params.public_id, this.payload]

                await this.$store.dispatch(
                    "distance_sale/create_by_seller_firm_public_id",
                    data_array
                );
            },
        }
    }
</script>

<style>

</style>
