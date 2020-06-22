const resource = '/account'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}/`)
    },

    create(payload) {
        return $axios.post(`${resource}/`, payload)
    },

    get_by_id(account_id) {
        return $axios.get(`${resource}/${account_id}`)
    },

    update(account_id, payload) {
        return $axios.put(`${resource}/${account_id}`, payload)
    },

    delete_by_id(account_id) {
        return $axios.delete(`${resource}/${account_id}`)
    },

    upload(payload) {
        return $axios.post(`${resource}/csv`, payload)
    }

})
