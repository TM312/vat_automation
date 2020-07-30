<template>
    <b-card header="Base Data" :title="seller_firm.name">
        <b-card-text>
            <b>Address:</b> {{ seller_firm.address }} <br>
            <b>Establishment Country:</b> {{ seller_firm.establishment_country }}<br>
            <br>
            <b>Created On:</b> {{ seller_firm.created_on }} <br>
            <b>Created By:</b> {{ seller_firm.created_by }} <br>
            <button-follow-seller-firm :sellerFirm="seller_firm" />
        </b-card-text>
    </b-card>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        name: 'CardClient',
        computed: {
            ...mapState({
                seller_firm: state => state.seller_firm.seller_firm
            }),
        },
    }
</script>
