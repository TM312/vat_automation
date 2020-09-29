<template>
    <b-card :border-variant="cardBorder">
        <b-card-title>
            <b-row>
                <b-col cols="auto" class="mr-auto">Distance Sales</b-col>
                <b-col cols="auto">
                    <b-form-checkbox v-model="editMode" name="check-button" switch />
                </b-col>
            </b-row>

        </b-card-title>


        <b-card-text>
            <h5 v-if="distanceSales.length === 0 && !editMode" class="text-muted text-center m-5" > No Data Available Yet </h5>
            <div v-else>
                <p class="text-right">
                    <small v-if="!flashCounter" class="text-muted">TOTAL: {{ distanceSales.length }}</small>
                    <small v-else>TOTAL: <span class="text-primary">{{ distanceSales.length }}</span></small>
                </p>


                <div v-if="editMode===false">
                    <b-table borderless :items="distanceSales" :fields="fields" :busy="!distanceSales" hover>
                        <template v-slot:table-busy>
                            <div class="text-center text-secondary my-2">
                                <b-spinner class="align-middle"></b-spinner>
                                <strong>Loading...</strong>
                            </div>
                        </template>

                        <template v-slot:cell(active)="data">
                            <b-icon v-if="data.value === true" icon="check-circle" variant="success"></b-icon>
                            <b-icon v-else icon="x-circle" variant="danger"></b-icon>
                        </template>


                    </b-table>
                </div>

                <div v-else>
                    <b-tabs content-class="mt-3">
                        <b-tab title="Create" active>
                            <lazy-form-add-seller-firm-distance-sale @flash="flashCount"/>

                        </b-tab>

                        <b-tab title="Delete" :disabled="distanceSales.length === 0">
                            <lazy-table-delete-seller-firm-distance-sale :fields="fieldsEditable" @flash="flashCount"/>
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
        name: "CardDistanceSales",
        // eslint-disable-next-line

        data() {
            return {
                editMode: false,
                flashCounter: false,

                fields: [
                    { key: "arrival_country", sortable: true },
                    { key: "active", sortable: true }
                ]
            };
        },

        computed: {
            ...mapState({
                distanceSales: state => state.seller_firm.seller_firm.distance_sales,
            }),

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
