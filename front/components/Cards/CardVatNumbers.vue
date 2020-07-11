<template>
    <b-card :border-variant="cardBorder">
        <template v-slot:header>
            <b-row>
                <b-col cols="auto" class="mr-auto">
                    <h6 class="mb-0">Vat Numbers</h6>
                </b-col>
                <b-col cols="auto">
                    <b-form-checkbox v-model="editMode" @click="evaluateRefresh" name="check-button" switch>Edit Mode</b-form-checkbox>
                </b-col>
            </b-row>
        </template>
        <b-card-text>
            <h5 v-if="countVatNumbers === 0 && !editMode" class="text-muted text-center m-5" > No Data Available Yet </h5>
            <div v-else>
                <p class="text-right">
                    <small v-if="!flashCounter" class="text-muted">TOTAL: {{ countVatNumbers }}</small>
                    <small v-else>TOTAL: <span class="text-primary">{{ countVatNumbers }}</span></small>
                </p>


                <div v-if="editMode===false">
                    <b-table borderless :items="vatNumbers" :fields="fields" hover>
                        <template v-slot:cell(vatin)="data">
                            {{ data.item.country_code }} - {{ data.item.number }}
                        </template>

                    </b-table>
                </div>

                <div v-else>
                    <b-tabs content-class="mt-3">
                        <b-tab title="Create" active>
                            <lazy-form-add-seller-firm-vat-number @flash="flashCount"/>

                        </b-tab>

                        <b-tab title="Delete" :disabled="countVatNumbers === 0">
                            <lazy-table-delete-seller-firm-vat-number :fields="fieldsEditable" @flash="flashCount"/>
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
        name: "CardVatNumbers",
        // eslint-disable-next-line

        data() {
            return {
                editMode: false,
                flashCounter: false,

                fields: [
                    { key: "vatin", label: "VATIN", sortable: false },
                    { key: "valid", sortable: false },
                    { key: "last_validated", sortable: true },
                    { key: "valid_from", sortable: true },
                    { key: "valid_to", sortable: true },
                    { key: "initial_tax_date", sortable: true },
                ]
            };
        },

        computed: {
            ...mapState({
                vatNumbers: state => state.seller_firm.seller_firm.vat_numbers,
            }),

            countVatNumbers() {
                return this.$store.getters["seller_firm/countVatNumbers"];
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

            },

            async evaluateRefresh() {
                if (this.editMode === true) {
                    await this.$store.dispatch(
                        "seller_firm/get_by_public_id",
                        this.$route.params.public_id
                    );
                }
            }


        }
    };
</script>
