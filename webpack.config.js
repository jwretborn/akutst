var path = require("path"),
    webpack = require("webpack"),
    ExtractTextPlugin = require("extract-text-webpack-plugin"),
    ManifestRevisionPlugin = require("manifest-revision-webpack-plugin"),
    WebpackCleanupPlugin = require("webpack-cleanup-plugin")

var publicHost = '';
var buildOutputPath = './public';
var root = "./assets"

module.exports = {
    entry: {
        app_js: [
            root + "/scripts/index.js"
        ],
        main_css: [
            root + "/styles/main.scss"
        ]
    },
    output: {
        path : buildOutputPath,
        publicPath: publicHost +"/assets/",
        filename: "[name].[hash].js",
        chunkFilename: "[id].[hash].chunk"
    },
    resolve: {
        extensions: ["", ".js", ".scss"]
    },
    module: {
        loaders: [
            {
                test: /\.js$/i,
                exclude: /node_modules/,
                loader: "babel-loader"
            },
            {
                test: /\.scss$/i,
                loader: ExtractTextPlugin.extract("css!sass")
            }
        ]
    },
    plugins: [
        new ExtractTextPlugin("[name].[chunkhash].css"),
        new ManifestRevisionPlugin("manifest.json", {
            rootAssetPath: root,
            ignorePaths: ["/styles", "/scripts"]
        }),
        new webpack.optimize.UglifyJsPlugin(),
        new webpack.optimize.DedupePlugin(),
        new webpack.DefinePlugin({
            "process.env": {
                NODE_ENV: '"production"'
            }
        }),
        new webpack.NoErrorsPlugin(),
        // Dev, remove unused assets
        new WebpackCleanupPlugin({
            exclude : []
        })
    ]
}