<template>
    <b-container fluid>
        <b-row>
            <b-col cols="4">
                A card showing the number of clients
            </b-col>
            <b-col cols="4">
                A card showing sth else
            </b-col>
        </b-row>

        <hr>

        <AllClients />

    </b-container>
</template>

<script>
// import Metrics from './Metrics'
// import AllClients from './AllClients'
export default {
    name: 'Overview',
    // components: {
    //     Metrics,
    //     AllClients
    // }
}
</script>

<style>

</style>
