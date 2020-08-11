<template>
    <b-card bg-variant="white">
        <b-form-group
            label-cols-lg="3"
            label="New Client"
            label-size="lg"
            label-class="font-weight-bold pt-0"
            class="mb-2"
        >

            <b-form-group
                label-cols-sm="3"
                label-align-sm="right"
                label-for="companyName"
                label="Company Name"
                >
                    <b-form-input
                        id="companyName"
                        v-model="payload.name"
                        type="text"
                        class="mt-1"
                        required
                    />
            </b-form-group>

            <b-form-group
                label-cols-sm="3"
                label-align-sm="right"
                label-for="companyAddress"
                label="Company Address"
                >
                    <b-form-input
                        id="companyAddress"
                        v-model="payload.address"
                        type="text"
                        class="mt-1"
                    />
            </b-form-group>

            <b-form-group
                label-cols-sm="3"
                label-align-sm="right"
                label-for="establishment_country_code"
                label="Establishment Country"
            >
                <!-- <b-form-select v-if="$fetchState.pending" id="establishment_country_code_placeholder" disabled /> -->
                <b-form-select
                    id="establishment_country_code"
                    :options="optionsCountryCode"
                    v-model="payload.establishment_country_code"
                ></b-form-select>
            </b-form-group>

        </b-form-group>


        <b-button
                variant="primary"
                @click="submitPayload()"
                :disabled="validation_submit"
                block
            >
                <b-icon icon="box-arrow-in-up" /> Add New Client
        </b-button>
    </b-card>
</template>

<script>
    import { mapState } from "vuex";

    export default {
        name: 'FormAddSellerFirm',

        data() {
            return {
                payload: {
                    name: null,
                    address: null,
                    establishment_country_code: null
                }
            }
        },

        computed: {
            ...mapState({
                countries: state => state.country.countries
            }),

            optionsCountryCode() {
                let options = this.countries.map(country => {
                    let properties = {
                        value: country.code,
                        text: country.name
                    };
                    return properties;
                });
                return options;
            },

            validation_submit() {
                if (
                    this.payload.establishment_country_code !== null &&
                    this.payload.establishment_country_code !== null
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
                    await this.create_as_client();

                    this.payload.establishment_country_code = null;


                    this.$emit('flash')
                    await this.$toast.success('New client succesfully added.', {
                        duration: 5000
                    });
                } catch (error) {
                    this.$toast.error(error, { duration: 5000 });
                }
            },

            async create_as_client() {
                await this.$store.dispatch(
                    "seller_firm/create_as_client",
                     this.payload
                );
            },
        }
    }
</script>

<style>

</style>
