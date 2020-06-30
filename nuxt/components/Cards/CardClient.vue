<template>
    <b-card header="Base Data" :title="business.name">
        <b-card-text>
            <b>Public ID:</b> <span class="text-primary" v-b-popover.hover.top="'Use this ID when referring to this business in the templates.'">{{ business.public_id }}</span><br>
            <b>Address:</b> {{ business.address  }} <br>
            <b>Establishment Country:</b> {{ business.establishment_country }}<br>
            <br>
            <b>Created On:</b> {{ business.created_on }} <br>
            <b>Created By:</b> {{ business.created_by }} <br>
        </b-card-text>
    </b-card>
</template>

<script>

    export default {
        name: 'CardClient',
        // eslint-disable-next-line
        props: { business: { type: [Array, Object] } }
    }
</script>
