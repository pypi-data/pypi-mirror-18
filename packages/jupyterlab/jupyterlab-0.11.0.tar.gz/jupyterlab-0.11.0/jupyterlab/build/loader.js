// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
var loader_1 = require('@jupyterlab/extension-builder/lib/loader');
/**
 * A module loader instance.
 */
exports.loader = new loader_1.ModuleLoader();
/**
 * Define a module that can be synchronously required.
 *
 * @param path - The version-mangled fully qualified path of the module.
 *   For example, "foo@1.0.1/lib/bar/baz.js".
 *
 * @param callback - The callback function for invoking the module.
 */
function define(path, callback) {
    exports.loader.define.call(exports.loader, path, callback);
}
exports.define = define;
//# sourceMappingURL=loader.js.map