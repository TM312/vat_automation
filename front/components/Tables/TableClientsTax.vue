<template>
    <div>
        <b-table :fields="fields" :items="clients" hover>
            <template v-slot:cell(name)="data">
                <nuxt-link :to="`clients/${data.item.public_id}`">{{ data.value }}</nuxt-link>
            </template>
        </b-table>
    </div>
</template>

<script>
export default {
    name: 'TableClientsTax',

    props: {
        clients: {
            type: [Array],
            required: true

        }
    },

    data() {
        return {
            fields: [
                { key: 'name', sortable: false },
                { key: 'address', sortable: false }
            ],
        }
    }
}
</script>

<style>

</style>
