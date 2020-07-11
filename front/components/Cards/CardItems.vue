<template>
    <b-card :border-variant="cardBorder">
        <template v-slot:header>
            <b-row>
                <b-col cols="auto" class="mr-auto">
                    <h6 class="mb-0">Items</h6>
                </b-col>
                <b-col cols="auto"><b-form-checkbox v-model="editMode" name="check-button" switch>Edit Mode</b-form-checkbox></b-col>
            </b-row>
        </template>
        <b-card-text>
            <h5 v-if="countItems === 0 && !editMode" class="text-muted text-center m-5" > No Data Available Yet </h5>
            <div v-else>
                <p class="text-right">
                    <small v-if="!flashCounter" class="text-muted">TOTAL: {{ countItems }}</small>
                    <small v-else>TOTAL: <span class="text-primary">{{ countItems }}</span></small>
                </p>


                <div v-if="editMode===false">
                    <b-table borderless :items="items" :fields="fields" hover></b-table>
                </div>

                <div v-else>
                    <b-tabs content-class="mt-3">
                        <b-tab title="Create" active>
                            <lazy-form-add-seller-firm-item @flash="flashCount"/>

                        </b-tab>

                        <b-tab title="Delete" :disabled="countItems === 0">
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
                    { key: "brand_name", sortable: true },
                    { key: "name", sortable: true },
                    { key: "sku", label:"SKU", sortable: true },
                    { key: "ean", label:"EAN", sortable: true },
                    { key: "asin", label:"ASIN", sortable: true },
                    { key: "tax_code_code", label:"Tax Code", sortable: true },
                    { key: "weight_kg", sortable: true },
                    { key: "unit_cost_price_net", sortable: true },
                    { key: "unit_cost_price_currency_code", label: "Unit Cost Price Currency", sortable: true },
                    { key: "valid_from", sortable: true },
                    { key: "valid_to", sortable: true },
                    { key: "created_on", sortable: true },
                    { key: "created_by", sortable: true }
                ]
            };
        },

        computed: {
            ...mapState({
                items: state => state.seller_firm.seller_firm.items,
            }),

            countItems() {
                return this.$store.getters["seller_firm/countItems"];
            },

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
