const resource = '/utils'
export default ($axios) => ({
    get_all_key_account_notifications(params) {
        return $axios.get(`${resource}/notifications/key_accounts/` { params })
    }
})
