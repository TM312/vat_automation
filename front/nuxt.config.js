export default {
    server: {
        port: 3000, // default: 3000
        host: '0.0.0.0' // default: localhost
    },
    mode: 'universal',
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
        '~/plugins/sleep'
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
        '@nuxtjs/proxy',
        '@nuxtjs/auth',
        '@nuxtjs/toast',
        // Doc: https: //github.com/richardeschloss/nuxt-socket-io
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
            'ModalPlugin'
        ],
        components: [
            'BAlert',
            'BAvatar',
            'BAvatarGroup',
            'BBadge',
            'BButton',
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
            'BForm',
            'BFormCheckbox',
            'BFormDatepicker',
            'BFormGroup',
            'BFormInput',
            'BFormInvalidFeedback',
            'BFormValidFeedback',
            'BFormSelect',
            'BFormRow',
            'BModal',
            'BNav',
            'BNavbar',
            'BNavItem',
            'BNavItemDropdown',
            'BNavbarBrand',
            'BNavbarNav',
            'BNavbarToggle',
            'BPopover',
            'BProgress',
            'BProgressBar',
            'BRow',
            'BSpinner',
            'BTable',
            'BTab',
            'BTabs',
            'BToast',
            'BToaster'
        ],
        directives: [
            'VBModal',
            'VBPopover',
            'VBTooltip',
            'VBScrollspy',
            'VBToggle'
        ]
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
            local_tax_auditor: {
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
                        url: 'user/tax_auditor/self',
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
            logout: '/tax/login',
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

    toast: {
        register: [
            // Register custom toasts
            // {
            //   name: 'auth_success',
            //   message: 'Successfully authenticated',
            //   options: {
            //     type: 'success',
            //     theme: 'outline',
            //     duration: 5000,
            //     position: 'top-right'
            //   }
            // }
        ],
    },

    // https://medium.com/javascript-in-plain-english/introduction-to-nuxt-socket-io-b78c5322d389
    io: {
        sockets: [{
            name: 'home',
            url: 'http://127.0.0.1', // nginx reroutes to api
            default: true,
            vuex: {
                mutations: [
                    { new_account: 'seller_firm/PUSH_ACCOUNT' },
                    { new_item: 'seller_firm/PUSH_ITEM' },
                    { new_distance_sale: 'seller_firm/PUSH_DISTANCE_SALE' },
                    { new_vatin: 'seller_firm/PUSH_VAT_NUMBER' },
                    { new_transaction_input: 'transaction_input/PUSH_TRANSACTION_INPUT' }
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
