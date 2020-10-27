const resource = '/tax/vat_threshold'
export default ($axios) => ({
  get_all() {
    return $axios.get(`${resource}/`)
  },

  create(payload) {
    return $axios.post(`${resource}/`, payload)
  },

  get_by_public_id(vat_threshold_public_id) {
    return $axios.get(`${resource}/${vat_threshold_public_id}`)
  },

  update(vat_threshold_public_id, payload) {
    return $axios.put(`${resource}/${vat_threshold_public_id}`, payload)
  },

  delete_by_public_id(vat_threshold_public_id) {
    return $axios.delete(`${resource}/${vat_threshold_public_id}`)
  }

})
