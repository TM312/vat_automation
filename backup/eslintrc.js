module.exports = {
  env: {
    browser: true,
    es6: true,
    node: true
  },
  extends: [
    "eslint:recommended",
    // https://github.com/vuejs/eslint-plugin-vue#priority-a-essential-error-prevention
    // consider switching to `plugin:vue/strongly-recommended` or `plugin:vue/recommended` for stricter rules.
    "plugin:vue/recommended",
    "plugin:prettier/recommended"
  ],
  globals: {
    Atomics: "readonly",
    SharedArrayBuffer: "readonly"
  },
  parserOptions: {
    ecmaVersion: 2018,
    sourceType: "module",
    parser: "babel-eslint"
  },
  plugins: ["vue"],
  rules: {
    semi: [1, "never"],
    "no-console": "off",
    "vue/max-attributes-per-line": "off",
    "vue/html-self-closing": ["error", {
      "html": {
        "void": "always",
        "normal": "never",
        "component": "always"
      },
      "svg": "always",
      "math": "always"
    }],
    "prettier/prettier": [
      "error",
      {
        semi: false,
        tabWidth: 2,
        singleQuote: true,
        jsxSingleQuote: true,
        bracketSpacing: true
      }
    ]
  }
};
