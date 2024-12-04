module.exports = {
  overrides: [
    {
      files: '*.js',
      options: {
        printWidth: 80,
        singleQuote: true,
      },
    },
    {
      files: '*.html',
      options: {
        tabWidth: 2,
      },
    },
    {
      files: '*.css',
      options: {
        singleQuote: true,
      },
    },
  ],
};
