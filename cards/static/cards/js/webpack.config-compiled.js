"use strict";

module.exports = {
    entry: "./detail.js",
    output: {
        path: __dirname,
        filename: "detail_bundle.js"
    },
    module: {
        loaders: [{ test: /\.css$/, loader: "style!css" }]
    }
};

//# sourceMappingURL=webpack.config-compiled.js.map