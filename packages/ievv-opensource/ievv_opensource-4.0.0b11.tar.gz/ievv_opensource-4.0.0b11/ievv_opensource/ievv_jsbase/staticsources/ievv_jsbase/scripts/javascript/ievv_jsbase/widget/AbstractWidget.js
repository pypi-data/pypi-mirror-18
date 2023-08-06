/**
 * Base class for widgets for {@link WidgetRegistrySingleton}.
 *
 * @example <caption>Create a very simple widget</caption>
 * export default class OpenMenuWidget extends AbstractWidget {
 *     constructor(element) {
 *          super(element);
 *          this._onClickBound = (...args) => {
 *              this._onClick(...args);
 *          };
 *          this.element.addEventListener('click', this._onClickBound);
 *     }
 *
 *     _onClick = (e) => {
 *          e.preventDefault();
 *          console.log('I should have opened the menu here');
 *     }
 *
 *     destroy() {
 *          this.element.removeEventListener('click', this._onClickBound);
 *     }
 * }
 *
 * @example <caption>Use the widget</caption>
 * <button type="button" data-ievv-jsbase-widget="open-menu-button">
 *     Open menu
 * </button>
 *
 * @example <caption>A widget with configuration input</caption>
 * export default class OpenMenuWidget extends AbstractWidget {
 *     constructor(element) {
 *          super(element);
 *          this._onClickBound = (...args) => {
 *              this._onClick(...args);
 *          };
 *          this.element.addEventListener('click', this._onClickBound);
 *     }
 *
 *     getDefaultConfig() {
 *          return {
 *              'menuId': 'id_main_menu';
 *          }
 *     }
 *
 *     _onClick = (e) => {
 *          e.preventDefault();
 *          console.log(`I should have opened the menu with id="${this.config.menuId}" here`);
 *     }
 *
 *     destroy() {
 *          this.element.removeEventListener('click', this._onClickBound);
 *     }
 * }
 *
 * @example <caption>Use the widget with config</caption>
 * <!-- Using the default config -->
 * <button type="button" data-ievv-jsbase-widget="open-menu-button">
 *     Open the main menu
 * </button>
 * <!-- Override the menuId config -->
 * <button type="button" data-ievv-jsbase-widget="open-menu-button"
 *          data-ievv-jsbase-widget-config='{"menuId": "id_the_other_menu"}'>
 *     Open the other menu
 * </button>
 */
export default class AbstractWidget {
    /**
     * @param {Element} element The element to load the widget in.
     */
    constructor(element) {
        this.element = element;
    }

    /**
     * Get the default config.
     *
     * Any config supplied via the ``data-ievv-jsbase-widget-config``
     * attribute is merged into this object.
     *
     * @returns {Object}
     */
    getDefaultConfig() {
        return {};
    }

    _parseConfig() {
        const attributeName = 'data-ievv-jsbase-widget-config';
        if(this.element.hasAttribute(attributeName)) {
            const rawConfig = this.element.getAttribute(attributeName);
            const config = JSON.parse(rawConfig);
            return config;
        }
        return {}
    }

    /**
     * Get the config.
     *
     * JSON decodes any config supplied via the ``data-ievv-jsbase-widget-config``
     * attribute of the Element and {@link AbstractWidget#getDefaultConfig}
     * into a config object. The result of this is cached, so multiple calls
     * to this property will only result in the config object being created
     * once.
     *
     * @throws {SyntaxError} If the ``data-ievv-jsbase-widget-config`` attribute
     *      does not contain valid JSON data.
     *      Not thrown if the element does not have a
     *      ``data-ievv-jsbase-widget-config`` attribute.
     *
     * @returns {Object} The config object. This will be an empty object
     *      if we have no {@link AbstractWidget#getDefaultConfig} and
     *      no config is supplied via the ``data-ievv-jsbase-widget-config``
     *      attribute of the Element.
     */
    get config() {
        if(typeof this._config === 'undefined') {
            const parsedConfig = this._parseConfig();
            this._config = Object.assign({}, this.getDefaultConfig(), parsedConfig);
        }
        return this._config;
    }

    /**
     * Destroy the widget.
     *
     * You should override this in subclasses if your
     * widget sets up something that will work incorrectly
     * if the widget disappears or is re-created (such as event
     * listeners and signals).
     */
    destroy() {
        
    }
}
