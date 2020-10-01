<template>
    <div>
        <b-row cols="1" cols-lg="2" cols-xl="4" class="my-2">
            <b-col class="my-2 px-2">
                <b-card title="File" class="h-100">
                    <b-table-lite borderless small :items="itemsFile" :fields="fieldsBase" class="mb-4">
                        <template v-slot:cell(value)="data">
                            <span v-if="data.value !== ''">{{ data.value }}</span>
                            <span v-else><text-icon-na /></span>
                        </template>
                    </b-table-lite>
                </b-card>
            </b-col>

            <b-col class="my-2 px-2">
                <b-card title="Source" class="h-100">
                    <b-table-lite borderless small :items="itemsBaseDetails" :fields="fieldsBase" class="mb-4">
                        <template v-slot:cell(value)="data">
                            <span v-if="data.value !== ''">{{ data.value }}</span>
                            <span v-else><text-icon-na /></span>
                        </template>
                    </b-table-lite>
                </b-card>
            </b-col>

            <b-col class="my-2 px-2">
                <b-card title="Dates" class="h-100">
                    <b-table-lite borderless small :items="itemsDate" :fields="fieldsBase" class="mb-4">
                        <template v-slot:cell(value)="data">
                            <span v-if="data.value !== ''">{{ data.value }}</span>
                            <span v-else><text-icon-na /></span>
                        </template>
                    </b-table-lite>
                </b-card>
            </b-col>

            <b-col class="my-2 px-2">
                <b-card title="Logistics" class="h-100">
                     <b-table-lite borderless small :items="itemsLogistics" :fields="fieldsBase" class="mb-4">
                        <template v-slot:cell(value)="data">
                            <span v-if="data.value !== '' && Array.isArray(data.value) === false">{{ data.value }}</span>
                            <span v-else-if="data.value !== '' && Array.isArray(data.value) === true">
                                {{ data.value[0] }} <br>
                                {{ data.value[1] }} {{ data.value[2] }}
                                <span v-if="data.value.length === 3 && data.value[3] !== '' && data.value[3] !== null"><br>{{ data.value[3] }}</span>
                            </span>
                            <span v-else><text-icon-na /></span>
                        </template>
                    </b-table-lite>
                </b-card>
            </b-col>
        </b-row>

        <b-row cols="1" cols-lg="2" cols-xl="3" class="my-2">
            <b-col class="my-2 px-2">
                <b-card title="Item" class="h-100">
                    <b-table-lite borderless small :items="itemsItem" :fields="fieldsBase" class="mb-4">
                        <template v-slot:cell(value)="data">
                            <span v-if="data.value !== ''">{{ data.value }} </span>
                            <span v-else><text-icon-na /></span>
                        </template>
                    </b-table-lite>

                </b-card>
            </b-col>

             <b-col class="my-2 px-2">
                <b-card title="Gross Prices" class="h-100">
                    <b-table hover borderless :items="itemsGrossPrices" :fields="fieldsGrossPrices"></b-table>
                </b-card>
            </b-col>

            <b-col class="my-2 px-2">
                <b-card class="h-100">
                    <b-card-title>
                        <b-row>
                            <b-col cols="auto" class="mr-auto">Invoice</b-col>
                            <b-col cols="auto">
                                <b-button
                                    v-if="transactionInput.invoice_url"
                                    class="ml-2"
                                    size="sm"
                                    variant="outline-primary"
                                    :href="transactionInput.invoice_url"
                                    ><b-icon icon="box-arrow-in-down" /> Download
                                </b-button>

                            </b-col>
                        </b-row>
                    </b-card-title>
                    <b-table-lite borderless small :items="itemsInvoice" :fields="fieldsBase" class="mb-4">
                        <template v-slot:cell(value)="data">
                            <span v-if="data.value !== ''">{{ data.value }}</span>
                            <span v-else><text-icon-na /></span>
                        </template>
                    </b-table-lite>
                </b-card>
            </b-col>


        </b-row>


    </div>

</template>

<script>
import { mapState } from 'vuex'
export default {
    name:'CardTransactionInput',

    computed: {
        ...mapState({
            transactionInput: state => state.transaction_input.transaction_input
        }),

        itemsGrossPrices() {
            return [
                {
                    x: 'Price',
                    item: this.transactionInput.currency_code ? `${Number.parseFloat(this.transactionInput.item_price_gross).toFixed(2)} ${this.transactionInput.currency_code}` : '-',
                    shipment: this.transactionInput.currency_code ? `${Number.parseFloat(this.transactionInput.shipment_price_gross).toFixed(2)} ${this.transactionInput.currency_code}` : '-',
                    gift_wrap: this.transactionInput.currency_code ? `${Number.parseFloat(this.transactionInput.gift_wrap_price_gross).toFixed(2)} ${this.transactionInput.currency_code}` : '-'
                },
                {
                    x: 'Discount',
                    item: this.transactionInput.currency_code ? `${Number.parseFloat(this.transactionInput.item_price_discount_gross).toFixed(2)} ${this.transactionInput.currency_code}` : '-',
                    shipment: this.transactionInput.currency_code ? `${Number.parseFloat(this.transactionInput.shipment_price_discount_gross).toFixed(2)} ${this.transactionInput.currency_code}` : '-',
                    gift_wrap: this.transactionInput.currency_code ? `${Number.parseFloat(this.transactionInput.gift_wrap_price_discount_gross).toFixed(2)} ${this.transactionInput.currency_code}` : '-'
                },
                {
                    x: 'Total',
                    item: this.transactionInput.currency_code ? `${Number.parseFloat(this.transactionInput.item_price_total_gross).toFixed(2)} ${this.transactionInput.currency_code}` : '-',
                    shipment: this.transactionInput.currency_code ? `${Number.parseFloat(this.transactionInput.shipment_price_total_gross).toFixed(2)} ${this.transactionInput.currency_code}` : '-',
                    gift_wrap: this.transactionInput.currency_code ? `${Number.parseFloat(this.transactionInput.gift_wrap_price_total_gross).toFixed(2)} ${this.transactionInput.currency_code}` : '-'
               }
            ]


        },

        fieldsGrossPrices() {
            return [
                {
                    key: 'x',
                    label:'',
                    sortable: false
                },
                {
                    key: 'item',
                    sortable: false
                },
                {
                    key: 'shipment',
                    sortable: false
                },
                {
                    key: 'gift_wrap',
                    sortable: false
                }
            ]
        },


        fieldsBase() {
            return [
                { key: 'key', label:'' },
                { key: 'value', label:'' },
            ]
        },

        itemsFile() {
            return [
                { key: 'Name', value: this.transactionInput.original_filename },
                { key: 'Uploaded On', value: this.transactionInput.created_on ? this.$dateFns.format(this.transactionInput.created_on, 'MMMM dd, yyyy') : null },
                { key: 'Uploaded By', value: this.transactionInput.created_by}
            ]
        },

        itemsBaseDetails() {
            return [
                { key: 'Channel', value: this.transactionInput.channel_code },
                { key: 'Account', value: this.transactionInput.account_given_id },
                { key: 'Marketplace', value: this.transactionInput.marketplace},
                { key: 'Transaction ID', value: this.transactionInput.activity_id},
                { key: 'Transaction Type', value: this.capitalize(this.transactionInput.transaction_type_public_code)}
            ]
        },

        itemsDate() {
            return [
                { key: 'Activity Period', value: this.transactionInput.public_activity_period },
                { key: 'Shipment', value: this.transactionInput.shipment_date ? this.$dateFns.format(this.transactionInput.shipment_date, 'MMMM dd, yyyy') : null },
                { key: 'Arrival', value: this.transactionInput.arrival_date ? this.$dateFns.format(this.transactionInput.arrival_date,  'MMMM dd, yyyy') : null },
                { key: 'Complete', value: this.transactionInput.complete_date ? this.$dateFns.format(this.transactionInput.complete_date,  'MMMM dd, yyyy') : null },
                { key: 'Tax Calculation', value: this.transactionInput.check_tax_calculation_date ? this.$dateFns.format(this.transactionInput.check_tax_calculation_date,  'MMMM dd, yyyy') : null }
            ]
        },

        itemsLogistics() {
            return [
                {
                    key: 'Departure',
                    value: [this.transactionInput.departure_country_code, this.transactionInput.departure_postal_code, this.transactionInput.departure_city],
                },
                {
                    key: 'Arrival',
                    value: [this.transactionInput.arrival_country_code, this.transactionInput.arrival_postal_code, this.transactionInput.arrival_city, this.transactionInput.arrival_address],
                },
                { key: 'Mode', value: this.transactionInput.shipment_mode ? this.capitalize(this.transactionInput.shipment_mode) : null },
                { key: 'Conditions', value: this.transactionInput.shipment_conditions }
            ]
        },

        itemsInvoice() {
            return [
                { key: 'Number', value: this.transactionInput.invoice_number },
                { key: 'Tax Jurisdiction', value: this.transactionInput.check_tax_jurisdiction ? this.capitalize(this.transactionInput.check_tax_jurisdiction) : null },
                { key: 'Vat Amount', value: this.transactionInput.check_invoice_amount_vat ? `${this.transactionInput.check_invoice_amount_vat} ${this.transactionInput.check_invoice_currency_code}` : null},
                { key: 'Exchange Rate', value: this.transactionInput.check_invoice_exchange_rate ? `${this.transactionInput.check_invoice_exchange_rate} | Date: ${ this.transactionInput.check_invoice_exchange_rate_date}` : null}
            ]
        },

        itemsItem() {
            return [
                { key: 'SKU', value: this.transactionInput.item_sku },
                { key: 'Name', value: this.transactionInput.item_name },
                { key: 'Quantity', value: this.transactionInput.item_quantity },
                { key: 'Manufactured In', value: this.transactionInput.item_manufacture_country },
                { key: 'Item Weight', value: this.transactionInput.item_weight_kg ? `${Number.parseFloat(this.transactionInput.item_weight_kg).toFixed(3)}kg` : null},
                { key: 'Total Weight', value: this.transactionInput.item_weight_kg_total ? `${Number.parseFloat(this.transactionInput.item_weight_kg_total).toFixed(3)}kg` : null}
            ]
        },
    }

}
</script>
