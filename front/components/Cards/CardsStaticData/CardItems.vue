<template>
    <b-card :border-variant="cardBorder">
        <b-card-title>
            <b-row>
                <b-col cols="auto" class="mr-auto"></b-col>
                <b-col cols="auto"><b-form-checkbox v-model="editMode" name="check-button" switch /></b-col>
            </b-row>
        </b-card-title>
        <b-card-text>
            <h5 v-if="items.length === 0 && !editMode" class="text-muted text-center m-5" > No Data Available Yet </h5>
            <div v-else>
                <p class="text-right">
                    <small v-if="!flashCounter" class="text-muted">TOTAL: {{ items.length }}</small>
                    <small v-else>TOTAL: <span class="text-primary">{{ items.length }}</span></small>
                </p>


                <div v-if="editMode===false">
                    <b-table borderless :items="items" :fields="fields" hover>
                        <template v-slot:cell(unit_cost_price_net)="data">
                            {{ data.value }} {{ data.item.unit_cost_price_currency_code }}
                        </template>

                        <template v-slot:cell(weight_kg)="data">
                            {{ data.value }} kg
                        </template>

                    </b-table>
                </div>

                <div v-else>
                    <b-tabs content-class="mt-3">
                        <b-tab title="Create" active>
                            <lazy-form-add-seller-firm-item @flash="flashCount"/>

                        </b-tab>

                        <b-tab title="Delete" :disabled="items.length === 0">
                            <lazy-table-delete-seller-firm-item :fields="fieldsEditable" @flash="flashCount"/>
                        </b-tab>
                    </b-tabs>
                </div>
            </div>
        </b-card-text>
    </b-card>
</template>

<script>
    import { mapState } from "vuex";

    export default {
        name: "CardItems",

        data() {
            return {
                editMode: false,
                flashCounter: false,

                fields: [
                    { key: "brand_name", sortable: false },
                    { key: "sku", label:"SKU", sortable: false },
                    { key: "name", sortable: false },
                    { key: "tax_code_code", label:"Tax Code", sortable: false },
                    {
                        key: "weight_kg",
                        label: "Weight",
                        formatter: value => {
                            return Number.parseFloat(value).toFixed(3)
                        },
                        sortable: false
                    },
                    {
                        key: "unit_cost_price_net",
                        sortable: false,
                        formatter: value => {
                            return Number.parseFloat(value).toFixed(2)
                        },
                    }
                ]
            };
        },

        computed: {
            ...mapState({
                items: state => state.seller_firm.seller_firm.items,
                seller_firm: state => state.seller_firm.seller_firm,
            }),

            // countItems() {
            //     return this.$store.getters["seller_firm/countItems"];
            // },

            cardBorder() {
                return this.editMode ? "info" : "";
            },

            fieldsEditable() {
                return this.fields.concat({
                    key: "edit",
                    label: "",
                    sortable: false
                });
            }


        },

        methods: {
            flashCount() {
                this.flashCounter = true
                setTimeout(() => this.flashCounter = false, 1000)

            }


        }
    };
</script>
