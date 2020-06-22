const resource = '/business/seller_firm'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}/`)
    },

    create(payload) {
        return $axios.post(`${resource}/`, payload)
    },

    get_by_id(seller_firm_id) {
        return $axios.get(`${resource}/${seller_firm_id}`)
    },

    update(seller_firm_id, payload) {
        return $axios.put(`${resource}/${seller_firm_id}`, payload)
    },

    delete_by_id(seller_firm_id) {
        return $axios.delete(`${resource}/${seller_firm_id}`)
    },

    get_clients() {
        return $axios.get(`${resource}/as_client`)
    },

    upload(payload) {
        return $axios.post(`${resource}/csv`, payload)
    }
})
