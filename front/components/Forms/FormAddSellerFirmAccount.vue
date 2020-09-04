<template>
    <b-card bg-variant="white">
        <b-form-group
            label-cols-lg="3"
            label="New Account"
            label-size="lg"
            label-class="font-weight-bold pt-0"
            class="mb-2"
        >
            <b-form-group
                label-cols-sm="3"
                label-align-sm="right"
                label-for="channel_code"
                label="Channel"
            >
                <b-form-select v-if="$fetchState.pending" id="channel_code" disabled />
                <b-form-select
                    v-else
                    id="channel_code"
                    :options="optionsChannelCode"
                    v-model="payload.channel_code"
                ></b-form-select>
            </b-form-group>

            <b-form-group
                label-cols-sm="3"
                label-align-sm="right"
                label-for="given_id"
                label="Account ID"
            >
                <b-form-input
                    id="given_id"
                    type="text"
                    v-model="payload.given_id"
                    class="mt-1"
                ></b-form-input>
            </b-form-group>

        </b-form-group>


        <b-button
                variant="primary"
                @click="submitPayload()"
                :disabled="validation_submit"
                block
            >
                <b-icon icon="box-arrow-in-up" /> Add New Account
        </b-button>
    </b-card>
</template>

<script>
    import { mapState } from "vuex";

    export default {
        name: 'FormAddSellerFirmAccount',

        data() {
            return {
                payload: {
                    channel_code: null,
                    given_id: null,
                },
            }
        },

        async fetch() {
            if (this.channels.length == 0) {
                const { store } = this.$nuxt.context;
                await store.dispatch("channel/get_all");
            }
        },

        computed: {
            ...mapState({
                channels: state => state.channel.channels
            }),

            optionsChannelCode() {
                let options = this.channels.map(channel => {
                    let properties = {
                        value: channel.code,
                        text: channel.code
                    };
                    return properties;
                });
                return options;
            },

            validation_submit() {
                if (
                    this.payload.channel_code !== null &&
                    this.payload.channel_code !== '' &&
                    this.payload.given_id !== null &&
                    this.payload.given_id !== ''

                ) {
                    return false;
                } else {
                    return true;
                }
            }
        },

        methods: {
            async submitPayload() {
                try {
                    await this.create_by_seller_firm_public_id();

                    this.payload.channel_code = null;
                    this.payload.given_id = null;

                    await this.$store.dispatch(
                        "seller_firm/get_by_public_id",
                        this.$route.params.public_id
                    );
                    this.$emit('flash')
                    await this.$toast.success('New account succesfully added.', {
                        duration: 5000
                    });
                } catch (error) {
                    this.$toast.error(error, { duration: 5000 });
                }
            },

            async create_by_seller_firm_public_id() {
                const data_array = [this.$route.params.public_id, this.payload]

                await this.$store.dispatch(
                    "account/create_by_seller_firm_public_id",
                    data_array
                );
            },
        }
    }
</script>

<style>

</style>
