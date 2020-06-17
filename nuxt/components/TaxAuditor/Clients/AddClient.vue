<template>
    <b-row>
        <b-col cols="12" md="5">
            <AddSingleClient />
        </b-col>
        <b-col cols="12" md="7">
            <AddMultipleClients />
        </b-col>
    </b-row>
</template>

<script>
import AddSingleClient from "./AddSingleClient"
import AddMultipleClients from "./AddMultipleClients"
export default {
    components: {
        AddSingleClient,
        AddMultipleClients
    }
}
</script>

<style>

</style>
