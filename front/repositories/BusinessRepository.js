const resource = '/business'
export default ($axios) => ({
  get_all() {
    return $axios.get(`${resource}/`)
  },

  // create(payload) {
  //     return $axios.post(`${resource}/`, payload)
  // },

  get_by_id(business_id) {
    return $axios.get(`${resource}/${business_id}`)
  },

  update(business_id, payload) {
    return $axios.put(`${resource}/${business_id}`, payload)
  },

  delete_by_id(business_id) {
    return $axios.delete(`${resource}/${business_id}`)
  }
})
