<template>
    <div>
        <b-card v-if="transactions.length > 1" no-body>
            <b-tabs card>
                <b-tab v-for="transaction in transactions" :key="transaction.public_id" :title="transaction.tax_treatment_code" lazy>
                    <b-card title="tbd">{{ transaction }}

                    </b-card>
                    <alert-transaction-input-notification
                        v-for="notification in transaction.notifications"
                        :key="notification.public_id"
                        :notification="notification"
                        class="my-5"
                    />
                </b-tab>
            </b-tabs>
        </b-card>
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: "ViewTransactions",
    computed: {
        ...mapState({
            transactions: state => state.transaction_input.transaction_input.transactions
        })
    }
    // props: {
    //     transactions: {
    //         type: Array,
    //         required: true
    //     }
    // }
};
</script>

<style>
</style>
