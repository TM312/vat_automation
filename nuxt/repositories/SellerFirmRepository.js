const resource = '/business/seller_firm'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}/`)
    },

    create(payload) {
        return $axios.post(`${resource}/`, payload)
    },

    get_by_public_id(seller_firm_public_id) {
        return $axios.get(`${resource}/${seller_firm_public_id}`)
        // return $axios.get(`/business/seller_firm/${seller_firm_public_id}`)
    },

    update(seller_firm_id, payload) {
        return $axios.put(`${resource}/${seller_firm_id}`, payload)
    },

    delete_by_id(seller_firm_id) {
        return $axios.delete(`${resource}/${seller_firm_id}`)
    },

    upload(payload) {
        return $axios.post(`${resource}/csv`, payload)
    }
})
