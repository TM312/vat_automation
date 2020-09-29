<template>
    <b-container fluid class="my-3">
        <b-row class="my-5 px-3" cols="1" cols-xl="2">
            <b-col class="mb-2 pr-5">
                <h3>Local Sales</h3><br>
                <b-table :items="itemsLocalSales" :fields="fieldsNetVatGross" hover/>
            </b-col>

            <b-col class="mb-2 pr-5">
                <h3>Local Sales Reverse Charge</h3><br>
                <b-table :items="itemsLocalSaleReverseCharges" :fields="fieldsNetVatGross" hover/>
            </b-col>
        </b-row>

        <b-row class="my-5" cols="1" cols-xl="2">
            <b-col class="mb-2 pr-5">
                <h3>Distance Sales</h3><br>
                <b-table :items="itemsDistanceSales" :fields="fieldsNetVatGross" hover/>
            </b-col>

            <b-col class="mb-2 pr-5">
                <h3>Non-taxable Distance Sales</h3><br>
                <b-table :items="itemsNonTaxableDistanceSales" :fields="fieldsNetVatGross" hover/>
            </b-col>
        </b-row>

        <b-row class="my-5" cols="1" cols-xl="2">
            <b-col class="mb-2 pr-5">
                <h3>Intra-Community Sales</h3><br>
                <b-table :items="itemsIntraCommunitySales" :fields="fieldsNet" hover/>
            </b-col>

            <b-col class="mb-2 pr-5">
                <h3>Exports</h3><br>
                <b-table :items="itemsExports" :fields="fieldsNet" hover/>
            </b-col>
        </b-row>

        <b-row class="my-5" cols="1" cols-xl="2">
            <b-col class="mb-2 pr-5">
                <h3>Intra-Community Acquisitions</h3><br>
                <b-table :items="itemsIntraCommunityAcquisitions" :fields="fieldsNetReverseCharge" hover/>
            </b-col>

            <b-col class="mb-2 pr-5">
                <h3>Local Acquisitions</h3><br>
                <b-table :items="itemsLocalAcquisitions" :fields="fieldsNetVatGross" hover/>
            </b-col>
        </b-row>

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
                    sortable: false
                },
                {
                    key: 'netAmount',
                    sortable: false,
                    formatter: value => {
                        return  `${Number.parseFloat(value).toFixed(2)} ${this.taxRecord.currency_code}`;
                    }
                }
            ],

            fieldsNetReverseCharge: [
                {
                    key: 'itemName',
                    label: '',
                    sortable: false
                },
                {
                    key: 'netAmount',
                    sortable: false,
                    formatter: value => {
                        return  `${Number.parseFloat(value).toFixed(2)} ${this.taxRecord.currency_code}`;
                    }
                },
                {
                    key: 'reverseChargeAmount',
                    sortable: false,
                    formatter: value => {
                        return  `${Number.parseFloat(value).toFixed(2)} ${this.taxRecord.currency_code}`;
                    }
                }
            ],


            fieldsNetVatGross: [
                {
                    key: 'itemName',
                    label: '',
                    sortable: false,
                },
                {
                    key: 'netAmount',
                    sortable: false,
                    formatter: value => {
                        return  `${Number.parseFloat(value).toFixed(2)} ${this.taxRecord.currency_code}`;
                    }
                },
                {
                    key: 'vatAmount',
                    sortable: false,
                    formatter: value => {
                        return  `${Number.parseFloat(value).toFixed(2)} ${this.taxRecord.currency_code}`;
                    }
                },
                {
                    key: 'grossAmount',
                    sortable: false,
                    formatter: value => {
                        return  `${Number.parseFloat(value).toFixed(2)} ${this.taxRecord.currency_code}`;
                    }
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
                    'netAmount': this.taxRecord.local_sales_sales_invoice_amount_net,
                    'vatAmount': this.taxRecord.local_sales_sales_invoice_amount_vat,
                    'grossAmount': this.taxRecord.local_sales_sales_invoice_amount_gross,
                },
                {
                    'itemName': 'Refunds',
                    'netAmount': this.taxRecord.local_sales_refunds_invoice_amount_net,
                    'vatAmount': this.taxRecord.local_sales_refunds_invoice_amount_vat,
                    'grossAmount': this.taxRecord.local_sales_refunds_invoice_amount_gross,
                },
                {
                    'itemName': 'Total',
                    'netAmount': this.taxRecord.local_sales_total_invoice_amount_net,
                    'vatAmount': this.taxRecord.local_sales_total_invoice_amount_vat,
                    'grossAmount': this.taxRecord.local_sales_total_invoice_amount_gross,
                }
            ]
        },

        itemsLocalSaleReverseCharges() {
            return [
                {
                    'itemName': 'Sales',
                    'netAmount': this.taxRecord.local_sale_reverse_charges_sales_invoice_amount_net,
                    'vatAmount': this.taxRecord.local_sale_reverse_charges_sales_invoice_amount_vat,
                    'grossAmount': this.taxRecord.local_sale_reverse_charges_sales_invoice_amount_gross,
                },
                {
                    'itemName': 'Refunds',
                    'netAmount': this.taxRecord.local_sale_reverse_charges_refunds_invoice_amount_net,
                    'vatAmount': this.taxRecord.local_sale_reverse_charges_refunds_invoice_amount_vat,
                    'grossAmount': this.taxRecord.local_sale_reverse_charges_refunds_invoice_amount_gross,
                },
                {
                    'itemName': 'Total',
                    'netAmount': this.taxRecord.local_sale_reverse_charges_total_invoice_amount_net,
                    'vatAmount': this.taxRecord.local_sale_reverse_charges_total_invoice_amount_vat,
                    'grossAmount': this.taxRecord.local_sale_reverse_charges_total_invoice_amount_gross,
                }
            ]
        },

        itemsDistanceSales() {
            return [
                {
                    'itemName': 'Sales',
                    'netAmount': this.taxRecord.distance_sales_sales_invoice_amount_net,
                    'vatAmount': this.taxRecord.distance_sales_sales_invoice_amount_vat,
                    'grossAmount': this.taxRecord.distance_sales_sales_invoice_amount_gross,
                },
                {
                    'itemName': 'Refunds',
                    'netAmount': this.taxRecord.distance_sales_refunds_invoice_amount_net,
                    'vatAmount': this.taxRecord.distance_sales_refunds_invoice_amount_vat,
                    'grossAmount': this.taxRecord.distance_sales_refunds_invoice_amount_gross,
                },
                {
                    'itemName': 'Total',
                    'netAmount': this.taxRecord.distance_sales_total_invoice_amount_net,
                    'vatAmount': this.taxRecord.distance_sales_total_invoice_amount_vat,
                    'grossAmount': this.taxRecord.distance_sales_total_invoice_amount_gross,
                }
            ]
        },

        itemsNonTaxableDistanceSales() {
            return [
                {
                    'itemName': 'Sales',
                    'netAmount': this.taxRecord.non_taxable_distance_sales_sales_invoice_amount_net,
                    'vatAmount': this.taxRecord.non_taxable_distance_sales_sales_invoice_amount_vat,
                    'grossAmount': this.taxRecord.non_taxable_distance_sales_sales_invoice_amount_gross,
                },
                {
                    'itemName': 'Refunds',
                    'netAmount': this.taxRecord.non_taxable_distance_sales_refunds_invoice_amount_net,
                    'vatAmount': this.taxRecord.non_taxable_distance_sales_refunds_invoice_amount_vat,
                    'grossAmount': this.taxRecord.non_taxable_distance_sales_refunds_invoice_amount_gross,
                },
                {
                    'itemName': 'Total',
                    'netAmount': this.taxRecord.non_taxable_distance_sales_total_invoice_amount_net,
                    'vatAmount': this.taxRecord.non_taxable_distance_sales_total_invoice_amount_vat,
                    'grossAmount': this.taxRecord.non_taxable_distance_sales_total_invoice_amount_gross,
                }
            ]
        },

        itemsIntraCommunitySales() {
            return [
                {
                    'itemName': 'Sales',
                    'netAmount': this.taxRecord.intra_community_sales_sales_invoice_amount_net,                },
                {
                    'itemName': 'Refunds',
                    'netAmount': this.taxRecord.intra_community_sales_refunds_invoice_amount_net,
                },
                {
                    'itemName': 'Total',
                    'netAmount': this.taxRecord.intra_community_sales_total_invoice_amount_net,
                }
            ]
        },

        itemsExports() {
            return [
                {
                    'itemName': 'Sales',
                    'netAmount': this.taxRecord.exports_sales_invoice_amount_net
                },
                {
                    'itemName': 'Refunds',
                    'netAmount': this.taxRecord.exports_refunds_invoice_amount_net
                },
                {
                    'itemName': 'Total',
                    'netAmount': this.taxRecord.exports_total_invoice_amount_net
                }
            ]
        },

        itemsIntraCommunityAcquisitions() {
            return [
                {
                    'itemName': 'Acquisitions',
                    'netAmount': this.taxRecord.ica_acquisitions_invoice_amount_net,
                    'reverseChargeAmount': this.taxRecord.ica_acquisitions_invoice_amount_vat_reverse_charge
                },
                {
                    'itemName': 'Refunds',
                    'netAmount': this.taxRecord.ica_refunds_invoice_amount_net,
                    'reverseChargeAmount': this.taxRecord.ica_refunds_invoice_amount_vat_reverse_charge
                },
                {
                    'itemName': 'Total',
                    'netAmount': this.taxRecord.ica_total_invoice_amount_net,
                    'reverseChargeAmount': this.taxRecord.ica_total_invoice_amount_vat_reverse_charge
                }
            ]
        },

        itemsLocalAcquisitions() {
            return [
                {
                    'itemName': 'Acquisitions',
                    'netAmount': this.taxRecord.local_acquisitions_acquisitions_invoice_amount_net,
                    'vatAmount': this.taxRecord.local_acquisitions_acquisitions_invoice_amount_vat,
                    'grossAmount': this.taxRecord.local_acquisitions_acquisitions_invoice_amount_gross,
                },
                {
                    'itemName': 'Refunds',
                    'netAmount': this.taxRecord.local_acquisitions_refunds_invoice_amount_net,
                    'vatAmount': this.taxRecord.local_acquisitions_refunds_invoice_amount_vat,
                    'grossAmount': this.taxRecord.local_acquisitions_refunds_invoice_amount_gross,
                },
                {
                    'itemName': 'Total',
                    'netAmount': this.taxRecord.local_acquisitions_total_invoice_amount_net,
                    'vatAmount': this.taxRecord.local_acquisitions_total_invoice_amount_vat,
                    'grossAmount': this.taxRecord.local_acquisitions_total_invoice_amount_gross,
                }
            ]
        }
    }

}
</script>

<style>

</style>
