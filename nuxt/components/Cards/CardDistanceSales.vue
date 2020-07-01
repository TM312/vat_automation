<template>
    <b-card :border-variant="cardBg" :header-bg-variant="cardBg">
        <template v-slot:header>
            <b-row>
                <b-col cols="auto" class="mr-auto"><h6 class="mb-0">Distance Sales</h6></b-col>
                <b-col cols="auto">
                    <b-form-checkbox v-model="checked" name="check-button" switch>Edit Mode</b-form-checkbox>
                </b-col>
            </b-row>

        </template>
        <b-card-text >
            <h3 v-if="countDistanceSales === 0" class="text-secondary text-center">An Overview of This Company's Distance Sales Can Be Seen Here Once The Corresponding Data Has Been Uploaded</h3>
            <b-table v-else-if="!checked" borderless :items="distanceSales" :fields="fields" />
            <editable-table-delete v-else :fields="fields" :items="distanceSales" />
        </b-card-text>
    </b-card>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        name: 'CardDistanceSales',
        // eslint-disable-next-line
        props: {
            distanceSales: {
                type: [Array, Object],
                required: true
            }
        },

        data() {
            return {
                checked: false,

                fields: [
                    {
                        key: 'platform',
                        sortable: false
                    },
                    {
                        key: 'arrival_country',
                        sortable: true
                    },
                    {
                        key: 'valid_from',
                        sortable: true
                    },
                    {
                        key: 'valid_to',
                        sortable: true
                    },
                    {
                        key: 'active',
                        sortable: true
                    },
                    {
                        key: 'created_on',
                        sortable: true
                    },
                    {
                        key: 'created_by',
                        sortable: true
                    }
                ],

            }
        },

        computed: {
            ...mapState({
                countDistanceSales() {
                    return this.$store.getters['seller_firm/countDistanceSales']
                },
                cardBg() {
                    return this.checked ? 'info' : 'light'
                }


            }),
        },


    }
</script>
