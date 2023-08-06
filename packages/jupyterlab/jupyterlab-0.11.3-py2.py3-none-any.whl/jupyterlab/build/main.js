// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
var es6_promise_1 = require('es6-promise');
var application_1 = require('../../lib/application');
require('font-awesome/css/font-awesome.min.css');
require('../../lib/default-theme/index.css');
es6_promise_1.polyfill();
/**
 * Create an application object.
 *
 * @param loader - The module loader for the application.
 *
 * @returns A new application object.
 */
function createLab(loader) {
    return new application_1.JupyterLab({
        loader: loader,
        version: require('../../package.json').version,
        gitDescription: process.env.GIT_DESCRIPTION
    });
}
exports.createLab = createLab;
//# sourceMappingURL=main.js.map