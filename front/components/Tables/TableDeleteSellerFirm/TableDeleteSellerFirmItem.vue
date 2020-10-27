<template>
  <b-table
    borderless
    :items="items"
    :fields="fields"
    hover
    :busy.sync="tableIsBusy"
  >
    <template v-show="editMode===true" v-slot:cell(edit)="data">
      <b-button
        size="sm"
        variant="outline-danger"
        class="remove-entry"
        @click="removeFile(data.index, data.item.public_id)"
      >
        <b-icon icon="trash" />
      </b-button>
    </template>
  </b-table>
</template>
<script>
import { mapState } from "vuex"
export default {
  name: 'TableDeleteSellerFirmItem',

  props: {
    fields: {
      type: [Object, Array],
      required: true
    }
  },

  data() {
    return {
      tableIsBusy: false,
    }
  },

  computed: {
    ...mapState({
      items: state => state.seller_firm.seller_firm.items,
    })
  },

  methods: {
    async removeFile(object, publicId) {
      this.tableIsBusy = true
      try {
        await this.deleteFile(publicId)
        await this.$store.dispatch(
          "seller_firm/get_by_public_id",
          this.$route.params.public_id
        )
        this.tableIsBusy = false
      } catch (error) {
        this.$toast.error(error, { duration: 5000 })
        this.tableIsBusy = false
        return []
      }
    },

    async deleteFile(publicId) {
      await this.$store.dispatch(
        "item/delete_by_public_id",
        publicId
      )
      this.$emit('flash')
    }
  }
}
</script>
