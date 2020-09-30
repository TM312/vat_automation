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
                    key: 'net',
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
                    key: 'net',
                    sortable: false,
                    formatter: value => {
                        return  `${Number.parseFloat(value).toFixed(2)} ${this.taxRecord.currency_code}`;
                    }
                },
                {
                    key: 'reverseChargeVat',
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
                    key: 'net',
                    sortable: false,
                    formatter: value => {
                        return  `${Number.parseFloat(value).toFixed(2)} ${this.taxRecord.currency_code}`;
                    }
                },
                {
                    key: 'vat',
                    sortable: false,
                    formatter: value => {
                        return  `${Number.parseFloat(value).toFixed(2)} ${this.taxRecord.currency_code}`;
                    }
                },
                {
                    key: 'gross',
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
                    'net': this.taxRecord.local_sales_sales_net,
                    'vat': this.taxRecord.local_sales_sales_vat,
                    'gross': this.taxRecord.local_sales_sales_gross,
                },
                {
                    'itemName': 'Refunds',
                    'net': this.taxRecord.local_sales_refunds_net,
                    'vat': this.taxRecord.local_sales_refunds_vat,
                    'gross': this.taxRecord.local_sales_refunds_gross,
                },
                {
                    'itemName': 'Total',
                    'net': this.taxRecord.local_sales_total_net,
                    'vat': this.taxRecord.local_sales_total_vat,
                    'gross': this.taxRecord.local_sales_total_gross,
                }
            ]
        },

        itemsLocalSaleReverseCharges() {
            return [
                {
                    'itemName': 'Sales',
                    'net': this.taxRecord.local_sale_reverse_charges_sales_net,
                    'vat': this.taxRecord.local_sale_reverse_charges_sales_vat,
                    'gross': this.taxRecord.local_sale_reverse_charges_sales_gross,
                },
                {
                    'itemName': 'Refunds',
                    'net': this.taxRecord.local_sale_reverse_charges_refunds_net,
                    'vat': this.taxRecord.local_sale_reverse_charges_refunds_vat,
                    'gross': this.taxRecord.local_sale_reverse_charges_refunds_gross,
                },
                {
                    'itemName': 'Total',
                    'net': this.taxRecord.local_sale_reverse_charges_total_net,
                    'vat': this.taxRecord.local_sale_reverse_charges_total_vat,
                    'gross': this.taxRecord.local_sale_reverse_charges_total_gross,
                }
            ]
        },

        itemsDistanceSales() {
            return [
                {
                    'itemName': 'Sales',
                    'net': this.taxRecord.distance_sales_sales_net,
                    'vat': this.taxRecord.distance_sales_sales_vat,
                    'gross': this.taxRecord.distance_sales_sales_gross,
                },
                {
                    'itemName': 'Refunds',
                    'net': this.taxRecord.distance_sales_refunds_net,
                    'vat': this.taxRecord.distance_sales_refunds_vat,
                    'gross': this.taxRecord.distance_sales_refunds_gross,
                },
                {
                    'itemName': 'Total',
                    'net': this.taxRecord.distance_sales_total_net,
                    'vat': this.taxRecord.distance_sales_total_vat,
                    'gross': this.taxRecord.distance_sales_total_gross,
                }
            ]
        },

        itemsNonTaxableDistanceSales() {
            return [
                {
                    'itemName': 'Sales',
                    'net': this.taxRecord.non_taxable_distance_sales_sales_net,
                    'vat': this.taxRecord.non_taxable_distance_sales_sales_vat,
                    'gross': this.taxRecord.non_taxable_distance_sales_sales_gross,
                },
                {
                    'itemName': 'Refunds',
                    'net': this.taxRecord.non_taxable_distance_sales_refunds_net,
                    'vat': this.taxRecord.non_taxable_distance_sales_refunds_vat,
                    'gross': this.taxRecord.non_taxable_distance_sales_refunds_gross,
                },
                {
                    'itemName': 'Total',
                    'net': this.taxRecord.non_taxable_distance_sales_total_net,
                    'vat': this.taxRecord.non_taxable_distance_sales_total_vat,
                    'gross': this.taxRecord.non_taxable_distance_sales_total_gross,
                }
            ]
        },

        itemsIntraCommunitySales() {
            return [
                {
                    'itemName': 'Sales',
                    'net': this.taxRecord.intra_community_sales_sales_net,                },
                {
                    'itemName': 'Refunds',
                    'net': this.taxRecord.intra_community_sales_refunds_net,
                },
                {
                    'itemName': 'Total',
                    'net': this.taxRecord.intra_community_sales_total_net,
                }
            ]
        },

        itemsExports() {
            return [
                {
                    'itemName': 'Sales',
                    'net': this.taxRecord.exports_sales_net
                },
                {
                    'itemName': 'Refunds',
                    'net': this.taxRecord.exports_refunds_net
                },
                {
                    'itemName': 'Total',
                    'net': this.taxRecord.exports_total_net
                }
            ]
        },

        itemsIntraCommunityAcquisitions() {
            return [
                {
                    'itemName': 'Acquisitions',
                    'net': this.taxRecord.ica_acquisitions_net,
                    'reverseChargeVat': this.taxRecord.ica_acquisitions_reverse_charge_vat
                },
                {
                    'itemName': 'Refunds',
                    'net': this.taxRecord.ica_refunds_net,
                    'reverseChargeVat': this.taxRecord.ica_refunds_reverse_charge_vat
                },
                {
                    'itemName': 'Total',
                    'net': this.taxRecord.ica_total_net,
                    'reverseChargeVat': this.taxRecord.ica_total_reverse_charge_vat
                }
            ]
        },

        itemsLocalAcquisitions() {
            return [
                {
                    'itemName': 'Acquisitions',
                    'net': this.taxRecord.local_acquisitions_acquisitions_net,
                    'vat': this.taxRecord.local_acquisitions_acquisitions_vat,
                    'gross': this.taxRecord.local_acquisitions_acquisitions_gross,
                },
                {
                    'itemName': 'Refunds',
                    'net': this.taxRecord.local_acquisitions_refunds_net,
                    'vat': this.taxRecord.local_acquisitions_refunds_vat,
                    'gross': this.taxRecord.local_acquisitions_refunds_gross,
                },
                {
                    'itemName': 'Total',
                    'net': this.taxRecord.local_acquisitions_total_net,
                    'vat': this.taxRecord.local_acquisitions_total_vat,
                    'gross': this.taxRecord.local_acquisitions_total_gross,
                }
            ]
        }
    }

}
</script>

<style>

</style>
