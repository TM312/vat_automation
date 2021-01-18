const resource = '/business/seller_firm'
export default ($axios) => ({
  get_all() {
    return $axios.get(`${resource}/`)
  },

  get_sample() {
    return $axios.get(`${resource}/sample`)
  },

  create(payload) {
    return $axios.post(`${resource}/`, payload)
  },

  create_as_client(payload) {
    return $axios.post(`${resource}/as_client`, payload)
  },

  get_by_public_id(seller_firm_public_id) {
    return $axios.get(`${resource}/${seller_firm_public_id}`)
    // return $axios.get(`/business/seller_firm/${seller_firm_public_id}`)
  },

  update(seller_firm_public_id, payload) {
    return $axios.put(`${resource}/${seller_firm_public_id}`, payload)
  },

  delete_by_public_id(seller_firm_public_id) {
    return $axios.delete(`${resource}/${seller_firm_public_id}`)
  },

  // upload_create(payload) {
  //     return $axios.post(`${resource}/csv`, payload)
  // }
})
