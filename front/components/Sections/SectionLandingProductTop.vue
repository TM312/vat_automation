<template>
  <section id="landing-product-top">
    <div class="diagonal-box">
      <div class="content">
        <b-row cols="1" cols-lg="2">
          <b-col>
            <b-jumbotron
              header="VAT Compliance For Your Amazon Business"
              class="text-right ml-auto"
              style="max-width: 60rem"
              bg-variant="transparent"
              text-variant="dark"
            >
              <template
                #lead
                style="max-width: 40rem"
                class="mt-5 text-muted"
              >
                We provide Amazon sellers with
                tools to meet VAT requirements across
                Europe. We assist with VAT registration and
                preliminary turnover tax returns. Keep track of sales and all
                relevant distance selling thresholds through our advanced
                platform.
              </template>

              <button-enter-arrow-right to="/vat-compliance" content="Learn More" />
            </b-jumbotron>
          </b-col>
          <b-col cols="auto">
            <b-img
              rounded
              src="@/assets/img/product/company_overview.png"
              class="product-image"
            />
          </b-col>
        </b-row>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "SectionLandingProductTop"
}
</script>

<style scoped>


    .product-container {
        display: inline-block;

        border-radius: 5px;
        /* background:rgba(193, 194, 207, 0.4); */
    }


    .product-image {
        opacity: 0.95;
        height: 100%;
        width: auto;
        height: 40rem;
        /* background-color: #ffffff; */
        /* border-radius: 5px; */
        background: rgba(136, 139, 139, 0.1);
    }

    .diagonal-box {
        width: 100%;
        height: 100%;
        background: linear-gradient(
            -45deg,
            #eecf8e,
            #c26c52,
            #eb6095,
            rgb(69, 149, 180),
            #a166b3
        );
        background-size: 300% 300%;
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
        0% {
            background-position: 0 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0 50%;
        }
    }

    .content {
        position: relative;
        transform: skewY(11deg);
    }
</style>
