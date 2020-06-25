<template>
    <div class="mt-3">
        <p>Below you find examples and complementary information for each of the fields in the template.</p>
        <b-table hover :items="items" :fields="fields"></b-table>
    </div>
</template>

<script>
    export default {
        name: "TemplateInformation",
        data() {
            return {
                fields: [
                    {
                        key: 'field_name',
                        sortable: true,
                        variant: 'light'
                    },
                    'example',
                    'required',
                    'field_formatting',
                    'complementary_information'
                ],
            }
        },
        props: {
            items: {
                type: [Array, Object],
                required: true
            }
        }
    };
</script>

<style>
</style>
