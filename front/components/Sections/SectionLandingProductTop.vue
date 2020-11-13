<template>
  <section id="landing-product-top">
    <div class="diagonal-box">
      <div class="content">
        <b-row cols="1" cols-md="2">
          <b-col>
            <b-jumbotron
              header="Infrastructure to run your ecommerce business successfully"
              class="text-right ml-auto"
              style="max-width: 60rem"
              bg-variant="transparent"
              text-variant="dark"
            >
              <template #lead style="max-width: 40rem" class="mt-5">
                Tax-Automation provides Amazon sellers with the tools to manage their business and meet their vat requirements across Europe.
                We assist you with the registration and your preliminary turnover tax returns.
                Use our platform to keep track of your sales and all relevant distance selling thresholds.
              </template>
            </b-jumbotron>
          </b-col>
          <b-col>
            <h2>jasdk</h2>
          </b-col>
        </b-row>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "SectionLandingProductTop",
}
</script>

<style>
    .diagonal-box {
        width: 100%;
        height: 100%;
        background: linear-gradient(-45deg, #eecf8e, #c26c52, #eb6095, rgb(69, 149, 180), #66b39d);
        background-size: 400% 400%;
        animation: change 120s ease-in-out infinite;
        transform: skewY(-11deg);


    }

/*
    #landing-product-top {
        width: 100%;
        height: 100%;
        background: linear-gradient(-45deg, #eecf8e, #c26c52, #eb6095, rgb(69, 149, 180), #66b39d);
        background-size: 400% 400%;
        animation: change 120s ease-in-out infinite;
    } */

    @keyframes change {
        0%{
            background-position: 0 50%;
        }
        50%{
            background-position: 100% 50%;
        }
        100%{
            background-position: 0 50%;
        }
    }

     .content {
        position: relative;
        transform: skewY(11deg);
    }

</style>
