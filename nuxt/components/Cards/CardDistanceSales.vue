<template>
    <b-card :border-variant="cardBg" :header-bg-variant="cardBg">
        <template v-slot:header>
            <b-row>
                <b-col cols="auto" class="mr-auto"><h6 class="mb-0">Distance Sales</h6></b-col>
                <b-col cols="auto" v-if="countDistanceSales !== 0">
                    <b-form-checkbox
                        v-model="editMode"
                        name="check-button"
                        switch
                        >Edit Mode</b-form-checkbox>
                </b-col>
            </b-row>

        </template>
        <b-card-text>
            <h5 v-if="countDistanceSales === 0"
                class="text-secondary text-center m-5"
                >An Overview of This Company's Distance Sales Can Be Seen Here Once The Corresponding Data Has Been Uploaded</h5>

            <div v-else>
                <b-table v-show="!editMode" borderless :items="distanceSales" :fields="fields" />
                <div v-show="editMode">
                    <!-- <h1>Selected:
                        <span v-if="selected != [[]]">{{ selected }}</span>
                        <span v-else>"Default Selected"</span>
                        after selected
                    </h1> -->
                    <!-- <button-remove-entry :publicId="selected"/> -->
                    <editable-table-delete :fields="fields" :items="distanceSales" @objectSelected="selected=$event"/>
                </div>


            </div>


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
                editMode: false,

                selected: [[]],

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
                    return this.editMode ? 'info' : ''
                }


            }),
        },


    }
</script>
