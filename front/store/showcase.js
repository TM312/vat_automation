export const state = () => ({
  showcase_accounts: false,
  showcase_distance_sales: false,
  showcase_vat_numbers: false,
  showcase_items: false,
})


export const mutations = {
  SET_SHOWCASE_ACCOUNTS(state) {
    state.showcase_accounts = true
  },
  SET_SHOWCASE_DISTANCE_SALES(state) {
    state.showcase_distance_sales = true
  },
  SET_SHOWCASE_VAT_NUMBERS(state) {
    state.showcase_vat_numbers = true
  },
  SET_SHOWCASE_ITEMS(state) {
    state.showcase_items = true
  },
}
