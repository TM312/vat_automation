<template>
    <b-card bg-variant="white">
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
                >
                <b-row>
                    <b-col cols="6" md="4">
                        <b-form-group
                            description="Country Code"
                        >
                            <b-form-select
                                id="country_code"
                                :options="optionsCountryCode"
                                v-model="payload.country_code"
                                :state="vatinVerified"
                                :disabled="buttonVerifyDisabled"
                            ></b-form-select>

                        </b-form-group>

                    </b-col>
                    <b-col cols="6" md="4">
                        <b-form-group
                            description="Number"
                        >
                            <b-form-input
                                id="number"
                                type="text"
                                :disabled="buttonVerifyDisabled"
                                v-model="payload.number"
                                :state="vatinVerified"
                                @input="vatinVerified=null"
                            >
                            </b-form-input>
                        </b-form-group>
                    </b-col>
                    <b-col v-show="payload.number !== null" cols="6" md="2">
                        <b-button
                            variant="outline-primary"
                            :disabled="buttonVerifyDisabled"
                            @click="verify"
                            block
                        >
                            <span v-if="!buttonVerifyBusy">Verify</span>
                            <span v-else><b-spinner small></b-spinner></span>
                        </b-button>
                    </b-col>
                    <b-col v-show="payload.number !== null" cols="6" md="2">
                        <b-button
                            variant="outline-secondary"
                            @click="reset"
                            block
                        >
                            <span>Reset</span>
                        </b-button>
                    </b-col>
                </b-row>

                <b-form-invalid-feedback :state="vatinVerified">
                    {{ vatinInvalidFeedback }}
                </b-form-invalid-feedback>

            </b-form-group>

            <b-form-group
                label-cols-sm="3"
                label-align-sm="right"
                label="Status"
                v-show="vatinVerified"
            >
                <b-collapse v-model="vatinVerified">
                    <b-button
                        v-if="!vatinValidated || (vatinValidated && payload.valid === null)"
                        @click="validate"
                        variant="outline-primary"
                        :disabled="buttonValidateDisabled"
                        block
                    >
                        <span v-if="buttonValidateBusy"><b-spinner small></b-spinner></span>

                        <span v-if="vatinValidated && payload.valid === null">Retry Validation</span>
                        <span v-else>Validate VATIN</span>

                    </b-button>
                    <div v-if="vatinValidated" class="mt-3">
                        <b-row>
                            <b-col cols="3" md="6">
                                <b-form-group>
                                    <b-form-input id="valid" :state="payload.valid" type="text" cols-sm="3" v-model="payloadValidString" disabled></b-form-input>
                                    <b-form-invalid-feedback :state="payload.valid">Only valid vat numbers are accepted for seller firms.</b-form-invalid-feedback>
                                </b-form-group>
                            </b-col>
                            <b-col cols="9" md="6">
                                <b-form-group description="Last Validation"><b-form-input id="request_date" type="text" cols-sm="3" :value="payload.request_date" disabled /></b-form-group>
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col>
                                <p v-if="payload.valid !== null || !payload.valid" class="text-secondary my-2">
                                    <small>{{ payload.name }}</small>
                                    <span
                                        v-if="payload.address !== null"
                                        class="text-secondary">
                                        <small>{{ payload.address }}</small>
                                    </span>
                                </p>
                            </b-col>
                        </b-row>

                    </div>
                </b-collapse>
            </b-form-group>

            <b-form-group
                v-show="vatinValidated && payload.request_date !== null"
                label-cols-sm="3"
                label-align-sm="right"
                label-for="valid_from"
                label="Valid From"
            >
                <b-form-datepicker
                    cols-sm="3"
                    id="valid_from"
                    v-model="payload.valid_from"
                    :disabled="payload.valid === false"
                ></b-form-datepicker>

            </b-form-group>

            <div cols-sm="3">
                <b-card
                    v-if="vatinValidated && payload.valid === null"
                    border-variant="warning"
                    class="my-3"
                >
                    <b-card-title>Attention</b-card-title>
                    <b-card-text>
                        <p>Retry the validation now or validate it at a later stage after the submission.</p>
                        <p>Make sure that the vat number has been validated <i>before</i> submitting transaction reports for this firm.</p>
                    </b-card-text>
                </b-card>


                <b-button
                    variant="primary"
                    @click="submitPayload()"
                    :disabled="submitDisabled"
                    class="mt-4"
                    block
                >
                    <b-icon icon="box-arrow-in-up" /> Add New Vat Number
                </b-button>
            </div>

        </b-form-group>

    </b-card>
</template>

<script>
    import { mapState } from "vuex";
    import { BIcon } from "bootstrap-vue";

    export default {
        name: 'FormAddSellerFirmVatNumber',

        components: {
            BIcon
        },

        data() {
            return {
                payload: {
                    country_code: null,
                    number: null,
                    valid: null,
                    request_date: null,
                    name: null,
                    address: null,
                    valid_from: null,
                    valid_to: null
                },

                vatinVerified: null,
                vatinValidated: null,

                buttonVerifyDisabled: false,
                buttonVerifyBusy: false,

                buttonValidateDisabled : false,
                buttonValidateBusy : false
            }
        },

        computed: {
            ...mapState({
                countries: state => state.country.countries,
                vatin: state => state.vatin.vatin
            }),

            payloadValidString() {
                if (this.payload.request_date) {
                    if (this.payload.valid === true) {
                        return 'Valid'
                    } else if (this.payload.valid === false) {
                        return 'Invalid'
                    } else {
                        return 'Validation Failed'
                    }
                } else {
                    return ''
                }
            },


            vatinInvalidFeedback() {
                if (this.payload.country_code && this.payload.number) {
                    return `${this.payload.country_code} - ${this.payload.number} does not match any country's vat number specification. Please recheck the input.`

                } else if (this.payload.country_code === null && this.payload.number) {
                    return `${this.payload.number} does not match any country's vat number specification. Please recheck the input.`

                } else if (this.payload.country_code && this.payload.number === null) {
                    return `${this.payload.country_code} does not match any country's vat number specification. Please recheck the input.`

                } else {
                    return "The provided input does not match any country's vat number specification. Please recheck the input."
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

            submitDisabled() {
                if (
                    (this.payload.valid === true || this.payload.valid === null) &&
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

                // const res = await this.$axios.post('/tax/vatin/verify', this.payload)

                await this.$store.dispatch(
                    "vatin/verify",
                    this.payload
                );


                if (this.vatin.valid === null) {
                    // this.reset()
                    this.buttonVerifyDisabled = false
                    this.vatinVerified = false

                } else {
                    this.vatinVerified = this.vatin.verified
                    this.buttonVerifyDisabled = this.vatin.verified
                    this.payload.country_code = this.vatin.country_code
                    this.payload.number = this.vatin.number
                }


                this.buttonVerifyBusy = false
                this.payload.valid_from = null
            },

            reset() {
                this.payload = {
                    country_code: null,
                    number: null,
                    valid: null,
                    request_date: null,
                    name: null,
                    address: null,
                    valid_from: null,
                },

                this.vatinVerified = null,
                this.vatinValidated = null,

                this.buttonVerifyDisabled = false,
                this.buttonVerifyBusy = false,

                this.buttonValidateDisabled = false,
                this.buttonValidateBusy = false
            },

            async validate() {
                this.buttonValidateDisabled = true
                this.buttonValidateBusy = true

                this.payload.request_date = null

                await this.$store.dispatch(
                    "vatin/validate",
                    this.payload
                );


                if (this.vatin) {
                    this.payload = {
                        country_code: this.vatin.country_code,
                        number: this.vatin.number,
                        valid: this.vatin.valid,
                        request_date: this.vatin.request_date,
                        name: this.vatin.name,
                        address: this.vatin.address,
                        valid_from: this.$dateFns.format(new Date(), 'yyyy-MM-dd')
                    }

                    this.vatinValidated = (this.vatin.valid || this.vatin.valid === null) ? true : false

                } else {
                    await this.$toast.error('Oops, an error occured.', {
                        duration: 1000
                    });
                }
                if (!this.vatinValidated || this.vatin.valid === null) {
                    this.buttonValidateDisabled = false
                }

                this.buttonValidateBusy = false
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
                    await this.$toast.success('New vat number succesfully added.', {
                        duration: 5000
                    });

                    this.reset()

                } catch (error) {
                    this.$toast.error(error, { duration: 5000 });
                }
            },

            async create_by_seller_firm_public_id() {
                const data_array = [this.$route.params.public_id, this.payload]

                await this.$store.dispatch(
                    "vatin/create_by_seller_firm_public_id",
                    data_array
                );
            },
        }
    }
</script>

<style>

</style>
