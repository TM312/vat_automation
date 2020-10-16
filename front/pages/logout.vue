<template>
  <b-container>
    <b-row class="my-5">
      <b-col align-self="center">
        <b-jumbotron header="See you next time!" lead="This is a beta version of our upcoming service for e-commerce sellers.">
          <div class="my-5">
            <p>For more information, get in contact: </p>
            <code class="text-primary">
              Dr. Thomas Moellers<br />
              tmoellers@protonmail.ch
            </code>
          </div>
        </b-jumbotron>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  middleware: 'guest',
}
</script>
