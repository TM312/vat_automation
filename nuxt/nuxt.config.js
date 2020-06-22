export default {
    server: {
        port: 3000, // default: 3000
        host: '0.0.0.0', // default: localhost
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
        '~/plugins/repositories.js'
    ],

    /*
     ** Nuxt.js modules
     */

    buildModules: [
        '@nuxt/components'
    ],

    modules: [
        'bootstrap-vue/nuxt',
        '@nuxtjs/axios',
        '@nuxtjs/proxy',
        '@nuxtjs/auth',
        '@nuxtjs/toast',
    ],
    bootstrapVue: {
        icons: true,
    },

    axios: {
        // proxy: true,
        baseURL: 'http://127.0.0.1:5000',
        /* "94.237.95.140:5000", */
        /* "http://api.tax-automation.com", */
        /*  "http://127.0.0.1:5000"  */
        headers: {
            'Content-Type': 'application/json',
        },
        https: false,
        withCredentials: true,
    },
    auth: {
        strategies: {
            local_seller: {
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
            },
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
            },
        },
        redirect: {
            logout: '/login',
        },
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
        /* ESLint will run on save during npm run dev */
        extend(config, ctx) {
            // Run ESLint on save
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
