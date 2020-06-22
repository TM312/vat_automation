const resource = '/distance_sale'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}/`)
    },

    create(payload) {
        return $axios.post(`${resource}/`, payload)
    },

    get_by_id(distance_sale_id) {
        return $axios.get(`${resource}/${distance_sale_id}`)
    },

    update(distance_sale_id, payload) {
        return $axios.put(`${resource}/${distance_sale_id}`, payload)
    },

    delete_by_id(distance_sale_id) {
        return $axios.delete(`${resource}/${distance_sale_id}`)
    },

    upload(payload) {
        return $axios.post(`${resource}/csv`, payload)
    }

})
