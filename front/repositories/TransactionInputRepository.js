const resource = '/transaction_input'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}/`)
    },

    get_by_public_id(transaction_input_public_id) {
        return $axios.get(`${resource}/${transaction_input_public_id}`)
    },

    get_by_bundle_public_id(bundle_public_id) {
        return $axios.get(`${resource}/bundle/${bundle_public_id}`)
    },

    delete_all() {
        return $axios.delete(`${resource}/`)
    },

    get_by_seller_firm_public_id(params) {
        return $axios.get(`${resource}/seller_firm/`, {params})
    },

    update_by_public_id(transaction_input_public_id, payload) {
        return $axios.put(`${resource}/${transaction_input_public_id}`, payload)
    },

    delete_by_public_id(transaction_input_public_id) {
        return $axios.delete(`${resource}/${transaction_input_public_id}`)
    },

    upload(payload) {
        return $axios.post(`${resource}/csv`, payload)
    }
})
