const resource = '/platform'
export default ($axios) => ({
  get_all() {
    return $axios.get(`${resource}/`)
  },

  create(payload) {
    return $axios.post(`${resource}/`, payload)
  },

  get_by_id(platform_id) {
    return $axios.get(`${resource}/${platform_id}`)
  },

  update(platform_id, payload) {
    return $axios.put(`${resource}/${platform_id}`, payload)
  },

  delete_by_id(platform_id) {
    return $axios.delete(`${resource}/${platform_id}`)
  }
})
