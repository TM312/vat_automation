const resource = '/utils/template'
export default ($axios) => ({

    get_by_name(template_filename) {
        return $axios.get(`${resource}/${template_filename}`)
    }
})
