<template>
    <div>
        <b-tabs content-class="mt-3">
            <b-tab title="Card View" active>
                <b-row class="mb-3" cols="1" cols-md="1" cols-lg="3" cols-xl="4">
                    <card-client-short v-for="(client, i) in $auth.user.key_accounts" :key="i" :business="client" class="mb-2" />
                </b-row>
            </b-tab>
            <b-tab title="Table View">
                <table-clients-tax :clients="$auth.user.key_accounts" />
            </b-tab>
        </b-tabs>
    </div>
</template>

<script>
    import { mapState } from "vuex";

    export default {
        name: 'ViewKeyAccounts',
    }
</script>

<style>
</style>
