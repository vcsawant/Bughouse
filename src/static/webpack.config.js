const webpack = require('webpack')
const config = {
  entry: {
    index: __dirname + '/js/index.jsx',
    login: __dirname + '/js/login.jsx',
    register: __dirname + '/js/register.jsx',
    game: __dirname + '/js/game.jsx'
  },
  output: {
    path: __dirname + '/dist',
    filename: '[name]-bundle.js',
  },
  resolve: {
    extensions: ['.js', '.jsx', '.css'],
  },
  module: {
    rules: [
      {
        test: /\.jsx?/,
        exclude: /node_modules/,
        loader: 'babel-loader',
        options:{
          presets: ['env','react'],
          plugins: ['transform-class-properties']
        }
      },
      {
        test:/\.css$/,
        use:['style-loader','css-loader']
      },
    ],
  },
}
module.exports = config
