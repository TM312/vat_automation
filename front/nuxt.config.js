export default {
    server: {
        port: 14000, // default: 3000
        host: '0.0.0.0' // default: localhost
    },
    /*
     ** Headers of the page
     */
    head: {
        title: 'Tax-Automation.com',
        meta: [
            { charset: 'utf-8' },
            {
                name: 'viewport',
                content: 'width=device-width, initial-scale=1',
            },
            {
                hid: 'description',
                name: 'description',
                content: process.env.npm_package_description || '',
            },
        ],
        link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
    },

    /*
     ** Customize the progress-bar color
     */
    loading: {
        name: 'chasing-dots',
        color: '#ff5638',
        background: 'white',
        height: '4px',
    },

    // https://damienbeaufils.dev/blog/server-sent-events-with-nuxt-js-vue-js-and-nginx-proxy/
    render: {
        gzip: false
    },

    /*
     ** Global CSS
     */
    css: [],

    components: true,

    /*
     ** Plugins to load before mounting the App
     */
    plugins: [
        // '~/plugins/file-system'
        '~/plugins/repositories',
        '~/plugins/sleep',
        '~/plugins/capitalize'
    ],

    /*
     ** Nuxt.js modules
     */

    buildModules: [
        '@nuxt/components',
        '@nuxtjs/date-fns'
    ],

    modules: [
        'bootstrap-vue/nuxt',
        '@nuxtjs/axios',
        '@nuxtjs/auth',
        // '@nuxtjs/toast',
        // Docs: https: //github.com/richardeschloss/nuxt-socket-io
        'nuxt-socket-io'
    ],

    bootstrapVue: {
        icons: true,
        componentPlugins: [
            'LayoutPlugin',
            'FormPlugin',
            'FormCheckboxPlugin',
            'FormInputPlugin',
            'FormRadioPlugin',
            'ToastPlugin',
            'TooltipPlugin',
            'ModalPlugin'
        ],
        components: [
            'BAlert',
            'BAvatar',
            'BAvatarGroup',
            'BBadge',
            'BButton',
            'BButtonGroup',
            'BCard',
            'BCardHeader',
            'BCardFooter',
            'BCardBody',
            'BCardText',
            'BCardTitle',
            'BCardSubTitle',
            'BCardGroup',
            'BCol',
            'BCollapse',
            'BContainer',
            'BDropdown',
            'BDropdownItem',
            'BDropdownHeader',
            'BDropdownDivider',
            'BEmbed',
            'BForm',
            'BFormCheckbox',
            'BFormDatepicker',
            'BFormGroup',
            'BFormInput',
            'BFormInvalidFeedback',
            'BFormValidFeedback',
            'BFormSelect',
            'BFormRow',
            'BFormTextarea',
            'BImg',
            'BJumbotron',
            'BModal',
            'BNav',
            'BNavbar',
            'BNavItem',
            'BNavItemDropdown',
            'BNavbarBrand',
            'BNavbarNav',
            'BNavbarToggle',
            'BPagination',
            'BPopover',
            'BProgress',
            'BProgressBar',
            'BRow',
            'BSidebar',
            'BSkeleton',
            'BSpinner',
            'BTable',
            'BTableLite',
            'BTab',
            'BTabs',
            'BToast',
            'BToaster'
        ],
        directives: [
            'VBModal',
            'VBPopover',
            'VBTooltip',
            'VBToggle'
        ],
        directivePlugins: ['VBScrollspyPlugin']
    },

    axios: {
        // proxy: true,
        baseURL: 'http://127.0.0.1:5000',
        /* "94.237.95.140:5000", */
        /* "http://api.tax-automation.com", */
        /*  "http://127.0.0.1:5000"  */
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': true
        },
        https: false,
        withCredentials: true,
    },

    auth: {
        strategies: {
            local: {
                _scheme: 'local',
                endpoints: {
                    login: {
                        url: '/auth/login',
                        method: 'post',
                        propertyName: 'token',
                    },
                    logout: {
                        url: '/auth/logout',
                        method: 'post',
                    },
                    user: {
                        url: 'user/seller/self',
                        method: 'get',
                        propertyName: 'data',
                    },
                },
                tokenRequired: true,
                tokenType: '',
                sameSite: 'secure'
            },
        },
        redirect: {
            logout: '/login',
        },
        auth: {
            cookie: {
                prefix: 'auth.',
                options: {
                    path: '/'
                }
            }
        }
    },

    // https://medium.com/javascript-in-plain-english/introduction-to-nuxt-socket-io-b78c5322d389
    io: {
        sockets: [{
            name: 'home',
            url: 'http://127.0.0.1', // nginx reroutes to api
            default: true,
            vuex: {
                mutations: [
                    { clear_accounts: 'seller_firm/CLEAR_ACCOUNTS' },
                    { new_account: 'seller_firm/PUSH_ACCOUNT' },
                    { new_accounts: 'seller_firm/PUSH_ACCOUNTS' },

                    { clear_items: 'seller_firm/CLEAR_ITEMS' },
                    { new_item: 'seller_firm/PUSH_ITEM' },
                    { new_items: 'seller_firm/PUSH_ITEMS' },

                    { clear_distance_sales: 'seller_firm/CLEAR_DISTANCE_SALES' },
                    { new_distance_sale: 'seller_firm/PUSH_DISTANCE_SALE' },
                    { new_distance_sales: 'seller_firm/PUSH_DISTANCE_SALES' },

                    { clear_vat_numbers: 'seller_firm/CLEAR_VAT_NUMBERS' },
                    { new_vat_number: 'seller_firm/PUSH_VAT_NUMBER' },
                    { update_vat_number: 'seller_firm/UPDATE_VAT_NUMBER' },
                    { new_vat_numbers: 'seller_firm/PUSH_VAT_NUMBERS' },

                    { clear_transaction_inputs: 'transaction_input/CLEAR_TRANSACTION_INPUTS' },
                    { new_transaction_input: 'transaction_input/PUSH_TRANSACTION_INPUT' },
                    { new_transaction_inputs: 'transaction_input/PUSH_TRANSACTION_INPUTS_DIRECT' },

                    { new_tax_record: 'tax_record/PUSH_TAX_RECORD' }
                ],
                actions: [
                    { status: 'status/handle_status' },
                ]
            }
        }]
    },

    /*
     ** Build configuration
     */
    build: {
        transpile: ['file-system'],
        html: {
            minify: {
                collapseWhitespace: true,
                removeComments: true
            }
        },
        /*
         ** You can extend webpack config here
         */
        extend(config, ctx) {
            // Run ESLint on save
            /* ESLint will run on save during npm run dev */
            if (ctx.isDev && ctx.isClient) {
                config.module.rules.push({
                    enforce: 'pre',
                    test: /\.(js|vue)$/,
                    loader: 'eslint-loader',
                    exclude: /(node_modules)/,
                    options: {
                        fix: true,
                    },
                })
            }

            // Bootstrap
            const vueLoader = config.module.rules.find(rule => rule.loader === 'vue-loader')
            vueLoader.options.transformAssetUrls = {
                video: ['src', 'poster'],
                source: 'src',
                img: 'src',
                image: 'xlink:href',
                'b-avatar': 'src',
                'b-img': 'src',
                'b-img-lazy': ['src', 'blank-src'],
                'b-card': 'img-src',
                'b-card-img': 'src',
                'b-card-img-lazy': ['src', 'blank-src'],
                'b-carousel-slide': 'img-src',
                'b-embed': 'src'
            }
        },
    },
    // generate: {
    //   /* I may not need this due to SSR rendering.
    //    ** The path to the fallback HTML file. It should be set as the error page, so that also unknown routes are rendered via Nuxt.
    //    ** If set to true, the filename will be 404.html
    //    ** If working with statically generated pages then it is recommended to use a 404.html for error pages
    //    */
    //   fallback: true,
    //   routes() {
    //     return axios.get("/users").then(res => {
    //       return res.data.map(user => {
    //         return {
    //           route: "/users  /" + user.public_id,
    //           payload: user
    //         };
    //       });
    //     });
    //   }
    // }
}
