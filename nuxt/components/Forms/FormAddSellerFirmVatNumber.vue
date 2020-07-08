<template>
    <b-card bg-variant="white">
        <p>payload.valid_from: {{ payload.valid_from }}</p>
        <p>payload.valid_to: {{ payload.valid_to }}</p>
        <p>this.payload.valid: {{ payload.valid }}</p>
        <p>vatinVerified: {{ vatinVerified }}</p>
        <p>vatinValidated: {{ vatinValidated }}</p>
        <p>validationValidTo: {{ validationValidTo }}</p>
        <br>
        <b-form-group
            label-cols-lg="2"
            label="New Vat Number"
            label-size="lg"
            label-class="font-weight-bold pt-0"
            class="mb-2"
        >
            <b-form-group
                label-cols-sm="3"
                label-align-sm="right"
                label="VATIN"
                :invalid-feedback="vatinInvalidFeedback"
            >
                <b-row>
                    <b-col cols="4">
                        <b-form-select
                            id="country_code"
                            :options="optionsCountryCode"
                            v-model="payload.country_code"
                            :state="vatinVerified"
                            :disabled="buttonVerifyDisabled"
                        ></b-form-select>
                    </b-col>
                    <b-col cols="4">
                        <b-form-input
                            id="number"
                            type="text"
                            :disabled="buttonVerifyDisabled"
                            v-model="payload.number"
                            :state="vatinVerified"
                        >
                            <b-form-invalid-feedback :state="vatinVerified">
                                {{ vatinInvalidFeedback }}
                            </b-form-invalid-feedback>
                        </b-form-input>
                    </b-col>
                    <b-col cols="2">
                        <b-button
                            variant="outline-primary"
                            class="mr-auto"
                            :disabled="buttonVerifyDisabled"
                            @click="verify"
                            block
                        >
                            <span v-if="!buttonVerifyBusy">Verify</span>
                            <span v-else><b-spinner small></b-spinner></span>
                        </b-button>
                    </b-col>
                    <b-col cols="2">
                        <b-button
                            variant="outline-secondary"
                            class="mr-auto"
                            @click="reset"
                            block
                        >
                            <span>Reset</span>
                        </b-button>
                    </b-col>
                </b-row>

            </b-form-group>

            <b-form-group
                label-cols-sm="3"
                label-align-sm="right"
                label="Status"
            >
                <b-collapse v-model="vatinVerified ">
                    <b-button v-if="!vatinValidated" @click="validate" variant="outline-primary" block>Validate VATIN</b-button>
                    <div v-else>
                        <b-form-input id="valid" :state="payload.valid" type="text" cols-sm="3" v-model="payloadValidString" disabled>
                            <b-form-invalid-feedback :state="payload.valid">Only valid vat numbers are accepted for seller firms. Please enter a different one.</b-form-invalid-feedback>
                        </b-form-input>
                        <p class="text-secondary my-2">
                            <small>{{ payload.name }}</small>
                            <span
                                v-if="payload.address !== null"
                                class="text-secondary">
                                <small>{{ payload.address }}</small>
                            </span>
                        </p>

                        <!-- <b-form-input id="name" type="text" cols-sm="3" disabled v-model="payload.name" />
                        <b-form-input id="address" type="text" cols-sm="3" disabled v-model="payload.address" /> -->
                    </div>
                </b-collapse>
            </b-form-group>

            <b-form-group
                label-cols-sm="3"
                label-align-sm="right"
                label-for="valid_from"
                label="Valid From"
            >
                <b-row>
                    <b-col cols="9">
                        <b-form-datepicker
                            cols-sm="3"
                            id="valid_from"
                            v-model="payload.valid_from"
                            :disabled="!payload.valid"
                        ></b-form-datepicker>
                    </b-col>
                    <b-col cols="3">
                        <b-button
                            v-if="vatinValidated"
                            variant="outline-primary"
                            class="mr-auto"
                            block
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
                :state="validationValidTo"
                label="Valid To"
            >
                <b-row>
                    <b-col cols="9">
                        <b-form-datepicker
                            id="valid_to"
                            :state="validationValidTo"
                            :disabled="!payload.valid"
                            v-model="payload.valid_to"
                        ></b-form-datepicker>
                    </b-col>
                </b-row>

            </b-form-group>
        </b-form-group>


        <b-button
            variant="primary"
            @click="submitPayload()"
            :disabled="submitDisabled"
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

                vatinVerified: null,
                vatinValidated: false,

                buttonVerifyDisabled: false,
                buttonVerifyBusy: false,

                buttonValidateDisabled : false,
                buttonValidateBusy : false
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

            payloadValidString() {
                return this.payload.valid ? 'Valid' : 'Invalid'
            },


            vatinInvalidFeedback() {
                return `${this.payload.number} does not match the country's VAT ID specifications.`
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

            validationValidTo() {
                if (this.payload.valid_to === null) {
                    return null
                } else {
                    var valid_from = this.payload.valid_from.split('-');
                    var valid_from_date = new Date(valid_from[0], valid_from[1] - 1, valid_from[2]);

                    var valid_to = this.payload.valid_to.split('-');
                    var valid_to_date = new Date(valid_to[0], valid_to[1] - 1, valid_to[2]);

                    return valid_from_date <= valid_to_date;
                }
            },

            submitDisabled() {
                if (
                    this.payload.valid === true &&
                    this.vatinVerified === true &&
                    this.vatinValidated === true
                ) {
                    return false;
                } else {
                    return true;
                }
            }
        },

        methods: {

            async verify() {
                this.buttonVerifyDisabled = true
                this.buttonVerifyBusy = true

                // removes all empty values from object : https://stackoverflow.com/questions/23774231/how-do-i-remove-all-null-and-empty-string-values-from-a-json-object
                Object.keys(this.payload).forEach(k => (!this.payload[k] && this.payload[k] !== undefined) && delete this.payload[k]);

                const res = await this.$axios.post('/tax/vatin/verify', this.payload)
                const { status, data } = res
                if (status === 200 && data) {
                    this.vatinVerified = data.verified
                    this.buttonVerifyDisabled = data.verified
                    this.payload.country_code = data.country_code
                    this.payload.number = data.number
                    this.payload.valid_from = data.valid_from
                    this.payload.valid_to = data.valid_to

                    console.log('data.valid_from: ', data.valid_from)
                    console.log('data.valid_to: ', data.valid_to)

                    console.log('as string? to: ', new Date(data.valid_to).toISOString().slice(0,10))
                    console.log('as string? from: ', new Date(data.valid_from).toISOString().slice(0,10))

                }

                this.buttonVerifyBusy = false
                this.payload.valid_from = null
                this.payload.valid_to = null
            },

            reset() {
                this.buttonVerifyDisabled = false
                this.vatinVerified = null
                this.vatinValidated = false

                this.payload.country_code = null
                this.payload.number = null
                this.payload.valid = null
                this.payload.name = null
                this.payload.address = null
                this.payload.valid_from = null
                this.payload.valid_to = null
            },

            async validate() {
                this.buttonValidateDisabled = true
                this.buttonValidateBusy = true

                // removes all empty values from object : https://stackoverflow.com/questions/23774231/how-do-i-remove-all-null-and-empty-string-values-from-a-json-object
                Object.keys(this.payload).forEach(k => (!this.payload[k] && this.payload[k] !== undefined) && delete this.payload[k]);

                const res = await this.$axios.post('/tax/vatin/validate', this.payload)
                const { status, data } = res
                if (status === 200 && data) {
                    this.payload.country_code = data.country_code,
                    this.payload.number = data.number,
                    this.payload.valid = data.valid,
                    this.payload.name = data.name,
                    this.payload.address = data.address

                    this.vatinValidated = true

                } else {
                    await this.$toast.error(data.message, {
                        duration: 1000
                    });
                }
                this.buttonValidateBusy = false
            },

            setToday() {
                const today = new Date()
                this.payload.valid_from = new Date(today.getFullYear(), today.getMonth(), today.getDate())
                console.log('set Today this.valid_from: ', this.payload.valid_from)
            },

            // getTodayAsYYYYMMDD() {
            //     var today = new Date();
            //     var dd = String(today.getDate()).padStart(2, "0");
            //     var mm = String(today.getMonth() + 1).padStart(2, "0"); //January is 0!
            //     var yyyy = today.getFullYear();

            //     const today_string = yyyy + "-" + mm + "-" + dd;
            //     return today_string

            // },

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
