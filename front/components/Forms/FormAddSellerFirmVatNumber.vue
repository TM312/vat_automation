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
                :invalid-feedback="vatinInvalidFeedback"
            >
                <b-row>
                    <b-col cols="6" md="4" class="mb-2">
                        <b-form-select
                            id="country_code"
                            :options="optionsCountryCode"
                            v-model="payload.country_code"
                            :state="vatinVerified"
                            :disabled="buttonVerifyDisabled"
                        ></b-form-select>
                    </b-col>
                    <b-col cols="6" md="4">
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
                    <b-col cols="6" md="2">
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
                    <b-col cols="6" md="2">
                        <b-button
                            variant="outline-secondary"
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
                        <b-row>
                            <b-col cols="3" md="6">
                                <b-form-input id="valid" :state="payload.valid" type="text" cols-sm="3" v-model="payloadValidString" disabled>
                                    <b-form-invalid-feedback :state="payload.valid">Only valid vat numbers are accepted for seller firms. Please enter a different one.</b-form-invalid-feedback>
                                </b-form-input>
                                <b-card border-variant="warning">
                                    <b-card-header bg-variant="warning"><b-icon icon="info" /> Attention</b-card-header>
                                    <b-card-text v-if="vatinValidated === null">We have been unable to validate the provided vat number. You can either try to manually resend the validation request again or submit the data now and validate it later. Just make sure that the number has been validated before submitting your transaction reports.</b-card-text>
                                </b-card>
                            </b-col>
                            <b-col cols="9" md="6">
                                <b-form-group description="Last Validated"><b-form-input id="request_data" type="text" cols-sm="3" :value="payload.request_data" disabled /></b-form-group>
                            </b-col>
                        </b-row>

                        <p class="text-secondary my-2">
                            <small>{{ payload.name }}</small>
                            <span
                                v-if="payload.address !== null"
                                class="text-secondary">
                                <small>{{ payload.address }}</small>
                            </span>
                        </p>

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
                    <b-col cols="6" lg="9">
                        <b-form-datepicker
                            cols-sm="3"
                            id="valid_from"
                            v-model="payload.valid_from"
                            :disabled="!payload.valid"
                        ></b-form-datepicker>
                    </b-col>
                    <b-col cols="6" lg="3"><b-button v-if="payload.valid" @click="setToday" variant="outline-primary" block>Set Today</b-button></b-col>
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
    import { BIcon } from "bootstrap-vue";

    export default {
        name: 'FormAddSellerFirmVatNumber',

        data() {
            return {
                payload: {
                    country_code: null,
                    number: null,
                    valid: null,
                    request_data: null,
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

        async fetch() {
            const { store } = this.$nuxt.context;
            await store.dispatch("country/get_all");
        },

        computed: {
            ...mapState({
                countries: state => state.country.countries
            }),

            payloadValidString() {
                if (this.payload.valid === true) {
                    return 'Valid'
                } else if (this.payload.valid === false) {
                    return 'Invalid'
                } else {
                    return 'Validation Failed'
                }
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
            setToday() {
                this.payload.valid_from = this.$dateFns.format(new Date(), 'yyyy-MM-dd')
            },


            async verify() {
                this.buttonVerifyDisabled = true
                this.buttonVerifyBusy = true

                const res = await this.$axios.post('/tax/vatin/verify', this.payload)

                const { status, data } = res
                if (status === 200 && data) {
                    if (data.country_code === null || data.number === null) {
                        this.reset()
                        this.payload.country_code = false,
                        this.payload.number = false

                    } else {
                        this.vatinVerified = data.verified
                        this.buttonVerifyDisabled = data.verified
                        this.payload.country_code = data.country_code
                        this.payload.number = data.number
                    }
                }

                this.buttonVerifyBusy = false
                this.payload.valid_from = null
            },

            reset() {
                this.payload = {
                    country_code: null,
                    number: null,
                    valid: null,
                    request_data: null,
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

                // removes all empty values from object : https://stackoverflow.com/questions/23774231/how-do-i-remove-all-null-and-empty-string-values-from-a-json-object
                Object.keys(this.payload).forEach(k => (!this.payload[k] && this.payload[k] !== undefined) && delete this.payload[k]);

                const res = await this.$axios.post('/tax/vatin/validate', this.payload)
                const { status, data } = res
                if (status === 200 && data) {
                    this.payload = {
                        country_code: data.country_code,
                        number: data.number,
                        valid: data.valid,
                        request_data: data.request_data,
                        name: data.name,
                        address: data.address,
                        valid_from: this.$dateFns.format(new Date(), 'yyyy-MM-dd')
                        }

                    this.vatinValidated = data.valid ? true : false

                } else {
                    await this.$toast.error(data.message, {
                        duration: 1000
                    });
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
