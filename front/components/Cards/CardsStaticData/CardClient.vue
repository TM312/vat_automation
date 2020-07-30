<template>
    <b-card header="Base Data">
        <b-card-title>
            <b-row>
                <b-col cols="auto" class="mr-auto mb-1"><span>{{ seller_firm.name }}</span></b-col>
                <b-col cols="auto"><button-follow-seller-firm :sellerFirm="seller_firm" /></b-col>
            </b-row>

        </b-card-title>
        <b-card-text>
            <b-row>
                <b-col cols="auto"><b>Client ID:</b></b-col>
                <b-col cols="auto" class="mr-auto">
                    <span v-if="seller_firm.accounting_firm_client_id">{{ seller_firm.accounting_firm_client_id }} </span>
                    <span v-else><i>No ID assigned to this client.</i></span>
                </b-col>
            </b-row>
            <br>
            <b-row>
                <b-col cols="auto"><b>Address:</b></b-col>
                <b-col cols="auto" class="mr-auto">{{ seller_firm.address }} </b-col>
            </b-row>
            <b-row>
                <b-col cols="auto"><b>Establishment Country:</b></b-col>
                <b-col cols="auto" class="mr-auto">{{ seller_firm.establishment_country }} </b-col>
            </b-row>
            <br>
            <b-row>
                <b-col cols="auto"><b>Tax Auditors: </b></b-col>
                <b-col cols="auto" class="mr-auto">
                    <b-avatar
                        v-for="(taxAuditor, index) in seller_firm.tax_auditors"
                        :key="taxAuditor.public_id"
                        :id="`popover-target-${taxAuditor.public_id}`"
                        :variant="(index % 2 == 0) ? 'success' : 'info'"
                        :text="taxAuditor.initials"
                        class="mr-1"
                        >

                    </b-avatar>
                    <b-popover
                        v-for="(taxAuditor, index) in seller_firm.tax_auditors"
                        :key="index"
                        :target="`popover-target-${taxAuditor.public_id}`"
                        triggers="hover"
                        variant='info'
                        placement="top"
                    >
                        <template v-slot:title>{{ taxAuditor.name }}</template>
                        <b>Role: </b> {{ get_role(taxAuditor.role) }}
                    </b-popover>
                </b-col>
            </b-row>
            <br>
            <b-row>
                <b-col cols="auto"><b>Created On:</b></b-col>
                <b-col cols="auto" class="mr-auto">{{ seller_firm.created_on }}</b-col>
            </b-row>
            <b-row>
                <b-col cols="auto"><b>Created By:</b></b-col>
                <b-col cols="auto" class="mr-auto">{{ seller_firm.created_by }}</b-col>
            </b-row>
        </b-card-text>
    </b-card>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        name: 'CardClient',
        computed: {
            ...mapState({
                seller_firm: state => state.seller_firm.seller_firm
            }),
            // calcVariant: index => (index % 2 == 0) ? 'success' : 'info'
        },
        methods: {
            get_role(role) {
                return role.replace('_', ' ').replace(/(^\w{1})|(\s{1}\w{1})/g, match => match.toUpperCase());
            }
        }

            // function() {
            //     var taxAuditors = this.seller_firm.tax_auditors
            //     return taxAuditors.map(function(index) {
            //         console.log('index:', index, 'index % 2 == 0:', index % 2 == 0)
            //         return (index % 2 == 0) ? 'success' : 'info'
            //     })
    }
</script>
