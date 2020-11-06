const resource = '/currency'
export default ($axios) => ({
  get_all() {
    return $axios.get(`${resource}/`)
  },

  create(payload) {
    return $axios.post(`${resource}/`, payload)
  },

  get_by_code(currency_code) {
    return $axios.get(`${resource}/${currency_code}`)
  },

  update(currency_code, payload) {
    return $axios.put(`${resource}/${currency_code}`, payload)
  },

  delete_by_code(currency_code) {
    return $axios.delete(`${resource}/${currency_code}`)
  }

})
