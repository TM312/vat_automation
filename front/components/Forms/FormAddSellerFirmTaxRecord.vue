<template>
    <b-container>
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
                        id="tax_jurisdiction_code"
                        :options="optionsCountryCode"
                        v-model="payload.tax_jurisdiction_code"
                        required
                    ></b-form-select>

                </b-form-group>


                <b-form-group
                    label-cols-sm="3"
                    label-align-sm="right"
                    label="Validity"
                >
                    <b-row class="my-2">
                        <b-col><b-button @click="setQ(1)" :disabled="test(1)" :variant="test(1) ? 'outline-secondary' : 'outline-primary'" :pressed="selected == 'Q1'" block>Q1</b-button></b-col>
                        <b-col><b-button @click="setQ(2)" :disabled="test(2)" :variant="test(2) ? 'outline-secondary' : 'outline-primary'" :pressed="selected == 'Q2'" block>Q2</b-button></b-col>
                        <b-col><b-button @click="setQ(3)" :disabled="test(3)" :variant="test(3) ? 'outline-secondary' : 'outline-primary'" :pressed="selected == 'Q3'" block>Q3</b-button></b-col>
                        <b-col><b-button @click="setQ(4)" :disabled="test(4)" :variant="test(4) ? 'outline-secondary' : 'outline-primary'" :pressed="selected == 'Q4'" block>Q4</b-button></b-col>
                    </b-row>
                    <b-row class="mb-2">
                        <b-col><b-button @click="setPastYear()" variant="outline-primary" :pressed="selected == 'pastYear'" block>{{ pastYearString }}</b-button></b-col>
                        <b-col><b-button @click="setPastMonth()" variant="outline-primary" :pressed="selected == 'pastMonth'" block>{{ $dateFns.format(pastMonthDate, 'MMMM yyyy') }}</b-button></b-col>
                    </b-row>
                    <b-row>
                        <b-col>
                            <b-form-group
                                label-align-sm="right"
                                label-for="start_date"
                                description="From"
                            >

                                <b-form-datepicker
                                    cols-sm="3"
                                    id="start_date"
                                    v-model="payload.start_date"
                                    :value="dateStringEndLastMonth"
                                    description="From"
                                    required
                                ></b-form-datepicker>
                            </b-form-group>
                        </b-col>
                        <b-col>
                            <b-form-group
                                label-align-sm="right"
                                label-for="end_date"
                                description="To"
                            >
                                <b-form-datepicker
                                    cols-sm="3"
                                    id="end_date"
                                    v-model="payload.end_date"
                                    :value="dateStringBeginningLastMonth"
                                    required
                                ></b-form-datepicker>
                            </b-form-group>

                        </b-col>
                    </b-row>
                </b-form-group>
            </b-form-group>


            <b-button
                variant="primary"
                @click="submitPayload()"
                block
            ><b-icon icon="box-arrow-in-up" /> Create New Tax Record</b-button>

        </b-card>
    </b-container>
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
                    tax_jurisdiction_code: null,
                    start_date: null,
                    end_date: null
                }
            }
        },

        computed: {
            ...mapState({
                countries: state => state.country.countries
            }),

            dateStringEndLastMonth() {
                var d = new Date()
                var dateEndLastMonth = new Date(d.getFullYear(), d.getMonth(), 0 )
                return this.$dateFns.format(dateEndLastMonth, 'yyyy-MM-dd')
            },

            dateStringBeginningLastMonth() {
                var d = new Date()
                var dateBeginningLastMonth = new Date(d.getFullYear(), d.getMonth(), 1 )
                return this.$dateFns.format(dateBeginningLastMonth, 'yyyy-MM-dd')
            },

            pastYearString() {
                var d = new Date()
                var pastYear = d.setFullYear(d.getFullYear() - 1);
                return this.$dateFns.format(pastYear, 'yyyy')
            },

            currentYearString() {
                return this.$dateFns.format(new Date(), 'yyyy')
            },

            pastMonthDate() {
                var d = new Date()
                return d.setMonth(d.getMonth() - 1);
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
            },

            selected() {
                var selected = null
                var pastMonthString = this.$dateFns.format(this.pastMonthDate, 'yyyy-MM')

                if (
                    this.payload.start_date == this.currentYearString + '-01-01' &&
                    this.payload.end_date == this.currentYearString + '-03-31'
                    ) {
                        selected = 'Q1'
                } else if (
                    this.payload.start_date == this.currentYearString + '-04-01' &&
                    this.payload.end_date == this.currentYearString + '-06-30'
                    ) {
                        selected = 'Q2'
                } else if (
                        this.payload.start_date == this.currentYearString + '-07-01' &&
                        this.payload.end_date == this.currentYearString + '-09-30'
                    ) {
                        selected = 'Q3'
                } else if (
                        this.payload.start_date == this.currentYearString + '-10-01' &&
                        this.payload.end_date == this.currentYearString + '-12-31'
                    ) {
                        selected = 'Q4'
                } else if(
                    this.payload.start_date == this.pastYearString + '-01-01' &&
                    this.payload.end_date == this.pastYearString + '-12-31'
                ) {
                    selected = 'pastYear'

                } else if (
                    this.payload.start_date == pastMonthString + '-01' &&
                    this.payload.end_date == pastMonthString + '-31'
                ) {
                    selected = 'pastMonth'
                }

                return selected

            },
        },

        methods: {

            test(quarter) {
                if (quarter === 1) {
                    return new Date() < new Date(this.currentYearString, 2, 31)
                } else if (quarter === 2) {
                    return new Date() < new Date(this.currentYearString, 5, 30)
                } else if (quarter === 3) {
                    return new Date() < new Date(this.currentYearString, 8, 30)
                } else if (quarter === 4) {
                    return new Date() < new Date(this.currentYearString, 11, 31)
                }

            },

            setPastYear() {
                this.payload.start_date = this.pastYearString + '-01-01'
                this.payload.end_date = this.pastYearString + '-12-31'
            },

            setPastMonth() {
                var pastMonthString = this.$dateFns.format(this.pastMonthDate, 'yyyy-MM')

                this.payload.start_date = pastMonthString + '-01'
                this.payload.end_date = pastMonthString + '-31'
            },

            setQ(quarter) {
                // https://en.wikipedia.org/wiki/Calendar_year
                // First quarter, Q1: 1 January – 31 March (90 days or 91 days in leap years)
                // Second quarter, Q2: 1 April – 30 June (91 days)
                // Third quarter, Q3: 1 July – 30 September (92 days)
                // Fourth quarter, Q4: 1 October – 31 December (92 days)

                switch (quarter) {
                    case 1:
                        this.payload.start_date = this.currentYearString + '-01-01'
                        this.payload.end_date = this.currentYearString + '-03-31'
                        break;
                    case 2:
                        this.payload.start_date = this.currentYearString + '-04-01'
                        this.payload.end_date = this.currentYearString + '-06-30'
                        break;
                    case 3:
                        this.payload.start_date = this.currentYearString + '-07-01'
                        this.payload.end_date = this.currentYearString + '-09-30'
                        break;
                    case 4:
                        this.payload.start_date = this.currentYearString + '-10-01'
                        this.payload.end_date = this.currentYearString + '-12-31'
                        break;
                }

            },

            reset() {
                this.payload = {
                    tax_jurisdiction_code: null,
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
                    await this.$toast.success('New tax record succesfully added.', {
                        duration: 5000
                    });
                } catch (error) {
                    this.$toast.error(error, { duration: 5000 });
                }
            },

            async create_by_seller_firm_public_id() {
                const data_array = [this.$route.params.public_id, this.payload]

                await this.$store.dispatch(
                    "tax_record/create_by_seller_firm_public_id",
                    data_array
                );
            },
        }
    }
</script>

<style>

</style>
