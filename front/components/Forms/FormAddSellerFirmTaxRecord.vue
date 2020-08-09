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
                    <b-row class="mt-2" cols="1" cols-md="3" cols-lg="4" cols-xl="6">
                        <b-col class="mb-2"><b-button @click="setM(0)" :disabled="test(0)" :variant="test(0) ? 'outline-secondary' : 'outline-primary'" :pressed="selected == 'Jan'" block>Jan</b-button></b-col>
                        <b-col class="mb-2"><b-button @click="setM(1)" :disabled="test(1)" :variant="test(1) ? 'outline-secondary' : 'outline-primary'" :pressed="selected == 'Feb'" block>Feb</b-button></b-col>
                        <b-col class="mb-2"><b-button @click="setM(2)" :disabled="test(2)" :variant="test(2) ? 'outline-secondary' : 'outline-primary'" :pressed="selected == 'March'" block>March</b-button></b-col>
                        <b-col class="mb-2"><b-button @click="setM(3)" :disabled="test(3)" :variant="test(3) ? 'outline-secondary' : 'outline-primary'" :pressed="selected == 'April'" block>April</b-button></b-col>
                        <b-col class="mb-2"><b-button @click="setM(4)" :disabled="test(4)" :variant="test(4) ? 'outline-secondary' : 'outline-primary'" :pressed="selected == 'May'" block>May</b-button></b-col>
                        <b-col class="mb-2"><b-button @click="setM(5)" :disabled="test(5)" :variant="test(5) ? 'outline-secondary' : 'outline-primary'" :pressed="selected == 'June'" block>June</b-button></b-col>

                        <b-col class="mb-2"><b-button @click="setM(6)" :disabled="test(6)" :variant="test(6) ? 'outline-secondary' : 'outline-primary'" :pressed="selected == 'July'" block>July</b-button></b-col>
                        <b-col class="mb-2"><b-button @click="setM(7)" :disabled="test(7)" :variant="test(7) ? 'outline-secondary' : 'outline-primary'" :pressed="selected == 'Aug'" block>Aug</b-button></b-col>
                        <b-col class="mb-2"><b-button @click="setM(8)" :disabled="test(8)" :variant="test(8) ? 'outline-secondary' : 'outline-primary'" :pressed="selected == 'Sep'" block>Sep</b-button></b-col>
                        <b-col class="mb-2"><b-button @click="setM(9)" :disabled="test(9)" :variant="test(9) ? 'outline-secondary' : 'outline-primary'" :pressed="selected == 'Oct'" block>Oct</b-button></b-col>
                        <b-col class="mb-2"><b-button @click="setM(10)" :disabled="test(10)" :variant="test(10) ? 'outline-secondary' : 'outline-primary'" :pressed="selected == 'Nov'" block>Nov</b-button></b-col>
                        <b-col class="mb-2"><b-button @click="setM(11)" :disabled="test(11)" :variant="test(11) ? 'outline-secondary' : 'outline-primary'" :pressed="selected == 'Dec'" block>Dec</b-button></b-col>
                    </b-row>
                    <b-row cols="1" cols-md="2" cols-lg="4">
                        <b-col class="mb-2"><b-button @click="setQ(1)" :disabled="test('Q1')" :variant="test('Q1') ? 'outline-secondary' : 'outline-primary'" :pressed="selected == 'Q1'" block>Q1</b-button></b-col>
                        <b-col class="mb-2"><b-button @click="setQ(2)" :disabled="test('Q2')" :variant="test('Q2') ? 'outline-secondary' : 'outline-primary'" :pressed="selected == 'Q2'" block>Q2</b-button></b-col>
                        <b-col class="mb-2"><b-button @click="setQ(3)" :disabled="test('Q3')" :variant="test('Q3') ? 'outline-secondary' : 'outline-primary'" :pressed="selected == 'Q3'" block>Q3</b-button></b-col>
                        <b-col class="mb-2"><b-button @click="setQ(4)" :disabled="test('Q4')" :variant="test('Q4') ? 'outline-secondary' : 'outline-primary'" :pressed="selected == 'Q4'" block>Q4</b-button></b-col>
                    </b-row>
                    <b-row class="mb-2">
                        <b-col><b-button @click="setPastYear()" variant="outline-primary" :pressed="selected == 'pastYear'" block>{{ pastYearString }}</b-button></b-col>
                        <!-- <b-col><b-button @click="setPastMonth()" variant="outline-primary" :pressed="selected == 'pastMonth'" block>{{ $dateFns.format(pastMonthDate, 'MMMM yyyy') }}</b-button></b-col> -->
                    </b-row>
                    <b-row class="mt-4" cols="1" cols-lg="2">
                        <b-col class="mb-2">
                            <b-form-group
                                label-align-sm="right"
                                label-for="start_date"
                                description="From"
                            >

                                <b-form-datepicker
                                    cols-sm="3"
                                    id="start_date"
                                    v-model="payload.start_date"
                                    description="From"
                                    required
                                ></b-form-datepicker>
                            </b-form-group>
                        </b-col>
                        <b-col class="mb-2">
                            <b-form-group
                                label-align-sm="right"
                                label-for="end_date"
                                description="To"
                            >
                                <b-form-datepicker
                                    cols-sm="3"
                                    id="end_date"
                                    v-model="payload.end_date"
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
                :disabled="sellerFirm.transactions.length === 0"
            ><b-icon icon="box-arrow-in-up" />
            <span v-if="sellerFirm.transactions.length === 0">There are no processed transactions available for this seller firm</span>
            <span v-else>Generate New Tax Record</span>
            </b-button>

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
                countries: state => state.country.countries,
                sellerFirm: state => state.seller_firm.seller_firm,
            }),



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
                    this.payload.start_date == this.currentYearString + '-01-01' &&
                    this.payload.end_date == this.currentYearString + '-01-31'
                    ) {
                        selected = 'Jan'
                } else if (
                    this.payload.start_date == this.currentYearString + '-02-01' &&
                    this.payload.end_date == this.currentYearString + ('-02-28' || '-02-29')
                    ) {
                        selected = 'Feb'
                } else if (
                    this.payload.start_date == this.currentYearString + '-03-01' &&
                    this.payload.end_date == this.currentYearString + '-03-31'
                    ) {
                        selected = 'March'
                } else if (
                    this.payload.start_date == this.currentYearString + '-04-01' &&
                    this.payload.end_date == this.currentYearString + '-04-30'
                    ) {
                        selected = 'April'
                } else if (
                    this.payload.start_date == this.currentYearString + '-05-01' &&
                    this.payload.end_date == this.currentYearString + '-05-31'
                    ) {
                        selected = 'May'
                } else if (
                    this.payload.start_date == this.currentYearString + '-06-01' &&
                    this.payload.end_date == this.currentYearString + '-06-30'
                    ) {
                        selected = 'June'
                } else if (
                    this.payload.start_date == this.currentYearString + '-07-01' &&
                    this.payload.end_date == this.currentYearString + '-07-31'
                    ) {
                        selected = 'July'
                } else if (
                    this.payload.start_date == this.currentYearString + '-08-01' &&
                    this.payload.end_date == this.currentYearString + '-08-31'
                    ) {
                        selected = 'Aug'
                } else if (
                    this.payload.start_date == this.currentYearString + '-09-01' &&
                    this.payload.end_date == this.currentYearString + '-09-30'
                    ) {
                        selected = 'Sep'
                } else if (
                    this.payload.start_date == this.currentYearString + '-10-01' &&
                    this.payload.end_date == this.currentYearString + '-10-31'
                    ) {
                        selected = 'Oct'
                } else if (
                    this.payload.start_date == this.currentYearString + '-11-01' &&
                    this.payload.end_date == this.currentYearString + '-11-30'
                    ) {
                        selected = 'Nov'
                } else if (
                    this.payload.start_date == this.currentYearString + '-12-01' &&
                    this.payload.end_date == this.currentYearString + '-12-31'
                    ) {
                        selected = 'Dec'
                }

                return selected

            },
        },

        methods: {

            test(timespan) {
                if (typeof(timespan) === 'string') {
                    if (timespan === 'Q1') {
                        return new Date() < new Date(this.currentYearString, 2, 31)
                    } else if (timespan === 'Q2') {
                        return new Date() < new Date(this.currentYearString, 5, 30)
                    } else if (timespan === 'Q3') {
                        return new Date() < new Date(this.currentYearString, 8, 30)
                    } else if (timespan === 'Q4') {
                        return new Date() < new Date(this.currentYearString, 11, 31)
                    }
                } else if (typeof(timespan) === 'number') {
                    return new Date() < new Date(this.currentYearString, timespan, 0)
                }

            },

            setPastYear() {
                this.payload.start_date = this.pastYearString + '-01-01'
                this.payload.end_date = this.pastYearString + '-12-31'
            },

            // setPastMonth() {
            //     var pastMonthString = this.$dateFns.format(this.pastMonthDate, 'yyyy-MM')

            //     this.payload.start_date = pastMonthString + '-01'
            //     this.payload.end_date = pastMonthString + '-31'
            // },

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

            dateStringEndMonth(month) {
                var d = new Date()
                var dateEndMonth = new Date(d.getFullYear(), month+1, 0 )
                return this.$dateFns.format(dateEndMonth, 'yyyy-MM-dd')
            },

            dateStringBeginningMonth(month) {
                var d = new Date()
                var dateBeginningMonth = new Date(d.getFullYear(), month, 1 )
                return this.$dateFns.format(dateBeginningMonth, 'yyyy-MM-dd')
            },

            setM(month) {
                this.payload.start_date = this.dateStringBeginningMonth(month)
                this.payload.end_date = this.dateStringEndMonth(month)
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
