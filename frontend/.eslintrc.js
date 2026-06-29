module.exports = {
  env: { browser: true, es2021: true, jest: true },
  globals: { process: "readonly" },
  extends: ["eslint:recommended", "plugin:react/recommended"],
  parserOptions: { ecmaVersion: "latest", sourceType: "module" },
  rules: {
    "react/prop-types": "off",
    "no-unused-vars": ["error", { "vars": "all", "args": "none" }]
  }
};