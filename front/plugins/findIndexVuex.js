import Vue from 'vue'

Vue.mixin({
    methods: {
        findIndex(values, expectedValue){
            let selectedIndex;
            const valuePresent = values.some((value, index) => {
                selectedIndex = index;
                return value === expectedValue;
            });
            return valuePresent ? selectedIndex : -1;
        }
    }
})
