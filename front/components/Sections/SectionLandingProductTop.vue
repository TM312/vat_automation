<template>
  <section id="landing-product-top">
    <div class="diagonal-box">
      <div class="content">
        <b-row cols="1" cols-md="2">
          <b-col>
            <b-jumbotron
              header="Vat Compliance For Your E-commerce Business"
              class="text-right ml-auto"
              style="max-width: 60rem"
              bg-variant="transparent"
              text-variant="dark"
            >
              <template #lead style="max-width: 40rem" class="mt-5">
                Tax-Automation provides Amazon sellers with the tools to meet their vat requirements across Europe.
                We assist with the vat registration and preliminary turnover tax returns.
                Our platform allows to keep track of sales and all relevant distance selling thresholds.
              </template>

              <b-button pill variant="outline-primary" @mouseover="buttonHover = true" @mouseleave="buttonHover = false">
                Product Details
                <b-icon :icon="buttonHover ? 'arrow-right' : 'chevron-right'" class="ml-1" />
              </b-button>
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

  data() {
    return {
      buttonHover: false
    }
  },
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
