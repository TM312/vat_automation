<template>
    <b-tabs content-class="mt-3">
        <b-tab title="Company Data" active>
            <b-card-group deck>
                <b-card class="mb-5" header="Base Data" title="">
                    <b-card-text>
                        <b>Public ID:</b> <br>
                        <b>Address:</b> <br>
                        <b>Establishment Country:</b> <br>
                        <br>
                        <b>Created On:</b> <br>
                        <b>Created By:</b> <br>
                    </b-card-text>
                </b-card>

                <b-card class="mb-5" >
                    <template v-slot:header>
                        <b-row>
                            <b-col cols="auto" class="mr-auto"><h6 class="mb-0">Accounts</h6></b-col>
                            <b-col cols="auto"><b-form-checkbox name="check-button" switch>Edit Mode</b-form-checkbox></b-col>
                        </b-row>
                    </template>
                    <b-card-text>
                        <div >
                            <p class="text-right"><small class="text-muted">TOTAL: </small><b-spinner variant="primary" small label="Spinning" /></p>
                            <div><b-table borderless busy :fields="fieldsAccounts"></b-table></div>
                        </div>
                    </b-card-text>
                </b-card>

            </b-card-group>
            <b-card-group deck>
                <b-card class="mb-5" >
                    <template v-slot:header>
                        <b-row>
                            <b-col cols="auto" class="mr-auto"><h6 class="mb-0">Vat Numbers</h6></b-col>
                            <b-col cols="auto"><b-form-checkbox name="check-button" switch>Edit Mode</b-form-checkbox></b-col>
                        </b-row>
                    </template>
                    <b-card-text>
                        <div >
                            <p class="text-right"><small class="text-muted">TOTAL: </small><b-spinner variant="primary" small label="Spinning" /></p>
                            <div><b-table borderless busy :fields="fieldsVatNumbers"></b-table></div>
                        </div>
                    </b-card-text>
                </b-card>



                <b-card class="mb-5" >
                    <template v-slot:header>
                        <b-row>
                            <b-col cols="auto" class="mr-auto"><h6 class="mb-0">Distance Sales</h6></b-col>
                            <b-col cols="auto"><b-form-checkbox name="check-button" switch>Edit Mode</b-form-checkbox></b-col>
                        </b-row>
                    </template>
                    <b-card-text>
                        <div >
                            <p class="text-right"><small class="text-muted">TOTAL: </small><b-spinner variant="primary" small label="Spinning" /></p>
                            <div><b-table borderless busy :fields="fieldsDistanceSales"></b-table></div>
                        </div>
                    </b-card-text>
                </b-card>
            </b-card-group>
        </b-tab>
        <b-tab title="Items" disabled>
        </b-tab>
    </b-tabs>
</template>

<script>
    export default {
        name:'OverviewBaseDataLoading',
        data() {
            return {
                fieldsVatNumbers: [
                    { key: "vatin", label: "VATIN", sortable: false },
                    { key: "valid_from", sortable: true },
                    { key: "valid_to", sortable: true }
                ],

                fieldsAccounts: [
                    { key: 'channel_code', sortable: true },
                    { key: 'given_id', label: "Platform ID", sortable: false },
                    { key: 'created_on', sortable: true },
                    { key: 'created_by', sortable: true }
                ],

                fieldsDistanceSales: [
                    { key: "platform", sortable: false },
                    { key: "arrival_country", sortable: true },
                    { key: "valid_from", sortable: true },
                    { key: "valid_to", sortable: true },
                    { key: "active", sortable: true },
                    { key: "created_on", sortable: true },
                    { key: "created_by", sortable: true }
                ]
            }
        },
    }
</script>

<style>
</style>
