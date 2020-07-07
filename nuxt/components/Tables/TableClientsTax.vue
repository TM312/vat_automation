<template>
    <div>
        <b-table :fields="fields" :items="clients" hover>
            <template v-slot:cell(name)="data">
                <nuxt-link :to="data.item.public_id" append >{{ data.value }}</nuxt-link>
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
                { key: 'name', sortable: true },
                { key: 'address', sortable: false },
                { key: 'len_vat_numbers', label: '# Vat Numbers', sortable: false },
                { key: 'created_on', sortable: true },
                { key: 'created_by', sortable: true },
            ],
        }
    }
}
</script>

<style>

</style>
