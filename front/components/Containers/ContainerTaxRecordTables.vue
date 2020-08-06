<template>
    <b-container fluid class="my-3">
        <div>
            <h3>Local Sales</h3><br>
            <b-table :items="itemsLocalSales" :fields="fieldsNetVatGross" borderless />
        </div>

        <div>
            <h3>Local Sales Reverse Charge</h3><br>
            <b-table :items="itemsLocalSaleReverseCharges" :fields="fieldsNetVatGross" borderless />
        </div>

        <div>
            <h3>Distance Sales</h3><br>
            <b-table :items="itemsDistanceSales" :fields="fieldsNetVatGross" borderless />
        </div>

        <div>
            <h3>Non-taxable Distance Sales</h3><br>
            <b-table :items="itemsNonTaxableDistanceSales" :fields="fieldsNetVatGross" borderless />
        </div>

        <div>
            <h3>Intra-Community Sales</h3><br>
            <b-table :items="itemsIntraCommunitySales" :fields="fieldsNet" borderless />
        </div>

            <div>
            <h3>Exports</h3><br>
            <b-table :items="itemsExports" :fields="fieldsNet" borderless />
        </div>

        <div>
            <h3>Intra-Community Acquisitions</h3><br>
            <b-table :items="itemsIntraCommunityAcquisitions" :fields="fieldsNetReverseCharge" borderless />
        </div>

        <div>
            <h3>Local Acquisitions</h3><br>
            <b-table :items="itemsLocalAcquisitions" :fields="fieldsNetVatGross" borderless />
        </div>

    </b-container>
</template>

<script>
import { mapState } from 'vuex';

export default {
    name: 'ContainerTaxRecordTables',

    data() {
        return {
            fieldsNet: [
                {
                    key: 'itemName',
                    label: '',
                    sortable: false,
                },
                {
                    key: 'netInvoiceAmount',
                    sortable: false,
                }
            ],

            fieldsNetReverseCharge: [
                {
                    key: 'itemName',
                    label: '',
                    sortable: false,
                },
                {
                    key: 'netInvoiceAmount',
                    sortable: false,
                },
                {
                    key: 'reverseChargeAmount',
                    sortable: false,
                }
            ],


            fieldsNetVatGross: [
                {
                    key: 'itemName',
                    label: '',
                    sortable: false,
                },
                {
                    key: 'netInvoiceAmount',
                    sortable: false,
                },
                {
                    key: 'vatInvoiceAmount',
                    sortable: false,
                },
                {
                    key: 'grossInvoiceAmount',
                    sortable: false,
                }
            ]
        }
    },

    computed: {
        ...mapState({
            taxRecord: state => state.tax_record.tax_record
        }),

        itemsLocalSales() {
            return [
                {
                    'itemName': 'Sales',
                    'netInvoiceAmount': this.taxRecord.local_sales_sales_invoice_amount_net,
                    'vatInvoiceAmount': this.taxRecord.local_sales_sales_invoice_amount_vat,
                    'grossInvoiceAmount': this.taxRecord.local_sales_sales_invoice_amount_gross,
                },
                {
                    'itemName': 'Refunds',
                    'netInvoiceAmount': this.taxRecord.local_sales_refunds_invoice_amount_net,
                    'vatInvoiceAmount': this.taxRecord.local_sales_refunds_invoice_amount_vat,
                    'grossInvoiceAmount': this.taxRecord.local_sales_refunds_invoice_amount_gross,
                },
                {
                    'itemName': 'Total',
                    'netInvoiceAmount': this.taxRecord.local_sales_total_invoice_amount_net,
                    'vatInvoiceAmount': this.taxRecord.local_sales_total_invoice_amount_vat,
                    'grossInvoiceAmount': this.taxRecord.local_sales_total_invoice_amount_gross,
                }
            ]
        },

        itemsLocalSaleReverseCharges() {
            return [
                {
                    'itemName': 'Sales',
                    'netInvoiceAmount': this.taxRecord.local_sale_reverse_charges_sales_invoice_amount_net,
                    'vatInvoiceAmount': this.taxRecord.local_sale_reverse_charges_sales_invoice_amount_vat,
                    'grossInvoiceAmount': this.taxRecord.local_sale_reverse_charges_sales_invoice_amount_gross,
                },
                {
                    'itemName': 'Refunds',
                    'netInvoiceAmount': this.taxRecord.local_sale_reverse_charges_refunds_invoice_amount_net,
                    'vatInvoiceAmount': this.taxRecord.local_sale_reverse_charges_refunds_invoice_amount_vat,
                    'grossInvoiceAmount': this.taxRecord.local_sale_reverse_charges_refunds_invoice_amount_gross,
                },
                {
                    'itemName': 'Total',
                    'netInvoiceAmount': this.taxRecord.local_sale_reverse_charges_total_invoice_amount_net,
                    'vatInvoiceAmount': this.taxRecord.local_sale_reverse_charges_total_invoice_amount_vat,
                    'grossInvoiceAmount': this.taxRecord.local_sale_reverse_charges_total_invoice_amount_gross,
                }
            ]
        },

        itemsDistanceSales() {
            return [
                {
                    'itemName': 'Sales',
                    'netInvoiceAmount': this.taxRecord.distance_sales_sales_invoice_amount_net,
                    'vatInvoiceAmount': this.taxRecord.distance_sales_sales_invoice_amount_vat,
                    'grossInvoiceAmount': this.taxRecord.distance_sales_sales_invoice_amount_gross,
                },
                {
                    'itemName': 'Refunds',
                    'netInvoiceAmount': this.taxRecord.distance_sales_refunds_invoice_amount_net,
                    'vatInvoiceAmount': this.taxRecord.distance_sales_refunds_invoice_amount_vat,
                    'grossInvoiceAmount': this.taxRecord.distance_sales_refunds_invoice_amount_gross,
                },
                {
                    'itemName': 'Total',
                    'netInvoiceAmount': this.taxRecord.distance_sales_total_invoice_amount_net,
                    'vatInvoiceAmount': this.taxRecord.distance_sales_total_invoice_amount_vat,
                    'grossInvoiceAmount': this.taxRecord.distance_sales_total_invoice_amount_gross,
                }
            ]
        },

        itemsNonTaxableDistanceSales() {
            return [
                {
                    'itemName': 'Sales',
                    'netInvoiceAmount': this.taxRecord.non_taxable_distance_sales_sales_invoice_amount_net,
                    'vatInvoiceAmount': this.taxRecord.non_taxable_distance_sales_sales_invoice_amount_vat,
                    'grossInvoiceAmount': this.taxRecord.non_taxable_distance_sales_sales_invoice_amount_gross,
                },
                {
                    'itemName': 'Refunds',
                    'netInvoiceAmount': this.taxRecord.non_taxable_distance_sales_refunds_invoice_amount_net,
                    'vatInvoiceAmount': this.taxRecord.non_taxable_distance_sales_refunds_invoice_amount_vat,
                    'grossInvoiceAmount': this.taxRecord.non_taxable_distance_sales_refunds_invoice_amount_gross,
                },
                {
                    'itemName': 'Total',
                    'netInvoiceAmount': this.taxRecord.non_taxable_distance_sales_total_invoice_amount_net,
                    'vatInvoiceAmount': this.taxRecord.non_taxable_distance_sales_total_invoice_amount_vat,
                    'grossInvoiceAmount': this.taxRecord.non_taxable_distance_sales_total_invoice_amount_gross,
                }
            ]
        },

        itemsIntraCommunitySales() {
            return [
                {
                    'itemName': 'Sales',
                    'netInvoiceAmount': this.taxRecord.intra_community_sales_sales_invoice_amount_net,                },
                {
                    'itemName': 'Refunds',
                    'netInvoiceAmount': this.taxRecord.intra_community_sales_refunds_invoice_amount_net,
                },
                {
                    'itemName': 'Total',
                    'netInvoiceAmount': this.taxRecord.intra_community_sales_total_invoice_amount_net,
                }
            ]
        },

        itemsExports() {
            return [
                {
                    'itemName': 'Sales',
                    'netInvoiceAmount': this.taxRecord.exports_sales_invoice_amount_net
                },
                {
                    'itemName': 'Refunds',
                    'netInvoiceAmount': this.taxRecord.exports_refunds_invoice_amount_net
                },
                {
                    'itemName': 'Total',
                    'netInvoiceAmount': this.taxRecord.exports_total_invoice_amount_net
                }
            ]
        },

        itemsIntraCommunityAcquisitions() {
            return [
                {
                    'itemName': 'Acquisitions',
                    'netInvoiceAmount': this.taxRecord.intra_community_acquisitions_acquisitions_invoice_amount_net,
                    'reverseChargeAmount': this.taxRecord.intra_community_acquisitions_acquisitions_invoice_amount_vat_reverse_charge
                },
                {
                    'itemName': 'Refunds',
                    'netInvoiceAmount': this.taxRecord.intra_community_acquisitions_refunds_invoice_amount_net,
                    'reverseChargeAmount': this.taxRecord.intra_community_acquisitions_refunds_invoice_amount_vat_reverse_charge
                },
                {
                    'itemName': 'Total',
                    'netInvoiceAmount': this.taxRecord.intra_community_acquisitions_total_invoice_amount_net,
                    'reverseChargeAmount': this.taxRecord.intra_community_acquisitions_total_invoice_amount_vat_reverse_charge
                }
            ]
        },

        itemsLocalAcquisitions() {
            return [
                {
                    'itemName': 'Acquisitions',
                    'netInvoiceAmount': this.taxRecord.local_acquisitions_acquisitions_invoice_amount_net,
                    'vatInvoiceAmount': this.taxRecord.local_acquisitions_acquisitions_invoice_amount_vat,
                    'grossInvoiceAmount': this.taxRecord.local_acquisitions_acquisitions_invoice_amount_gross,
                },
                {
                    'itemName': 'Refunds',
                    'netInvoiceAmount': this.taxRecord.local_acquisitions_refunds_invoice_amount_net,
                    'vatInvoiceAmount': this.taxRecord.local_acquisitions_refunds_invoice_amount_vat,
                    'grossInvoiceAmount': this.taxRecord.local_acquisitions_refunds_invoice_amount_gross,
                },
                {
                    'itemName': 'Total',
                    'netInvoiceAmount': this.taxRecord.local_acquisitions_total_invoice_amount_net,
                    'vatInvoiceAmount': this.taxRecord.local_acquisitions_total_invoice_amount_vat,
                    'grossInvoiceAmount': this.taxRecord.local_acquisitions_total_invoice_amount_gross,
                }
            ]
        }
    }

}
</script>

<style>

</style>
