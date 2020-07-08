<template>
    <b-tabs content-class="mt-3">
        <b-tab title="Company Data" active>
            <b-card-group deck>
                <card-client class="mb-5"/>
                <card-accounts class="mb-5"/>
            </b-card-group>
            <b-card-group deck>
                <card-vat-numbers class="mb-5"/>
                <card-distance-sales class="mb-5"/>
            </b-card-group>
        </b-tab>
        <b-tab title="Items">
            <lazy-card-items class="mb-5"/>
        </b-tab>
    </b-tabs>
</template>

<script>
    // import { mapState } from "vuex";

    export default {
        name:'OverviewBaseData'
    }
</script>

<style>
</style>
