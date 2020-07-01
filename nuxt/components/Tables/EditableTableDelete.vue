<template>
    <div>
        <b-table
            selectable
            select-mode="single"
            ref="editTable"
            borderless
            :items="items"
            :fields="fieldsEditable"
            @row-selected="onRowSelected"
        >
            <template v-slot:cell(edit)="{ rowSelected }">
                <template v-if="rowSelected">
                    <span aria-hidden="true">
                        <button-remove-entry />
                    </span>
                    <span class="sr-only">Selected</span>
                </template>
                <template v-else>
                    <span aria-hidden="true">&nbsp;</span>
                    <span class="sr-only">Not selected</span>
                </template>
            </template>
            <!-- <template v-slot:cell(edit)="row">
                <button-remove-entry :data="data" />
            </template> -->
        </b-table>

        <p>
            Selected Rows:<br>
            {{ selected }}
        </p>
    </div>
</template>

<script>
export default {
    name: 'EditableTableDelete',
    props: {
            items: {
                type: [Array, Object],
                required: true
            },
            fields: {
                type: [Array, Object],
                required: true
            }
        },
    data() {
        return {
            fieldsEditable: this.fields.concat({ key: 'edit', sortable: false}),
            selected: []
        }
    },

     methods: {
            // removeFile(key) {
            //     this.files.splice(key, 1);
            //     console.log(this.files);
            // },
            onRowSelected(items) {
                this.selected = items
            }
        }

}
</script>

<style>

</style>
