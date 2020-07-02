<template>
    <div>
        <b-table
            selectable
            select-mode="single"
            selected-variant="info"
            ref="editTable"
            borderless
            :items="items"
            :fields="fields"
            @row-selected="onRowSelected"
        >
            <!-- <template v-slot:cell(edit)="{ rowSelected }">
                <template v-if="rowSelected">
                    <span aria-hidden="true">
                        <button-remove-entry :publicId="selected.public_id" />
                    </span>
                    <span class="sr-only">Selected</span>
                </template>
                <template v-else>
                    <span aria-hidden="true">&nbsp;</span>
                    <span class="sr-only">Not selected</span>
                </template>
            </template> -->
            <!-- <template v-slot:cell(edit)="row">
                <button-remove-entry :data="data" />
            </template> -->
        </b-table>

        <p>
            Selected Rows:<br>
            {{ selected }}

            <br>
            Type of Selected: {{ typeofselected }}
            <br>

            Public ID: {{ publicid }}
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
            // fieldsEditable: this.fields.concat({ key: 'edit', sortable: false}),
            selected: ''
        }
    },

     methods: {
            // removeFile(key) {
            //     this.files.splice(key, 1);
            //     console.log(this.files);
            // },
            onRowSelected(items) {
                if (items !== "[]") {
                    this.selected = items
                } else {
                    this.selected = ''
                }
                console.log('selected: ', this.selected)
                this.$emit('objectSelected', this.selected)
            }
        },
    computed: {
        typeofselected() {
            return typeof this.selected
        },
        publicid() {
            return this.selected.public_id
        }
    },

}
</script>

<style>

</style>
