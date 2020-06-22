<template>
    <b-col cols="4">
        <b-card :title="taxAuditor.name">
            <b-card-text>
                <ul>
                    <li>{{ taxAuditor.email }}</li>
                    <li>{{ taxAuditor.public_id }}</li>
                    <li>{{ taxAuditor.last_seen }}</li>
                </ul>
            </b-card-text>
        </b-card>
    </b-col>
</template>

<script>
    export default {
        props: { taxAuditor: { type: [Array, Object] } }
    }
</script>
