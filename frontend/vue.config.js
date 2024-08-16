module.exports = {
  pwa: {
    name: 'Pomodoro Timer',
    themeColor: '#4caf50',
    msTileColor: '#4caf50',
    appleMobileWebAppCapable: 'yes',
    appleMobileWebAppStatusBarStyle: 'black',
    manifestOptions: {
      background_color: '#4caf50'
    }
  },
  devServer: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        pathRewrite: { '^/api': '' }
      }
    }
  }
};
