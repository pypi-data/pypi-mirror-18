import { JupyterLab, ModuleLoader } from '../../lib/application';
import 'font-awesome/css/font-awesome.min.css';
import '../../lib/default-theme/index.css';
/**
 * Create an application object.
 *
 * @param loader - The module loader for the application.
 *
 * @returns A new application object.
 */
export declare function createLab(loader: ModuleLoader): JupyterLab;
