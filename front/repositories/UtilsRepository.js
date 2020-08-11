const resource = '/utils'
export default ($axios) => ({

    get_by_seller_firm_public_id() {
        return $axios.get(`${resource}/notifications/key_accounts`)
    }
})
