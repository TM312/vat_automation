<template>
<b-container fluid>
    <div class="mt-5">
      <b-table
        striped
        hover
        :items="files"
        :fields="fields"
      >
        <template v-slot:cell(#)="data">
          {{ data.index + 1 }}
        </template>

        <template v-slot:cell(platform)>
          <p>Amazon</p>
          <!-- <b-form-select v-model="selected" :options="options"></b-form-select> -->
        </template>

        <template v-slot:cell(keep?)="data">
          <b-button
            size="sm"
            variant="outline-danger"
            class="remove-file"
            @click="removeFile(data.index)"
          >
            <b-icon icon="trash" />
          </b-button>
        </template>
      </b-table>
    </div>
    <div class="my-5">
      <b-button
        variant="primary"
        @click="uploadFiles"
      >
        <b-icon icon="box-arrow-in-right" />
        Upload Files
      </b-button>
    </div>
</b-container>

</template>

<script>
export default {

}
</script>

<style>

</style>
