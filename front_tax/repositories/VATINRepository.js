const resource = '/tax/vatin'
export default ($axios) => ({
  get_all() {
    return $axios.get(`${resource}/`)
  },

  create(payload) {
    return $axios.post(`${resource}/`, payload)
  },

  create_by_seller_firm_public_id(seller_firm_public_id, payload) {
    return $axios.post(`${resource}/seller_firm/${seller_firm_public_id}`, payload)
  },

  get_by_id(vatin_id) {
    return $axios.get(`${resource}/${vatin_id}`)
  },

  verify(payload) {
    return $axios.post(`${resource}/verify`, payload)
  },

  validate(payload) {
    return $axios.post(`${resource}/validate`, payload)
  },

  update_by_public_id(vatin_public_id, payload) {
    return $axios.put(`${resource}/${vatin_public_id}`, payload)
  },

  delete_by_id(vatin_id) {
    return $axios.delete(`${resource}/${vatin_id}`)
  },

  delete_by_public_id(vatin_public_id) {
    return $axios.delete(`${resource}/${vatin_public_id}`)
  },

  upload(payload) {
    return $axios.post(`${resource}/csv`, payload)
  }
})
