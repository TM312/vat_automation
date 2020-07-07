<template>
    <b-card bg-variant="white">
        <b-form-group
            label-cols-lg="3"
            label="New Vat Number"
            label-size="lg"
            label-class="font-weight-bold pt-0"
            class="mb-2"
        >
            <b-form-group
                label-cols-sm="3"
                label-align-sm="right"
                label="VATIN"
            >
                <b-row>
                    <b-col cols="2">
                        <b-form-select
                            id="country_code"
                            :options="optionsCountryCode"
                            v-model="payload.country_code"
                        ></b-form-select>
                    </b-col>
                    <b-col cols="7">
                        <b-form-input
                            id="number"
                            type="text"
                            v-model="payload.number"
                        ></b-form-input>
                    </b-col>
                    <b-col cols="2">
                        <b-button
                            variant="outline-primary"
                            :disabled="buttonDisabled"
                            @click="verify"
                            :state="payload.valid"
                        >
                            <span v-if="!buttonBusy">Verify</span>
                            <span v-else><b-spinner small></b-spinner></span>
                        </b-button>
                    </b-col>
                </b-row>

            </b-form-group>

            <b-form-group
                label-cols-sm="3"
                label-align-sm="right"
                label-for="valid_from"
                label="Valid From"
            >
                <b-row align-h="between">
                    <b-col cols="9">
                        <b-form-datepicker
                            cols-sm="3"
                            id="valid_from"
                            v-model="payload.valid_from"
                            @context="onContext"
                        ></b-form-datepicker>
                    </b-col>
                    <b-col cols="3">
                        <b-button
                            variant="outline-primary"
                            class="ml-auto"
                            @click="setToday"
                        >Set Today</b-button>
                    </b-col>
                </b-row>

            </b-form-group>

            <b-form-group
                label-cols-sm="3"
                label-align-sm="right"
                label-for="valid_to"
                invalid-feedback="'Valid From' needs to predate 'Valid To'"
                :state="validation_valid_to"
                label="Valid To"
                :description="getValidToDescription"
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
            <b-icon icon="box-arrow-in-up" /> Add New Vat Number
        </b-button>
    </b-card>
</template>

<script>
    import { mapState } from "vuex";

    export default {
        name: 'FormAddSellerFirmVatNumber',

        data() {
            return {
                payload: {
                    country_code: null,
                    number: null,
                    valid: null,
                    name: null,
                    address: null,
                    valid_from: null,
                    valid_to: null
                },

                valid_to_formatted: null,
                valid_from_selected: null,

                buttonDisabled: false,
                buttonBusy: false
            }
        },

        async fetch() {
            const { store } = this.$nuxt.context;
            await store.dispatch("country/get_all");
        },

        computed: {
            ...mapState({
                countries: state => state.country.countries
            }),

            getValidToDescription() {
                if (this.valid_to === null) {
                    var today = new Date();
                    const array = [this.valid_from_selected, today]
                    var valid_to_base = Math.max.apply(Math, array);
                    var valid_to_calc = new Date().setDate(valid_to_base.getDate()+30)
                    return `If you do not pass a final validity date, the vat number will be considered valid until ${ valid_to_calc } and rechecked if necessary.`
                } else {
                    return null
                }
            },

            optionsCountryCode() {
                const countriesShort = this.countries.filter(country => (country.vat_country_code !== undefined && country.vat_country_code !== null))

                let options = countriesShort.map(country => {
                    let properties = {
                        value: country.vat_country_code,
                        text: country.vat_country_code
                    };
                    return properties;

                    })
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
                    this.payload.country_code !== null &&
                    this.payload.number !== null
                ) {
                    return false;
                } else {
                    return true;
                }
            }
        },

        methods: {

            async verify() {
                this.buttonDisabled = true
                this.buttonBusy = true

                console.log('this.payload: ', this.payload)
                this.valid = await this.$axios.post('/tax/vatin/verify', this.payload)

                if (!this.valid) {
                    this.buttonDisabled = false
                }
                this.buttonBusy = false
            },

            setToday() {
                const today = new Date()
                this.payload.valid_from = new Date(today.getFullYear(), today.getMonth(), today.getDate())
                console.log('set Today this.valid_from: ', this.payload.valid_from)
            },

            onContext(ctx) {
                // The following will be an empty string until a valid date is entered
                this.valid_from_selected = ctx.selectedYMD
            },

            getTodayAsYYYYMMDD() {
                var today = new Date();
                var dd = String(today.getDate()).padStart(2, "0");
                var mm = String(today.getMonth() + 1).padStart(2, "0"); //January is 0!
                var yyyy = today.getFullYear();

                const today_string = yyyy + "-" + mm + "-" + dd;
                return today_string

            },

            async submitPayload() {
                try {
                    // removes all empty values from object : https://stackoverflow.com/questions/23774231/how-do-i-remove-all-null-and-empty-string-values-from-a-json-object
                    Object.keys(this.payload).forEach(k => (!this.payload[k] && this.payload[k] !== undefined) && delete this.payload[k]);

                    await this.create_by_seller_firm_public_id();

                    this.payload.number = null;


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
                    "vat_number/create_by_seller_firm_public_id",
                    data_array
                );
            },
        }
    }
</script>

<style>

</style>
