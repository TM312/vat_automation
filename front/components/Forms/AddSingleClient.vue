<template>
    <b-card>
        <b-card-title class="text-center">Single Client</b-card-title>
        <b-card-body>
            <b-form @submit.prevent="add_client_data">
                <b-form-group id="input-group-given-id" label="Given ID" label-for="input-given-id">
                    <b-form-input
                        id="input-given-id"
                        v-model="form.given_id"
                        type="text"
                        placeholder="The ID you have assigned internally to this client."
                    />
                </b-form-group>
                <b-form-group
                    id="input-group-company-name"
                    label="Company Name"
                    label-for="input-company-name"
                >
                    <b-form-input
                        id="input-company-name"
                        v-model="form.company_name"
                        type="text"
                        required
                    />
                </b-form-group>
                <b-form-group id="input-group-address" label="Address" label-for="input-address">
                    <b-form-input id="input-address" v-model="form.address" type="text" required />
                </b-form-group>
                <b-form-group
                    id="input-group-establishment-country-code"
                    label="Establishment Country"
                    label-for="input-establishment-country-code"
                >
                    <b-form-input
                        id="input-establishment-country-code"
                        v-model="form.establishment_country_code"
                        type="text"
                        placeholder="e.g. NL, DE, ES"
                        required
                    />
                </b-form-group>

                <b-button block variant="primary" class="mt-5" type="submit" disabled>Add</b-button>
            </b-form>
        </b-card-body>
    </b-card>
</template>

<script>
    export default {
        data() {
            return {
                form: {
                    given_id: "",
                    company_name: "",
                    address: "",
                    establishment_country_code: ""
                }
            };
        },
        methods: {
            async add_client_data() {
                const payload = {
                    given_id: this.form.given_id,
                    company_name: this.form.company_name,
                    address: this.form.address,
                    establishment_country_code: this.form.establishment_country_code
                };
                await this.$axios
                    .post("/seller_firm", payload)

                    .then(response => {
                        let response_objects = response.data;
                        response_objects.map(data => {
                            if (data.status == "success") {
                                this.$toast.success(data.message, {
                                    duration: 5000
                                });
                                this.form.given_id = "";
                                this.form.company_name = "";
                                this.form.company_name = "";
                                this.form.establishment_country_code = "";
                            } else {
                                this.$toast.error(data.message, { duration: 5000 });
                            }
                        });
                    })

                    .catch(err => {
                        console.log(err);
                        this.$toast.error(
                            "An error occured. Please make sure you have tried to submit valid data.",
                            { duration: 5000 }
                        );
                        this.progressBarStyle = "danger";
                    });
                // console.log(err))
                // this.$toast.error(err.message, {duration: 5000,}))
            }
        }
    };
</script>
