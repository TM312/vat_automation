<template>
    <b-card header="Vat Numbers">
        <b-card-text>
            <h2 v-if="countVatNumbers === 0" class="text-secondary text-center">An Overview of This Company's Vat Numbers Can Be Seen Here Once The Corresponding Data Has Been Uploaded</h2>
            <b-table v-else borderless :items="vat_numbers"></b-table>
        </b-card-text>
    </b-card>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        name: 'CardVatNumbers',
        // eslint-disable-next-line
        // props: { vat_numbers: { type: [Array, Object] } },

        computed: {
            ...mapState({
                vat_numbers: state => state.seller_firm.seller_firm.vat_numbers,
                countVatNumbers() {
                    return this.$store.getters['seller_firm/countVatNumbers']
                },

            }),
        }

    }
</script>
