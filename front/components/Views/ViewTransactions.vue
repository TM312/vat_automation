<template>
    <div>
        <b-card
            no-body
            border-variant="primary"
            header-bg-variant="primary"
            header-text-variant="white"
            >
            <b-tabs card>
                <b-tab v-for="transaction in transactions" :key="transaction.public_id" :title="transaction.tax_treatment_code" lazy>
                    <card-transaction :transaction="transaction" />
                    <alert-transaction-input-notification
                        v-for="notification in transaction.notifications"
                        :key="notification.public_id"
                        :notification="notification"
                        style="max-width: 50rem;"
                        class="my-3"
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
