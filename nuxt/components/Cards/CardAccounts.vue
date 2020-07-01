<template>
    <b-card header="Accounts">
        <b-card-text>
            <h3 v-if="countAccounts === 0" class="text-secondary text-center">An Overview of This Company's Accounts Can Be Seen Here Once The Corresponding Data Has Been Uploaded</h3>
            <b-table v-else borderless :items="accounts" :fields="fields"></b-table>
        </b-card-text>
    </b-card>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        name: 'CardAccounts',
        props: { accounts: { type: [Array, Object] } },

        data() {
            return {
                fields: [
                {
                    key: 'channel_code',
                    sortable: true
                },
                {
                    key: 'given_id',
                    label: "Platform ID",
                    sortable: false
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
                countAccounts() {
                    return this.$store.getters['seller_firm/countAccounts']
                }
            }),
        }
    }
</script>
