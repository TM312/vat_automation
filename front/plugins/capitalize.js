import Vue from 'vue'

Vue.mixin({
    methods: {
        capitalize(string) {
            return string.toLowerCase()
            .replaceAll("_", " ")
            .replace(/(^\w{1})|(\s{1}\w{1})/g, (match) =>
                match.toUpperCase()
            )
        },
    }
})
