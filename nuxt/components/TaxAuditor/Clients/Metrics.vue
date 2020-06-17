<template>
    <b-container fluid>
        <b-card
            :title=clients
            sub-title="Total # Clients"
            tag="article"
            style="max-width: 20rem;"
            class="mb-2"
        >
            <b-card-text>
                Some quick example text to build on the card title and make up the bulk of the card's content.
            </b-card-text>

        </b-card>
    </b-container>
</template>

<script>
export default {
    name: "Metrics",
    data: {
        clients: "5"
    }

}
</script>

<style>

</style>
