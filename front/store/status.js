export const state = () => ({
    account_targets: [],
    item_targets: [],
    vat_number_targets: [],
    distance_sale_targets: [],
    transaction_input_targets: [],
    seller_firm_targets: [],
    file_targets: [],

    tax_record_target: [],
    tax_record_targets: [],

    account_target_index: [],
    item_target_index: [],
    vat_number_target_index: [],
    distance_sale_target_index: [],
    transaction_input_target_index: [],
    seller_firm_target_index: [],
    file_target_index: [],

    account_targets_done: [],
    item_targets_done: [],
    vat_number_targets_done: [],
    distance_sale_targets_done: [],
    transaction_input_targets_done: [],
    seller_firm_targets_done: [],
    file_targets_done: [],

    account_totals: [],
    item_totals: [],
    vat_number_totals: [],
    distance_sale_totals: [],
    transaction_input_totals: [],
    seller_firm_totals: [],
    file_totals: [],

})


export const getters = {

    doneStatusAccountTargets: state => state.account_targets_done.length > 0 ? state.account_targets_done.every(value => value.done === true) : false,
    doneStatusItemTargets: state => state.item_targets_done.length > 0 ? state.item_targets_done.every(value => value.done === true): false,
    doneStatusVatNumberTargets: state => state.vat_number_targets_done.length > 0 ? state.vat_number_targets_done.every(value => value.done === true) : false,
    doneStatusDistanceSaleTargets: state => state.distance_sale_targets_done.length > 0 ? state.distance_sale_targets_done.every(value => value.done === true) : false,
    doneStatusTransactionInputTargets: state => state.transaction_input_targets_done.length > 0 ? state.transaction_input_targets_done.every(value => value.done === true) : false,
    doneStatusSellerFirmTargets: state => state.seller_firm_targets_done.length > 0 ? state.seller_firm_targets_done.every(value => value.done === true) : false,
    doneStatusFileTargets: state => state.file_targets_done.length > 0 ? state.file_targets_done.every(value => value.done === true) : false,

    totalStatusAccountTargets: state  => state.account_totals.length === 0 ? 0 : state.account_totals.reduce((a, b) => a + b.total, 0),
    totalStatusItemTargets: state  => state.item_totals.length === 0 ? 0 : state.item_totals.reduce((a, b) => a + b.total, 0),
    totalStatusVatNumberTargets: state  => state.vat_number_totals.length === 0 ? 0 : state.vat_number_totals.reduce((a, b) => a + b.total, 0),
    totalStatusDistanceSaleTargets: state  => state.distance_sale_totals.length === 0 ? 0 : state.distance_sale_totals.reduce((a, b) => a + b.total, 0),
    totalStatusTransactionInputTargets: state  => state.transaction_input_totals.length === 0 ? 0 : state.transaction_input_totals.reduce((a, b) => a + b.total, 0),
    totalStatusSellerFirmTargets: state  => state.seller_firm_totals.length === 0 ? 0 : state.seller_firm_totals.reduce((a, b) => a + b.total, 0),
    totalStatusFileTargets: state  => state.file_totals.length === 0 ? 0 : state.file_totals.reduce((a, b) => a + b.total, 0),



    /*eslint-disable */
}
// mutations: receive the state as the first argumen, you can pass an additional argument to store.commit, which is called the payload for the mutation
export const mutations = {

    // considering reactive property: https://stackoverflow.com/questions/51149729/updating-state-of-vuex-array-when-one-item-has-some-changes/51153076
    SET_ACCOUNT_TARGET(state, payload) {
        Object.assign(state.account_targets[payload.index], payload.status);
    },
    SET_ITEM_TARGET(state, payload) {
        Object.assign(state.item_targets[payload.index], payload.status);
    },
    SET_VAT_NUMBER_TARGET(state, payload) {
        Object.assign(state.vat_number_targets[payload.index], payload.status);
    },
    SET_DISTANCE_SALE_TARGET(state, payload) {
        Object.assign(state.distance_sale_targets[payload.index], payload.status);
    },

    SET_TRANSACTION_INPUT_TARGET(state, payload) {
        Object.assign(state.transaction_input_targets[payload.index], payload.status);
    },

    SET_SELLER_FIRM_TARGET(state, payload) {
        Object.assign(state.seller_firm_targets[payload.index], payload.status);
    },

    SET_FILE_TARGET(state, payload) {
        Object.assign(state.file_targets[payload.index], payload.status);
    },



    SET_ACCOUNT_TARGET_DONE(state, payload) {
        const payload_done = { done: payload.done }
        Object.assign(state.account_targets_done[payload.index], payload_done);
    },

    SET_ITEM_TARGET_DONE(state, payload) {
        const payload_done = { done: payload.done }
        Object.assign(state.item_targets_done[payload.index], payload_done);
    },

    SET_VAT_NUMBER_TARGET_DONE(state, payload) {
        const payload_done = { done: payload.done }
        Object.assign(state.vat_number_targets_done[payload.index], payload_done);
    },

    SET_DISTANCE_SALE_TARGET_DONE(state, payload) {
        const payload_done = { done: payload.done }
        Object.assign(state.distance_sale_targets_done[payload.index], payload_done);
    },

    SET_TRANSACTION_INPUT_TARGET_DONE(state, payload) {
        const payload_done = { done: payload.done }
        Object.assign(state.transaction_input_targets_done[payload.index], payload_done);
    },

    SET_SELLER_FIRM_TARGET_DONE(state, payload) {
        const payload_done = { done: payload.done }
        Object.assign(state.seller_firm_targets_done[payload.index], payload_done);
    },

    SET_FILE_TARGET_DONE(state, payload) {
        const payload_done = { done: payload.done }
        Object.assign(state.file_targets_done[payload.index], payload_done);
    },


    PUSH_ACCOUNT_TARGET(state, payload) {
        state.account_targets.push(payload)
    },

    PUSH_ITEM_TARGET(state, payload) {
        state.item_targets.push(payload)
    },

    PUSH_VAT_NUMBER_TARGET(state, payload) {
        state.vat_number_targets.push(payload)
    },

    PUSH_DISTANCE_SALE_TARGET(state, payload) {
        state.distance_sale_targets.push(payload)
    },

    PUSH_TRANSACTION_INPUT_TARGET(state, payload) {
        state.transaction_input_targets.push(payload)
    },

    PUSH_SELLER_FIRM_TARGET(state, payload) {
        state.seller_firm_targets.push(payload)
    },

    PUSH_FILE_TARGET(state, payload) {
        state.file_targets.push(payload)
    },

    PUSH_TAX_RECORD_TARGET(state, payload) {
        state.tax_record_targets.push(payload)
    },




    PUSH_ACCOUNT_TARGET_INDEX(state, payload) {
        state.account_target_index.push(payload)
    },

    PUSH_ITEM_TARGET_INDEX(state, payload) {
        state.item_target_index.push(payload)
    },

    PUSH_VAT_NUMBER_TARGET_INDEX(state, payload) {
        state.vat_number_target_index.push(payload)
    },

    PUSH_DISTANCE_SALE_TARGET_INDEX(state, payload) {
        state.distance_sale_target_index.push(payload)
    },

    PUSH_TRANSACTION_INPUT_TARGET_INDEX(state, payload) {
        state.transaction_input_target_index.push(payload)
    },

    PUSH_SELLER_FIRM_TARGET_INDEX(state, payload) {
        state.seller_firm_target_index.push(payload)
    },

    PUSH_FILE_TARGET_INDEX(state, payload) {
        state.file_target_index.push(payload)
    },




    PUSH_ACCOUNT_TARGET_DONE(state, payload) {
        state.account_targets_done.push(payload)
    },

    PUSH_ITEM_TARGET_DONE(state, payload) {
        state.item_targets_done.push(payload)
    },

    PUSH_VAT_NUMBER_TARGET_DONE(state, payload) {
        state.vat_number_targets_done.push(payload)
    },

    PUSH_DISTANCE_SALE_TARGET_DONE(state, payload) {
        state.distance_sale_targets_done.push(payload)
    },

    PUSH_TRANSACTION_INPUT_TARGET_DONE(state, payload) {
        state.transaction_input_targets_done.push(payload)
    },

    PUSH_SELLER_FIRM_TARGET_DONE(state, payload) {
        state.seller_firm_targets_done.push(payload)
    },

    PUSH_FILE_TARGET_DONE(state, payload) {
        state.file_targets_done.push(payload)
    },



    PUSH_ACCOUNT_TOTALS(state, payload) {
        state.account_totals.push(payload)
    },

    PUSH_ITEM_TOTALS(state, payload) {
        state.item_totals.push(payload)
    },

    PUSH_VAT_NUMBER_TOTALS(state, payload) {
        state.vat_number_totals.push(payload)
    },

    PUSH_DISTANCE_SALE_TOTALS(state, payload) {
        state.distance_sale_totals.push(payload)
    },

    PUSH_TRANSACTION_INPUT_TOTALS(state, payload) {
        state.transaction_input_totals.push(payload)
    },

    PUSH_SELLER_FIRM_TOTALS(state, payload) {
        state.seller_firm_totals.push(payload)
    },

    PUSH_FILE_TOTALS(state, payload) {
        state.file_totals.push(payload)
    },


    CLEAR_ALL(state) {
        state.account_targets = []
        state.item_targets = []
        state.vat_number_targets = []
        state.distance_sale_targets = []
        state.transaction_input_targets = []
        state.seller_firm_targets = []
        state.file_targets = []
        state.tax_record_targets = []

        state.account_target_index = []
        state.item_target_index = []
        state.vat_number_target_index = []
        state.distance_sale_target_index = []
        state.transaction_input_target_index = []
        state.seller_firm_target_index = []
        state.file_target_index = []

        state.account_targets_done = []
        state.item_targets_done = []
        state.vat_number_targets_done = []
        state.distance_sale_targets_done = []
        state.transaction_input_targets_done = []
        state.seller_firm_targets_done = []
        state.file_targets_done = []

        state.account_totals = []
        state.item_totals = []
        state.vat_number_totals = []
        state.distance_sale_totals = []
        state.transaction_input_totals = []
        state.seller_firm_totals = []
        state.file_totals = []
    },

    CLEAR_STATUS_ACCOUNT_TARGETS(state) {
        state.account_targets = []
        state.account_target_index = []
        state.account_targets_done = []
        state.account_totals = []
    },
    CLEAR_STATUS_ITEM_TARGETS(state) {
        state.item_targets = []
        state.item_target_index = []
        state.item_targets_done = []
        state.item_totals = []
    },
    CLEAR_STATUS_VAT_NUMBER_TARGETS(state) {
        state.vat_number_targets = []
        state.vat_number_target_index = []
        state.vat_number_targets_done = []
        state.vat_number_totals = []
    },
    CLEAR_STATUS_DISTANCE_SALE_TARGETS(state) {
        state.distance_sale_targets = []
        state.distance_sale_target_index = []
        state.distance_sale_targets_done = []
        state.distance_sale_totals = []
    },
    CLEAR_STATUS_TRANSACTION_INPUT_TARGETS(state) {
        state.transaction_input_targets = []
        state.transaction_input_target_index = []
        state.transaction_input_targets_done = []
        state.transaction_input_totals = []
    },
    CLEAR_STATUS_SELLER_FIRM_TARGETS(state) {
        state.seller_firm_targets = []
        state.seller_firm_target_index = []
        state.seller_firm_targets_done = []
        state.seller_firm_totals = []
    },
    CLEAR_STATUS_FILE_TARGETS(state) {
        state.file_targets = []
        state.file_target_index = []
        state.file_targets_done = []
        state.file_totals = []
    },

    CLEAR_STATUS_TAX_RECORD_TARGETS(state) {
        state.tax_record_targets = []
        state.tax_record_target = []
    },

    POP_STATUS_TAX_RECORD_TARGETS(state) {
        state.tax_record_target = state.tax_record_targets.pop()
    }
}


export const actions = {
    async clear_all({ commit }) {
        commit('CLEAR_ALL')
    },

    async handle_status({ commit, state }, status) {

        const payload_target = { target: status.target }
        const payload_total = { total: status.total }
        const payload_done_false = { done: false }

        if (status.object === 'account') {
            var index = state.account_target_index.findIndex(e => e.target === status.target)
        } else if (status.object === 'item') {
            var index = state.item_target_index.findIndex(e => e.target === status.target)
        } else if (status.object === 'distance_sale') {
            var index = state.distance_sale_target_index.findIndex(e => e.target === status.target)
        } else if (status.object === 'vat_number') {
            var index = state.vat_number_target_index.findIndex(e => e.target === status.target)
        } else if (status.object === 'transaction_input') {
            var index = state.transaction_input_target_index.findIndex(e => e.target === status.target)
        } else if (status.object === 'seller_firm') {
            var index = state.seller_firm_target_index.findIndex(e => e.target === status.target)
        } else if(status.object === 'file') {
        var index = state.file_target_index.findIndex(e => e.target === status.target)
        }

        const upperObject = status.object.toUpperCase()

        if (status.object === 'tax_record') {
            // simple push
            commit(`PUSH_${upperObject}_TARGET`, status)
        } else {
            if (index === -1) {
                commit(`PUSH_${upperObject}_TARGET`, status)
                commit(`PUSH_${upperObject}_TARGET_INDEX`, payload_target)
                commit(`PUSH_${upperObject}_TOTALS`, payload_total)

                if (!status.done) {
                    commit(`PUSH_${upperObject}_TARGET_DONE`, payload_done_false)
                }
            } else {
                const payload_object = { status: status, index: index }
                commit(`SET_${upperObject}_TARGET`, payload_object)
            }

            if (status.done) {
                if (index === -1) {
                    const payload_push_done = { done: true }
                    commit(`PUSH_${upperObject}_TARGET_DONE`, payload_push_done)
                } else {
                    const payload_set_done = { done: true, index: index }
                    commit(`SET_${upperObject}_TARGET_DONE`, payload_set_done)
                }
            }
        }
    }
}
