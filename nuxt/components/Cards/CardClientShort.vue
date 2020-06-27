<template>
    <b-col>
        <b-card :header="business.name">
            <b-card-text>
                <b>Address:</b> {{ business.address  }} <br>
                <b>Created On:</b> {{ business.created_on }} <br>
                <b>Created By:</b> {{ business.created_by }} <br>
                <br>
                <nuxt-link :to="business.public_id" append>
                    Details <b-icon icon="arrow-right" />
                </nuxt-link>
            </b-card-text>
        </b-card>
    </b-col>
</template>

<script>
    import { BIcon } from "bootstrap-vue";

    export default {
        name: 'CardClientShort',
        // eslint-disable-next-line
        props: { business: { type: [Array, Object] } },
        components: {
            BIcon
        }
    }
</script>
