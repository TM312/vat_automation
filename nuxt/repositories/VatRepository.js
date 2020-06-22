const resource = '/tax/vat'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}/`)
    },

    create(payload) {
        return $axios.post(`${resource}/`, payload)
    },

    get_by_id(vat_id) {
        return $axios.get(`${resource}/${vat_id}`)
    },

    update(vat_id, payload) {
        return $axios.put(`${resource}/${vat_id}`, payload)
    },

    delete_by_id(vat_id) {
        return $axios.delete(`${resource}/${vat_id}`)
    }
})
