<template>
    <div>
        <b-row>
            <b-col cols="12" lg="6" xl="4">
                <b-card title="Base Data">
                    <b-table-lite borderless fixed small :items="itemsDates" :fields="fieldsDates" class="mb-4"/>
                    <b-table-lite borderless fixed small :items="itemsCategory" :fields="fieldsCategory" class="mb-4"/>
                    <b-table-lite borderless fixed small :items="itemsTaxRates" :fields="fieldsTaxRates" class="mb-4">
                        <template v-slot:cell(value)="data">
                            <span>{{ Number.parseFloat(data.value[0] * 100).toFixed(1) }}%</span>
                            <b-badge
                                class="ml-2"
                                v-b-popover.hover.top="taxRateTypes.find(el => el.code === data.value[1])['description']"
                                :title="taxRateTypes.find(el => el.code === data.value[1])['name']"
                                :variant="data.value[1] === 'S' ? 'primary' : 'success'"
                                >
                                {{ taxRateTypes.find(el => el.code === data.value[1])['name'] }}
                            </b-badge>
                        </template>
                    </b-table-lite>
                </b-card>

                <b-card title="Customer" class="mt-5">
                    <b-row>
                        <b-col cols="5" xl="4"><b>Transaction Relationship:</b></b-col>
                        <b-col cols="7" xl="8" style="white-space: pre-wrap word-wrap:break-word" class="mr-auto">
                            <b-button-group size="sm" class="ml-2">
                                <b-button :variant="transaction.customer_relationship === 'B2B' ? 'success' : 'outline-secondary'">B2B</b-button>
                                <b-button :variant="transaction.customer_relationship === 'B2C' ? 'success' : 'outline-secondary'">B2C</b-button>
                            </b-button-group>
                        </b-col>
                    </b-row>
                    <b-row v-if="transaction.customer_relationship === 'B2B'">
                        <b-col cols="5" xl="4"><b>Vat Number:</b></b-col>
                        <b-col cols="7" xl="8" style="white-space: pre-wrap" class="mr-auto">
                            <span>{{ transaction.customer_firm_vatin }}</span>
                            <span v-if="transaction.customer_firm_vatin"><b-icon icon="info-circle" @hover="getVatInfo(transaction.customer_firm_vatin)"/></span>
                        </b-col>
                    </b-row>
                    <b-row v-if="transaction.customer_firm_name">
                        <b-col cols="5" xl="4"><b>Name:</b></b-col>
                        <b-col cols="7" xl="8" style="white-space: pre-wrap" class="mr-auto">{{transaction.customer_firm_name}}</b-col>
                    </b-row>

                </b-card>

            </b-col>
            <b-col cols="12" lg="6" xl="8">
                <b-card title="Prices">
                    <div class="mt-3">
                        <!-- <h6>Item</h6> -->
                        <b-table hover fixed :items="itemsItem" :fields="fieldsItemPrices" class="mb-4" />
                    </div>
                    <div class="my-3">
                        <!-- <h6>Shipment</h6> -->
                        <b-table hover fixed :items="itemsShipment" :fields="fieldsShipmentPrices" class="mb-4" />
                    </div>
                    <div>
                        <!-- <h6>Gift Wrap</h6> -->
                        <b-table hover fixed :items="itemsGiftWrap" :fields="fieldsGiftWrapPrices" class="mb-4" />
                    </div>
                    <div class="mt-2">
                        <b-table hover fixed :items="itemsTotal" :fields="fieldsTotalPrices" class="mb-4" />
                    </div>

                </b-card>
            </b-col>
        </b-row>

        <b-row cols="1" cols-lg="2" cols-xl="4" class="mt-5">
            <b-col v-for="notification in transaction.notifications" :key="notification.public_id" >
                <alert-transaction-input-notification
                    :notification="notification"
                    style="max-width: 50rem;"
                    class="my-3 h-100"
                />
            </b-col>

        </b-row>
    </div>
</template>

<script>

    import { mapState } from 'vuex'

    export default {
        name: 'CardTransaction',
        props: {
            transaction: {
                type: [Array, Object],
                required: true
            }
        },
        computed: {

            ...mapState({
                taxRateTypes: state => state.tax_rate_type.tax_rate_types
            }),

            itemsDates() {
                return [
                    { date: 'Tax Date', value: this.$dateFns.format(this.transaction.tax_date, 'MMMM dd, yyyy'), },
                    { date: 'Tax Calculation Date', value: this.$dateFns.format(this.transaction.tax_calculation_date, 'MMMM dd, yyyy') }
                ]
            },

            fieldsDates() {
                return [
                    { key: 'date', label:'Dates' },
                    { key: 'value', label:'' },
                ]
            },

            itemsCategory() {
                return [
                    { category: 'Transaction Type', value: this.capitalize(this.transaction.type_code) },
                    { category: 'Tax Treatment', value: this.capitalize(this.transaction.tax_treatment_code) },
                    { category: 'Tax Jurisdiction', value: this.transaction.tax_jurisdiction }
                ]
            },

            fieldsCategory() {
                return [
                    { key: 'category', label:'Categories' },
                    { key: 'value', label:'' },
                ]
            },

            itemsTaxRates() {
                return [
                    { tax_rate: 'Item', value: [this.transaction.item_price_vat_rate, this.transaction.item_tax_rate_type_code]},
                    { tax_rate: 'Shipment', value: [this.transaction.shipment_price_vat_rate, this.transaction.shipment_tax_rate_type_code]},
                    { tax_rate: 'Gift Wrap', value: [this.transaction.gift_wrap_price_vat_rate, this.transaction.gift_wrap_tax_rate_type_code] }
                ]
            },

            fieldsTaxRates() {
                return [
                    { key: 'tax_rate', label:'Tax Rates' },
                    { key: 'value', label:'' },
                ]
            },

            itemsItem() {
                return [
                    {
                        x: 'Price',
                        net: `${Number.parseFloat(this.transaction.item_price_net).toFixed(2)} ${this.transaction.transaction_currency_code}`,
                        vat: `${Number.parseFloat(this.transaction.item_price_vat).toFixed(2)} ${this.transaction.transaction_currency_code}`,
                        gross: `${Number.parseFloat(this.transaction.item_price_net + this.transaction.item_price_vat).toFixed(2)} ${this.transaction.transaction_currency_code}`
                    },
                    {
                        x: 'Discount',
                        net: `${Number.parseFloat(this.transaction.item_price_discount_net).toFixed(2)} ${this.transaction.transaction_currency_code}`,
                        vat: `${Number.parseFloat(this.transaction.item_price_discount_vat).toFixed(2)} ${this.transaction.transaction_currency_code}`,
                        gross: `${Number.parseFloat(this.transaction.item_price_discount_net + this.transaction.item_price_discount_vat).toFixed(2)} ${this.transaction.transaction_currency_code}`
                    },
                    {
                        x: 'Total',
                        net: `${Number.parseFloat(this.transaction.item_price_total_net).toFixed(2)} ${this.transaction.transaction_currency_code}`,
                        vat: `${Number.parseFloat(this.transaction.item_price_total_vat).toFixed(2)} ${this.transaction.transaction_currency_code}`,
                        gross: `${Number.parseFloat(this.transaction.item_price_total_net + this.transaction.item_price_total_vat).toFixed(2)} ${this.transaction.transaction_currency_code}`
                }
                ]
            },

            itemsShipment() {
                return [
                    {
                        x: 'Price',
                        net: `${Number.parseFloat(this.transaction.shipment_price_net).toFixed(2)} ${this.transaction.transaction_currency_code}`,
                        vat: `${Number.parseFloat(this.transaction.shipment_price_vat).toFixed(2)} ${this.transaction.transaction_currency_code}`,
                        gross: `${Number.parseFloat(this.transaction.shipment_price_net + this.transaction.shipment_price_vat).toFixed(2)} ${this.transaction.transaction_currency_code}`
                    },
                    {
                        x: 'Discount',
                        net: `${Number.parseFloat(this.transaction.shipment_price_discount_net).toFixed(2)} ${this.transaction.transaction_currency_code}`,
                        vat: `${Number.parseFloat(this.transaction.shipment_price_discount_vat).toFixed(2)} ${this.transaction.transaction_currency_code}`,
                        gross: `${Number.parseFloat(this.transaction.shipment_price_discount_net + this.transaction.shipment_price_discount_vat).toFixed(2)} ${this.transaction.transaction_currency_code}`
                    },
                    {
                        x: 'Total',
                        net: `${Number.parseFloat(this.transaction.shipment_price_total_net).toFixed(2)} ${this.transaction.transaction_currency_code}`,
                        vat: `${Number.parseFloat(this.transaction.shipment_price_total_vat).toFixed(2)} ${this.transaction.transaction_currency_code}`,
                        gross: `${Number.parseFloat(this.transaction.shipment_price_total_net + this.transaction.shipment_price_total_vat).toFixed(2)} ${this.transaction.transaction_currency_code}`
                }
                ]
            },

            itemsGiftWrap() {
                return [
                    {
                        x: 'Price',
                        net: `${Number.parseFloat(this.transaction.gift_wrap_price_net).toFixed(2)} ${this.transaction.transaction_currency_code}`,
                        vat: `${Number.parseFloat(this.transaction.gift_wrap_price_vat).toFixed(2)} ${this.transaction.transaction_currency_code}`,
                        gross: `${Number.parseFloat(this.transaction.gift_wrap_price_net + this.transaction.gift_wrap_price_vat).toFixed(2)} ${this.transaction.transaction_currency_code}`
                    },
                    {
                        x: 'Discount',
                        net: `${Number.parseFloat(this.transaction.gift_wrap_price_discount_net).toFixed(2)} ${this.transaction.transaction_currency_code}`,
                        vat: `${Number.parseFloat(this.transaction.gift_wrap_price_discount_vat).toFixed(2)} ${this.transaction.transaction_currency_code}`,
                        gross: `${Number.parseFloat(this.transaction.gift_wrap_price_discount_net + this.transaction.gift_wrap_price_discount_vat).toFixed(2)} ${this.transaction.transaction_currency_code}`
                    },
                    {
                        x: 'Total',
                        net: `${Number.parseFloat(this.transaction.gift_wrap_price_total_net).toFixed(2)} ${this.transaction.transaction_currency_code}`,
                        vat: `${Number.parseFloat(this.transaction.gift_wrap_price_total_vat).toFixed(2)} ${this.transaction.transaction_currency_code}`,
                        gross: `${Number.parseFloat(this.transaction.gift_wrap_price_total_net + this.transaction.gift_wrap_price_total_vat).toFixed(2)} ${this.transaction.transaction_currency_code}`
                }
                ]
            },

            itemsTotal() {
                return [
                    {
                        x: 'Total',
                        net: `${Number.parseFloat(this.transaction.total_value_net).toFixed(2)} ${this.transaction.transaction_currency_code}`,
                        vat: `${Number.parseFloat(this.transaction.total_value_vat).toFixed(2)} ${this.transaction.transaction_currency_code}`,
                        gross: `${Number.parseFloat(this.transaction.total_value_gross + this.transaction.gift_wrap_price_vat).toFixed(2)} ${this.transaction.transaction_currency_code}`
                    },
                    {
                        x: `Reverse Charge (Rate: ${Number.parseFloat(this.transaction.vat_rate_reverse_charge * 100).toFixed(2)}%)`,
                        net: '-',
                        vat: `${Number.parseFloat(this.transaction.invoice_amount_vat_reverse_charge).toFixed(2)} ${this.transaction.transaction_currency_code}`,
                        gross: '-'
                }
                ]
            },

            fieldsPrices() {
                return [
                    {
                        key: 'net',
                        sortable: false
                    },
                    {
                        key: 'vat',
                        sortable: false
                    },
                    {
                        key: 'gross',
                        sortable: false
                    },
                ]
            },

            // https://stackoverflow.com/questions/8073673/how-can-i-add-new-array-elements-at-the-beginning-of-an-array-in-javascript

            fieldsItemPrices() {
                return [{ key: 'x', label: 'Item', sortable: false }].concat(this.fieldsPrices)
            },
             fieldsShipmentPrices() {
                return [{ key: 'x', label: 'Shipment', sortable: false }].concat(this.fieldsPrices)
            },
             fieldsGiftWrapPrices() {
                return [{ key: 'x', label: 'Gift Wrap', sortable: false }].concat(this.fieldsPrices)
            },
             fieldsTotalPrices() {
                return [{ key: 'x', label: 'Total', sortable: false }].concat(this.fieldsPrices)
            }
        },
        methods: {
            getVatInfo(vatin) {
                console.log(vatin)
            },
            getPopupDetail(code, position) {
                return this.taxRateTypes.find(el => el.code === code)[position]
            },
        },
    };
</script>

<style>
</style>
