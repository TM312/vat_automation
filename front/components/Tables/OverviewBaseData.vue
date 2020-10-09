<template>
    <div>
        <!-- <b-nav tabs content-class="mt-3">
            <b-nav-item to="#" :active="$route.hash === '#' || $route.hash === ''">
                Base Data
            </b-nav-item>
            <b-nav-item to="#items" :active="$route.hash === '#items'">
                Items
            </b-nav-item>
            <b-nav-item to="#transactions" :active="$route.hash === '#transactions'">
                Transactions
            </b-nav-item>
        </b-nav> -->

        <!-- <div class="tab-content">
            <div :class="['tab-pane', { 'active': $route.hash === '#' || $route.hash === '' }]" class="py-3"> -->
                <b-card-group deck>
                    <lazy-card-client class="mb-5"/>
                    <lazy-card-accounts class="mb-5"/>
                </b-card-group>
                <b-card-group deck>
                    <lazy-card-vat-numbers class="mb-5"/>
                    <lazy-card-distance-sales class="mb-5"/>
                </b-card-group>
            <!-- </div> -->
            <!-- <div :class="['tab-pane', { 'active': $route.hash === '#items' }]" class="py-3">
                <lazy-card-items class="mb-5"/>
            </div>
            <div :class="['tab-pane', { 'active': $route.hash === '#transactions' }]" class="py-3" lazy>
                <lazy-overview-transaction-inputs />
            </div> -->
        <!-- </div> -->
    </div>

</template>

<script>
    export default {
        name:'OverviewBaseData'
    }
</script>

<style>
</style>
