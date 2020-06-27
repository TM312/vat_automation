<template>
    <b-card header="Base Data">
        <b-card-text>
            <b>Company Name:</b> {{ client.name  }} <br>
            <b>Public ID:</b> <span class="text-primary" v-b-popover.hover.top="'Use this ID when referring to this client in the templates.'">{{ client.public_id }}</span><br>
            <b>Address:</b> {{ client.address  }} <br>
            <b>Created On:</b> {{ client.created_on }} <br>
            <b>Created By:</b> {{ client.created_by }} <br>
            <br>
            <b>Establishment Country:</b> {{ client.establishment_country }} <i>[<u>{{ client.establishment_country_code }}</u>]</i><br>
        </b-card-text>
    </b-card>
</template>

<script>

    export default {
        name: 'CardClient',
        // eslint-disable-next-line
        props: { client: { type: [Array, Object] } }
    }
</script>
