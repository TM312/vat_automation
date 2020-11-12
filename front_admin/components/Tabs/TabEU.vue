<template>
    <div>
        <h1 class="mb-5">Here is all EU Data</h1>
        <h2>EU Validity: {{ eu.valid_from }} - {{ eu.valid_to }}</h2>
        <h3>today as ISO String: {{ new Date().toISOString().slice(0, 10) }}</h3>
        <h3>selected date: {{ date }}</h3>

        <div>
            <b-card bg-variant="white" lg="6" xl="4" style="max-width: 80rem">
                <b-form-group
                    label-align-sm="right"
                    label-for="date"
                    description="Date"
                >
                    <b-form-datepicker
                        id="date"
                        v-model="date"
                        cols-sm="3"
                        description="Date"
                        required
                    />
                </b-form-group>
                <b-button variant="primary" block @click="submitPayload()">
                    <b-icon icon="box-arrow-in-up" />
                    <!-- <span v-if="sellerFirm.transactions.length === 0">There are no processed transactions available for this seller firm</span> -->
                    <span>Get EU By Date</span>
                </b-button>
            </b-card>
        </div>

        <b-table :items="eu.countries" :fields="fields">
            <template #cell(currency_code)="data">
                {{ $store.getters["country/countryNameByCode"](data.value) }}
            </template>
        </b-table>
    </div>
</template>

<script>
    import { mapState } from "vuex";

    export default {
        name: "TabEU",

        async fetch() {
            const { store } = this.$nuxt.context;
            if (this.eu.length === 0) {
                // https://stackoverflow.com/questions/23593052/format-javascript-date-as-yyyy-mm-dd
                var todayDate = new Date().toISOString().slice(0, 10);
                await store.dispatch("country/get_eu_by_date", todayDate);
            }
        },

        data() {
            return {
                date: null,
                fields: [
                    { key: "name", label: "Name", sortable: false },
                    { key: "code", label: "Code", sortable: false },
                    { key: "vat_country_code", label: "Code VAT", sortable: false },
                    {
                        key: "currency_code",
                        label: "Currency",
                        sortable: false,
                    },
                ],
            };
        },

        computed: {
            ...mapState({
                eu: (state) => state.country.eu,
            }),
        },

        methods: {
            async submitPayload() {
                const { store } = this.$nuxt.context;
                await store.dispatch("country/get_eu_by_date", this.date);
            },
        }
    };
</script>
