<template>
    <b-container fluid>
        <Metrics />
        <hr>
        <AllClients />
    </b-container>
</template>

<script>
import Metrics from './Metrics'
import AllClients from './AllClients'
export default {
    name: 'Overview',
    components: {
        Metrics,
        AllClients
    }
}
</script>

<style>

</style>
