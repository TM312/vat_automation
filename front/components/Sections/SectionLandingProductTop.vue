<template>
  <section id="landing-product-top">
    <div class="diagonal-box">
      <div class="content">
        <b-row cols="1" cols-lg="2">
          <b-col>
            <div>
              <div class="ml-auto" style="max-width: 60rem">
                <p class="hero-text text-dark text-right">
                  VAT Calculations For Your <span style="color: #cfd9de">Amazon Business </span>
                </p>
              </div>
              <!-- <b-jumbotron
              header="VAT Calculations For Your Amazon Business Across Europe"
              class="text-right ml-auto"
              style="max-width: 60rem"
              bg-variant="transparent"
              text-variant="dark"
            > -->
              <!-- <template
                #lead
                style="max-width: 40rem"
                class="mt-5 text-muted"
              >
                We provide Amazon sellers with
                tools to meet VAT requirements across
                Europe. We assist with the calculation of preliminary turnover tax returns, keeping track of sales and all
                relevant distance selling thresholds.
              </template> -->
              <div style="float: right; max-width: 40rem">
                <p class="lead mt-5 text-dark text-right">
                  We provide Amazon sellers with
                  tools to meet VAT requirements across
                  Europe. Our platform facilitates the easy calculation of preliminary turnover tax returns and to keep track of sales and all
                  relevant distance selling thresholds.
                </p>

                <button-enter-arrow-right to="/vat-compliance" style="float: right" content="Learn More" />
              </div>
            <!-- </b-jumbotron> -->
            </div>
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

    mark.red {
            color: #ff0000;
            background: none;
    }

    .hero-text {
        font-size: 4.5rem;
        text-align: end;
    }


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
        background: linear-gradient(-45deg, rgb(253, 200, 48), rgb(243, 115, 53));
        /* linear-gradient(-45deg, rgb(167, 112, 239), rgb(207, 139, 243), rgb(253, 185, 155)); */
        /* linear-gradient(-45deg, rgb(198, 255, 221), rgb(251, 215, 134), rgb(247, 121, 125)); */
        /* linear-gradient(
            -45deg,
            #eecf8e,
            #c26c52,
            #eb6095,
            rgb(69, 149, 180),
            #a166b3
        ); */


        background-size: 100% 100%;
        /* animation: change 60s ease-in-out infinite; */
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
