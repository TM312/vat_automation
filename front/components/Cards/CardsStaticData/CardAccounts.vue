<template>
    <b-card :border-variant="cardBorder">
        <template v-slot:header>
            <b-row>
                <b-col cols="auto" class="mr-auto">
                    <h6 class="mb-0">Accounts</h6>
                </b-col>
                <b-col cols="auto">
                    <b-form-checkbox v-model="editMode" name="check-button" switch>Edit Mode</b-form-checkbox>
                </b-col>
            </b-row>
        </template>
        <b-card-text>
            <h5 v-if="seller_firm.len_accounts === 0 && !editMode" class="text-muted text-center m-5" > No Data Available Yet </h5>
            <div v-else>
                <p class="text-right">
                    <small v-if="!flashCounter" class="text-muted">TOTAL: {{ seller_firm.len_accounts }}</small>
                    <small v-else>TOTAL: <span class="text-primary">{{ seller_firm.len_accounts }}</span></small>
                </p>


                <div v-if="editMode===false">
                    <b-table borderless :items="accounts" :fields="fields" hover></b-table>
                </div>

                <div v-else>
                    <b-tabs content-class="mt-3">
                        <b-tab title="Create" active>
                            <lazy-form-add-seller-firm-account @flash="flashCount"/>

                        </b-tab>

                        <b-tab title="Delete" :disabled="seller_firm.len_accounts === 0">
                            <lazy-table-delete-seller-firm-account :fields="fieldsEditable" @flash="flashCount"/>
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
        name: "CardAccounts",
        // eslint-disable-next-line

        data() {
            return {
                editMode: false,
                flashCounter: false,

                fields: [
                    { key: 'channel_code', sortable: true },
                    { key: 'given_id', label: "Platform ID", sortable: false }
                ],
            };
        },

        computed: {
            ...mapState({
                accounts: state => state.seller_firm.seller_firm.accounts,
                seller_firm: state => state.seller_firm.seller_firm,
            }),

            // countAccounts() {
            //         return this.$store.getters['seller_firm/countAccounts']
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
