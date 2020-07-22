<template>
    <div>
        <b-button
            :variant="buttonVariant"
            pill
            size="sm"
            @click="followSellerFirm"
            :disabled="buttonBusy"
        >{{ buttonText }}</b-button>
    </div>
</template>

<script>

    export default {
        name: "ButtonFollowSellerFirm",
        props: {
            sellerFirm: {
                type: [Array, Object],
                required: true
            }
        },

        data() {
            return {
                buttonBusy: false
            }
        },

        computed: {
            isFollowing() {
                return this.$auth.user.key_accounts.some(el => (el.public_id === this.sellerFirm.public_id ) )
            },

            buttonText() {
                return this.isFollowing ? 'Following' : 'Follow'
            },

            buttonVariant() {
                return this.isFollowing ? 'success' : 'outline-success'
            }
        },
        methods: {
            async followSellerFirm() {
                this.buttonBusy = true
                const { store } = this.$nuxt.context
                await store.dispatch("tax_auditor/follow_unfollow", this.sellerFirm.public_id)

                await this.$auth.fetchUser()
                this.buttonBusy = false
            }
        },
    };
</script>

<style>
</style>
