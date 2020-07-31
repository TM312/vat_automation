<template>
    <b-card bg-variant="white" lg="6" xl="4">
        <b-form-group
            label-cols-lg="2"
            label="New Tax Record"
            label-size="lg"
            label-class="font-weight-bold pt-0"
            class="mb-2"
        >

            <!-- <b-form-group
                label-cols-sm="3"
                label-align-sm="right"
                label="Name"
                description="The name helps for better distinction of tax records."
            >
                <b-form-input
                    id="name"
                    v-model="payload.name"
                    required
                ></b-form-input>

            </b-form-group> -->


            <b-form-group
                label-cols-sm="3"
                label-align-sm="right"
                label="Tax Jurisdiction"
            >

                <b-form-select
                    id="tax_jurisdiction"
                    :options="optionsCountryCode"
                    v-model="payload.tax_jurisdiction"
                    required
                ></b-form-select>

            </b-form-group>

            <b-row class="my-2">
                <b-col offset-sm="3"><b-button @click="setQ(1)" variant="outline-primary" block>Q1</b-button></b-col>
                <b-col><b-button @click="setQ(2)" variant="outline-primary" block>Q2</b-button></b-col>
                <b-col><b-button @click="setQ(3)" variant="outline-primary" block>Q3</b-button></b-col>
                <b-col><b-button @click="setQ(4)" variant="outline-primary" block>Q4</b-button></b-col>
            </b-row>
            <b-row class="mb-2">
                <b-col offset-sm="3"><b-button @click="setPastYear()" variant="outline-primary" block>Past Year ({{ yearString }})</b-button></b-col>
            </b-row>

            <b-form-group
                label-cols-sm="3"
                label-align-sm="right"
                label-for="start_date"
                label="Validity"
                description="From"
            >
            <b-row>
                <b-col>
                    <b-form-datepicker
                        cols-sm="3"
                        id="start_date"
                        v-model="payload.start_date"
                        description="From"
                        required
                    ></b-form-datepicker>
                </b-col>
                <b-col>
                    <b-form-datepicker
                        cols-sm="3"
                        id="end_date"
                        v-model="payload.end_date"
                        :value="dateLastMonth"
                        description="To"
                        required
                    ></b-form-datepicker>

                </b-col>
            </b-row>
            </b-form-group>


        </b-form-group>


        <b-button
            variant="primary"
            @click="submitPayload()"
            block
        ><b-icon icon="box-arrow-in-up" /> Create New Tax Record</b-button>

        <hr><br><hr>
        date.getMonth: {{ new Date().getMonth() }}
        <br>
        Payload: {{ payload }}
        <br>

    </b-card>
</template>

<script>
    import { mapState } from "vuex";
    import { BIcon } from "bootstrap-vue";

    export default {
        name: 'FormAddSellerFirmTaxRecord',

        components: {
            BIcon
        },

        data() {
            return {
                payload: {
                    tax_jurisdiction: null,
                    start_date: null,
                    end_date: null
                }
            }
        },

        computed: {
            ...mapState({
                countries: state => state.country.countries
            }),

            dateLastMonth() {
                var date = new Date()
                var dateLastMonth = new Date(date.getFullYear(), date.getMonth(), 0 )
                return this.$dateFns.format(dateLastMonth, 'yyyy-MM-dd')
            },

            yearString() {
                var d = new Date();
                var pastYear = d.getFullYear() - 1;
                d.setFullYear(pastYear);
                return this.$dateFns.format(d, 'yyyy')
            },

            optionsCountryCode() {
                const countriesShort = this.countries.filter(country => (country.code !== undefined && country.code !== null))

                let options = countriesShort.map(country => {
                    let properties = {
                        value: country.code,
                        text: country.name
                    };
                    return properties;

                    })
                return options;
            }
        },

        methods: {

            // setFirstOfMonth() {
            //     var date = new Date()
            //     var dateLastMonth = new Date(date.getFullYear(), date.getMonth() + 1, 1)
            //     this.payload.start_date = this.$dateFns.format(dateLastMonth, 'yyyy-MM-dd')
            // },

            setPastYear() {
                this.payload.start_date = this.yearString + '-01-01'
                this.payload.end_date = this.yearString + '-12-31'
            },

            setQ(quarter) {
                var yearString = this.$dateFns.format(new Date(), 'yyyy')
                // https://en.wikipedia.org/wiki/Calendar_year
                // First quarter, Q1: 1 January – 31 March (90 days or 91 days in leap years)
                // Second quarter, Q2: 1 April – 30 June (91 days)
                // Third quarter, Q3: 1 July – 30 September (92 days)
                // Fourth quarter, Q4: 1 October – 31 December (92 days)

                switch (quarter) {
                    case 1:
                        this.payload.start_date = yearString + '-01-01'
                        this.payload.end_date = yearString + '-03-31'
                        break;
                    case 2:
                        this.payload.start_date = yearString + '-04-01'
                        this.payload.end_date = yearString + '-06-30'
                        break;
                    case 3:
                        this.payload.start_date = yearString + '-07-01'
                        this.payload.end_date = yearString + '-09-30'
                        break;
                    case 4:
                        this.payload.start_date = yearString + '-10-01'
                        this.payload.end_date = yearString + '-12-31'
                        break;
                }

            },


            // setToday() {
            //     this.payload.end_date = this.$dateFns.format(new Date(), 'yyyy-MM-dd')
            // },

            // setLastMonth() {
            //     this.payload.end_date = this.dateLastMonth
            // },

            reset() {
                this.payload = {
                    tax_jurisdiction: null,
                    start_date: null,
                    end_date: null
                }
            },

            async submitPayload() {
                try {
                    await this.create_by_seller_firm_public_id();

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
