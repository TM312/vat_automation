const resource = '/country'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}/`)
    },

    create(payload) {
        return $axios.post(`${resource}/`, payload)
    },

    get_by_code(country_code) {
        return $axios.get(`${resource}/${country_code}`)
    },

    update(country_code, payload) {
        return $axios.put(`${resource}/${country_code}`, payload)
    },

    delete_by_code(country_code) {
        return $axios.delete(`${resource}/${country_code}`)
    }

})
