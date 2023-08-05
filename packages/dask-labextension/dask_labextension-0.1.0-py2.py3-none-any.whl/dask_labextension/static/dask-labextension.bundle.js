/** START DEFINE BLOCK for dask-labextension@0.1.0/lib/plugin.js **/
jupyter.define('dask-labextension@0.1.0/lib/plugin.js', function (module, exports, __jupyter_require__) {
	"use strict";
	var commandpalette_1 = __jupyter_require__('jupyterlab@^0.8.0/lib/commandpalette/index.js');
	var widget_1 = __jupyter_require__('dask-labextension@~0.1.0/lib/widget.js');
	var URL = '127.0.0.1';
	var PORT = '8787';
	var SCRIPTS = [
	    {
	        src: "http://" + URL + ":" + PORT + "/resource-profiles/autoload.js?bokeh-autoload-element=0938e7ff-da78-4769-bf7f-b31d99fd9680",
	        bokeh_id: "0938e7ff-da78-4769-bf7f-b31d99fd9680",
	        id: "distributed-ui:bk-resource-profiles-plot",
	        text: "Resource Profiles",
	        "data-bokeh-model-id": "bk-resource-profiles-plot",
	        "data-bokeh-doc-id": ""
	    },
	    {
	        src: "http://" + URL + ":" + PORT + "/memory-usage/autoload.js?bokeh-autoload-element=0938e7ff-da78-4769-bf7f-b31d99fd9682",
	        bokeh_id: "0938e7ff-da78-4769-bf7f-b31d99fd9682",
	        id: "distributed-ui:bk-nbytes-plot",
	        text: "Memory Use",
	        'data-bokeh-model-id': "bk-nbytes-plot",
	        'data-bokeh-doc-id': ""
	    },
	    {
	        src: "http://" + URL + ":" + PORT + "/task-stream/autoload.js?bokeh-autoload-element=0938e7ff-da78-4769-bf7f-b31d99fd9683",
	        bokeh_id: "0938e7ff-da78-4769-bf7f-b31d99fd9683",
	        id: "distributed-ui:bk-task-stream-plot",
	        text: "Task Stream",
	        'data-bokeh-model-id': "bk-task-stream-plot",
	        'data-bokeh-doc-id': ""
	    },
	    {
	        src: "http://" + URL + ":" + PORT + "/task-progress/autoload.js?bokeh-autoload-element=0938e7ff-da78-4769-bf7f-b31d99fd9684",
	        bokeh_id: "0938e7ff-da78-4769-bf7f-b31d99fd9684",
	        id: "distributed-ui:bk-task-progress-plot",
	        text: "Task Progress",
	        'data-bokeh-model-id': "bk-task-progress-plot",
	        'data-bokeh-doc-id': ""
	    },
	    {
	        src: "http://" + URL + ":" + PORT + "/processing-stacks/autoload.js?bokeh-autoload-element=0938e7ff-da78-4769-bf7f-b31d99fd9685",
	        bokeh_id: "0938e7ff-da78-4769-bf7f-b31d99fd9685",
	        id: "distributed-ui:bk-processing-stacks-plot",
	        text: "Processing and Stacks",
	        'data-bokeh-model-id': "bk-processing-stacks-plot",
	        'data-bokeh-doc-id': ""
	    },
	    {
	        src: "http://" + URL + ":" + PORT + "/worker-table/autoload.js?bokeh-autoload-element=0938e7ff-da78-4769-bf7f-b31d99fd9687",
	        bokeh_id: "0938e7ff-da78-4769-bf7f-b31d99fd9687",
	        id: "distributed-ui:bk-worker-table",
	        text: "Workers Table",
	        'data-bokeh-model-id': "bk-worker-table",
	        'data-bokeh-doc-id': ""
	    }
	];
	/**
	 * A namespace for help plugin private functions.
	 */
	var distributedUILab = {
	    id: 'jupyter.extensions.dask-labextension',
	    requires: [commandpalette_1.ICommandPalette],
	    activate: activateDistributedUILab,
	    autoStart: true
	};
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.default = distributedUILab;
	/**
	 * Activate the bokeh application extension.
	 */
	function activateDistributedUILab(app, palette) {
	    var elements = [];
	    for (var _i = 0, SCRIPTS_1 = SCRIPTS; _i < SCRIPTS_1.length; _i++) {
	        var script = SCRIPTS_1[_i];
	        elements.push(new widget_1.DistributedUIElement(script));
	    }
	    // Register commands for each DistributedUIElement
	    elements.forEach(function (element) { return app.commands.addCommand(element.id, {
	        label: element.title.label,
	        execute: function () {
	            app.shell.addToMainArea(element);
	        }
	    }); });
	    // Add a palette element for each DistributedUIElement command
	    elements.forEach(function (element) { return palette.addItem({
	        command: element.id,
	        category: "Dask Distributed UI"
	    }); });
	}
	
})
/** END DEFINE BLOCK for dask-labextension@0.1.0/lib/plugin.js **/


/** START DEFINE BLOCK for jupyterlab@0.8.0/lib/commandpalette/index.js **/
jupyter.define('jupyterlab@0.8.0/lib/commandpalette/index.js', function (module, exports, __jupyter_require__) {
	/*-----------------------------------------------------------------------------
	| Copyright (c) Jupyter Development Team.
	| Distributed under the terms of the Modified BSD License.
	|----------------------------------------------------------------------------*/
	"use strict";
	var token_1 = __jupyter_require__('phosphor@^0.6.1/lib/core/token.js');
	/* tslint:disable */
	/**
	 * The command palette token.
	 */
	exports.ICommandPalette = new token_1.Token('jupyter.services.commandpalette');
	//# sourceMappingURL=index.js.map
})
/** END DEFINE BLOCK for jupyterlab@0.8.0/lib/commandpalette/index.js **/


/** START DEFINE BLOCK for phosphor@0.6.1/lib/core/token.js **/
jupyter.define('phosphor@0.6.1/lib/core/token.js', function (module, exports, __jupyter_require__) {
	/*-----------------------------------------------------------------------------
	| Copyright (c) 2014-2016, PhosphorJS Contributors
	|
	| Distributed under the terms of the BSD 3-Clause License.
	|
	| The full license is in the file LICENSE, distributed with this software.
	|----------------------------------------------------------------------------*/
	"use strict";
	/**
	 * A runtime object which captures compile-time type information.
	 *
	 * #### Notes
	 * A token captures the compile-time type of an interface or class in
	 * an object which is useful for various type-safe runtime operations.
	 *
	 * #### Example
	 * ``` typescript
	 * interface IThing {
	 *   value: number;
	 * }
	 *
	 * const IThing = new Token<IThing>('my-module/IThing');
	 *
	 * // some runtime type registry
	 * registry.registerFactory(IThing, () => { value: 42 });
	 *
	 * // later...
	 * let thing = registry.getInstance(IThing);
	 * thing.value; // 42
	 * ```
	 */
	var Token = (function () {
	    /**
	     * Construct a new token.
	     *
	     * @param name - A human readable name for the token.
	     */
	    function Token(name) {
	        this._name = name;
	    }
	    Object.defineProperty(Token.prototype, "name", {
	        /**
	         * The human readable name for the token.
	         *
	         * #### Notes
	         * This can be useful for debugging and logging.
	         *
	         * This is a read-only property.
	         */
	        get: function () {
	            return this._name;
	        },
	        enumerable: true,
	        configurable: true
	    });
	    return Token;
	}());
	exports.Token = Token;
	
})
/** END DEFINE BLOCK for phosphor@0.6.1/lib/core/token.js **/


/** START DEFINE BLOCK for dask-labextension@0.1.0/lib/widget.js **/
jupyter.define('dask-labextension@0.1.0/lib/widget.js', function (module, exports, __jupyter_require__) {
	"use strict";
	var __extends = (this && this.__extends) || function (d, b) {
	    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
	    function __() { this.constructor = d; }
	    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
	};
	var widget_1 = __jupyter_require__('phosphor@0.6.1/lib/ui/widget.js');
	/**
	 * A Distributed UI element (generally a Bokeh plot) which wraps a phosphor widget.
	 */
	var DistributedUIElement = (function (_super) {
	    __extends(DistributedUIElement, _super);
	    /**
	     * Create a new DistributedUIElement.
	     */
	    function DistributedUIElement(script) {
	        var _this = this;
	        _super.call(this);
	        this._bokeh_id = "";
	        this._plot_ref = null;
	        // store bokeh model id as private attr for access in onResize eventing
	        this._bokeh_id = script["data-bokeh-model-id"];
	        var tag = document.createElement('script');
	        tag.src = script.src;
	        tag.id = script.bokeh_id;
	        tag.setAttribute('data-bokeh-model-id', script['data-bokeh-model-id']);
	        tag.setAttribute('data-bokeh-doc-id', script['data-bokeh-doc-id']);
	        tag.onload = function (event) {
	            var that = _this;
	            setTimeout(function () {
	                // wait until bokehjs is loaded and the plot is rendered and added to the index
	                // there's almost definitely a more elegant way to do this
	                that._plot_ref = Bokeh.index[that._bokeh_id].model;
	            }, 1000);
	        };
	        // wrap bokeh elements in div to apply css selector
	        var div = document.createElement('div');
	        div.classList.add('bk-root');
	        // could use some padding, but it interferes w/ the resizing rn
	        // div.style['margin'] = '10px 5px 5px'
	        div.appendChild(tag);
	        this.id = script.id;
	        this.title.label = script.text;
	        this.title.closable = true;
	        this.node.appendChild(div);
	    }
	    /**
	     * A message handler invoked on a `'resize'` message.
	     */
	    DistributedUIElement.prototype.onResize = function (msg) {
	        if (this._plot_ref) {
	            var width = msg.width;
	            var height = msg.height;
	            if (width === -1) {
	                width = null;
	            }
	            if (height === -1) {
	                height = null;
	            }
	            this._plot_ref.document.resize(width, height);
	        }
	    };
	    return DistributedUIElement;
	}(widget_1.Widget));
	exports.DistributedUIElement = DistributedUIElement;
	
})
/** END DEFINE BLOCK for dask-labextension@0.1.0/lib/widget.js **/


/** START DEFINE BLOCK for phosphor@0.6.1/lib/ui/widget.js **/
jupyter.define('phosphor@0.6.1/lib/ui/widget.js', function (module, exports, __jupyter_require__) {
	"use strict";
	var __extends = (this && this.__extends) || function (d, b) {
	    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
	    function __() { this.constructor = d; }
	    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
	};
	/*-----------------------------------------------------------------------------
	| Copyright (c) 2014-2016, PhosphorJS Contributors
	|
	| Distributed under the terms of the BSD 3-Clause License.
	|
	| The full license is in the file LICENSE, distributed with this software.
	|----------------------------------------------------------------------------*/
	var iteration_1 = __jupyter_require__('phosphor@~0.6.1/lib/algorithm/iteration.js');
	var messaging_1 = __jupyter_require__('phosphor@~0.6.1/lib/core/messaging.js');
	var properties_1 = __jupyter_require__('phosphor@~0.6.1/lib/core/properties.js');
	var signaling_1 = __jupyter_require__('phosphor@~0.6.1/lib/core/signaling.js');
	var title_1 = __jupyter_require__('phosphor@~0.6.1/lib/ui/title.js');
	/**
	 * The class name added to Widget instances.
	 */
	var WIDGET_CLASS = 'p-Widget';
	/**
	 * The class name added to hidden widgets.
	 */
	var HIDDEN_CLASS = 'p-mod-hidden';
	/**
	 * The base class of the Phosphor widget hierarchy.
	 *
	 * #### Notes
	 * This class will typically be subclassed in order to create a useful
	 * widget. However, it can be used directly to host externally created
	 * content.
	 */
	var Widget = (function () {
	    /**
	     * Construct a new widget.
	     *
	     * @param options - The options for initializing the widget.
	     */
	    function Widget(options) {
	        if (options === void 0) { options = {}; }
	        this._flags = 0;
	        this._layout = null;
	        this._parent = null;
	        this._node = Private.createNode(options);
	        this.addClass(WIDGET_CLASS);
	    }
	    /**
	     * Dispose of the widget and its descendant widgets.
	     *
	     * #### Notes
	     * It is unsafe to use the widget after it has been disposed.
	     *
	     * All calls made to this method after the first are a no-op.
	     */
	    Widget.prototype.dispose = function () {
	        // Do nothing if the widget is already disposed.
	        if (this.isDisposed) {
	            return;
	        }
	        // Set the disposed flag and emit the disposed signal.
	        this.setFlag(WidgetFlag.IsDisposed);
	        this.disposed.emit(void 0);
	        // Remove or detach the widget if necessary.
	        if (this.parent) {
	            this.parent = null;
	        }
	        else if (this.isAttached) {
	            Widget.detach(this);
	        }
	        // Dispose of the widget layout.
	        if (this._layout) {
	            this._layout.dispose();
	            this._layout = null;
	        }
	        // Clear the attached data associated with the widget.
	        signaling_1.clearSignalData(this);
	        messaging_1.clearMessageData(this);
	        properties_1.clearPropertyData(this);
	        // Clear the reference to the DOM node.
	        this._node = null;
	    };
	    Object.defineProperty(Widget.prototype, "isDisposed", {
	        /**
	         * Test whether the widget has been disposed.
	         *
	         * #### Notes
	         * This is a read-only property.
	         */
	        get: function () {
	            return this.testFlag(WidgetFlag.IsDisposed);
	        },
	        enumerable: true,
	        configurable: true
	    });
	    Object.defineProperty(Widget.prototype, "isAttached", {
	        /**
	         * Test whether the widget's node is attached to the DOM.
	         *
	         * #### Notes
	         * This is a read-only property.
	         */
	        get: function () {
	            return this.testFlag(WidgetFlag.IsAttached);
	        },
	        enumerable: true,
	        configurable: true
	    });
	    Object.defineProperty(Widget.prototype, "isHidden", {
	        /**
	         * Test whether the widget is explicitly hidden.
	         *
	         * #### Notes
	         * This is a read-only property.
	         */
	        get: function () {
	            return this.testFlag(WidgetFlag.IsHidden);
	        },
	        enumerable: true,
	        configurable: true
	    });
	    Object.defineProperty(Widget.prototype, "isVisible", {
	        /**
	         * Test whether the widget is visible.
	         *
	         * #### Notes
	         * A widget is visible when it is attached to the DOM, is not
	         * explicitly hidden, and has no explicitly hidden ancestors.
	         *
	         * This is a read-only property.
	         */
	        get: function () {
	            return this.testFlag(WidgetFlag.IsVisible);
	        },
	        enumerable: true,
	        configurable: true
	    });
	    Object.defineProperty(Widget.prototype, "node", {
	        /**
	         * Get the DOM node owned by the widget.
	         *
	         * #### Notes
	         * This is a read-only property.
	         */
	        get: function () {
	            return this._node;
	        },
	        enumerable: true,
	        configurable: true
	    });
	    Object.defineProperty(Widget.prototype, "id", {
	        /**
	         * Get the id of the widget's DOM node.
	         */
	        get: function () {
	            return this._node.id;
	        },
	        /**
	         * Set the id of the widget's DOM node.
	         */
	        set: function (value) {
	            this._node.id = value;
	        },
	        enumerable: true,
	        configurable: true
	    });
	    Object.defineProperty(Widget.prototype, "title", {
	        /**
	         * Get the title object for the widget.
	         *
	         * #### Notes
	         * The title object is used by some container widgets when displaying
	         * the widget alongside some title, such as a tab panel or side bar.
	         *
	         * Since not all widgets will use the title, it is created on demand.
	         *
	         * The `owner` property of the title is set to this widget.
	         *
	         * This is a read-only property.
	         */
	        get: function () {
	            return Private.titleProperty.get(this);
	        },
	        enumerable: true,
	        configurable: true
	    });
	    Object.defineProperty(Widget.prototype, "parent", {
	        /**
	         * Get the parent of the widget.
	         *
	         * #### Notes
	         * This will be `null` if the widget does not have a parent.
	         */
	        get: function () {
	            return this._parent;
	        },
	        /**
	         * Set the parent of the widget.
	         *
	         * #### Notes
	         * Children are typically added to a widget by using a layout, which
	         * means user code will not normally set the parent widget directly.
	         *
	         * The widget will be automatically removed from its old parent.
	         *
	         * This is a no-op if there is no effective parent change.
	         */
	        set: function (value) {
	            value = value || null;
	            if (this._parent === value) {
	                return;
	            }
	            if (value && this.contains(value)) {
	                throw new Error('Invalid parent widget.');
	            }
	            if (this._parent && !this._parent.isDisposed) {
	                messaging_1.sendMessage(this._parent, new ChildMessage('child-removed', this));
	            }
	            this._parent = value;
	            if (this._parent && !this._parent.isDisposed) {
	                messaging_1.sendMessage(this._parent, new ChildMessage('child-added', this));
	            }
	            messaging_1.sendMessage(this, WidgetMessage.ParentChanged);
	        },
	        enumerable: true,
	        configurable: true
	    });
	    Object.defineProperty(Widget.prototype, "layout", {
	        /**
	         * Get the layout for the widget.
	         *
	         * #### Notes
	         * This will be `null` if the widget does not have a layout.
	         */
	        get: function () {
	            return this._layout;
	        },
	        /**
	         * Set the layout for the widget.
	         *
	         * #### Notes
	         * The layout is single-use only. It cannot be set to `null` and it
	         * cannot be changed after the first assignment.
	         *
	         * The layout is disposed automatically when the widget is disposed.
	         */
	        set: function (value) {
	            value = value || null;
	            if (this._layout === value) {
	                return;
	            }
	            if (this.testFlag(WidgetFlag.DisallowLayout)) {
	                throw new Error('Cannot set widget layout.');
	            }
	            if (this._layout) {
	                throw new Error('Cannot change widget layout.');
	            }
	            if (value.parent) {
	                throw new Error('Cannot change layout parent.');
	            }
	            this._layout = value;
	            value.parent = this;
	            messaging_1.sendMessage(this, WidgetMessage.LayoutChanged);
	        },
	        enumerable: true,
	        configurable: true
	    });
	    /**
	     * Create an iterator over the widget's children.
	     *
	     * @returns A new iterator over the children of the widget.
	     *
	     * #### Notes
	     * The widget must have a populated layout in order to have children.
	     *
	     * If a layout is not installed, the returned iterator will be empty.
	     */
	    Widget.prototype.children = function () {
	        return iteration_1.iter(this._layout || iteration_1.EmptyIterator.instance);
	    };
	    /**
	     * Test whether a widget is a descendant of this widget.
	     *
	     * @param widget - The descendant widget of interest.
	     *
	     * @returns `true` if the widget is a descendant, `false` otherwise.
	     */
	    Widget.prototype.contains = function (widget) {
	        for (; widget; widget = widget._parent) {
	            if (widget === this)
	                return true;
	        }
	        return false;
	    };
	    /**
	     * Test whether the widget's DOM node has the given class name.
	     *
	     * @param name - The class name of interest.
	     *
	     * @returns `true` if the node has the class, `false` otherwise.
	     */
	    Widget.prototype.hasClass = function (name) {
	        return this._node.classList.contains(name);
	    };
	    /**
	     * Add a class name to the widget's DOM node.
	     *
	     * @param name - The class name to add to the node.
	     *
	     * #### Notes
	     * If the class name is already added to the node, this is a no-op.
	     *
	     * The class name must not contain whitespace.
	     */
	    Widget.prototype.addClass = function (name) {
	        this._node.classList.add(name);
	    };
	    /**
	     * Remove a class name from the widget's DOM node.
	     *
	     * @param name - The class name to remove from the node.
	     *
	     * #### Notes
	     * If the class name is not yet added to the node, this is a no-op.
	     *
	     * The class name must not contain whitespace.
	     */
	    Widget.prototype.removeClass = function (name) {
	        this._node.classList.remove(name);
	    };
	    /**
	     * Toggle a class name on the widget's DOM node.
	     *
	     * @param name - The class name to toggle on the node.
	     *
	     * @param force - Whether to force add the class (`true`) or force
	     *   remove the class (`false`). If not provided, the presence of
	     *   the class will be toggled from its current state.
	     *
	     * @returns `true` if the class is now present, `false` otherwise.
	     *
	     * #### Notes
	     * The class name must not contain whitespace.
	     */
	    Widget.prototype.toggleClass = function (name, force) {
	        if (force === true) {
	            this._node.classList.add(name);
	            return true;
	        }
	        if (force === false) {
	            this._node.classList.remove(name);
	            return false;
	        }
	        return this._node.classList.toggle(name);
	    };
	    /**
	     * Post an `'update-request'` message to the widget.
	     *
	     * #### Notes
	     * This is a simple convenience method for posting the message.
	     */
	    Widget.prototype.update = function () {
	        messaging_1.postMessage(this, WidgetMessage.UpdateRequest);
	    };
	    /**
	     * Post a `'fit-request'` message to the widget.
	     *
	     * #### Notes
	     * This is a simple convenience method for posting the message.
	     */
	    Widget.prototype.fit = function () {
	        messaging_1.postMessage(this, WidgetMessage.FitRequest);
	    };
	    /**
	     * Post an `'activate-request'` message to the widget.
	     *
	     * #### Notes
	     * This is a simple convenience method for posting the message.
	     */
	    Widget.prototype.activate = function () {
	        messaging_1.postMessage(this, WidgetMessage.ActivateRequest);
	    };
	    /**
	     * Post a `'deactivate-request'` message to the widget.
	     *
	     * #### Notes
	     * This is a simple convenience method for posting the message.
	     */
	    Widget.prototype.deactivate = function () {
	        messaging_1.postMessage(this, WidgetMessage.DeactivateRequest);
	    };
	    /**
	     * Send a `'close-request'` message to the widget.
	     *
	     * #### Notes
	     * This is a simple convenience method for sending the message.
	     */
	    Widget.prototype.close = function () {
	        messaging_1.sendMessage(this, WidgetMessage.CloseRequest);
	    };
	    /**
	     * Show the widget and make it visible to its parent widget.
	     *
	     * #### Notes
	     * This causes the [[isHidden]] property to be `false`.
	     *
	     * If the widget is not explicitly hidden, this is a no-op.
	     */
	    Widget.prototype.show = function () {
	        if (!this.testFlag(WidgetFlag.IsHidden)) {
	            return;
	        }
	        this.clearFlag(WidgetFlag.IsHidden);
	        this.removeClass(HIDDEN_CLASS);
	        if (this.isAttached && (!this.parent || this.parent.isVisible)) {
	            messaging_1.sendMessage(this, WidgetMessage.AfterShow);
	        }
	        if (this.parent) {
	            messaging_1.sendMessage(this.parent, new ChildMessage('child-shown', this));
	        }
	    };
	    /**
	     * Hide the widget and make it hidden to its parent widget.
	     *
	     * #### Notes
	     * This causes the [[isHidden]] property to be `true`.
	     *
	     * If the widget is explicitly hidden, this is a no-op.
	     */
	    Widget.prototype.hide = function () {
	        if (this.testFlag(WidgetFlag.IsHidden)) {
	            return;
	        }
	        if (this.isAttached && (!this.parent || this.parent.isVisible)) {
	            messaging_1.sendMessage(this, WidgetMessage.BeforeHide);
	        }
	        this.setFlag(WidgetFlag.IsHidden);
	        this.addClass(HIDDEN_CLASS);
	        if (this.parent) {
	            messaging_1.sendMessage(this.parent, new ChildMessage('child-hidden', this));
	        }
	    };
	    /**
	     * Show or hide the widget according to a boolean value.
	     *
	     * @param hidden - `true` to hide the widget, or `false` to show it.
	     *
	     * #### Notes
	     * This is a convenience method for `hide()` and `show()`.
	     */
	    Widget.prototype.setHidden = function (hidden) {
	        if (hidden) {
	            this.hide();
	        }
	        else {
	            this.show();
	        }
	    };
	    /**
	     * Test whether the given widget flag is set.
	     *
	     * #### Notes
	     * This will not typically be called directly by user code.
	     */
	    Widget.prototype.testFlag = function (flag) {
	        return (this._flags & flag) !== 0;
	    };
	    /**
	     * Set the given widget flag.
	     *
	     * #### Notes
	     * This will not typically be called directly by user code.
	     */
	    Widget.prototype.setFlag = function (flag) {
	        this._flags |= flag;
	    };
	    /**
	     * Clear the given widget flag.
	     *
	     * #### Notes
	     * This will not typically be called directly by user code.
	     */
	    Widget.prototype.clearFlag = function (flag) {
	        this._flags &= ~flag;
	    };
	    /**
	     * Process a message sent to the widget.
	     *
	     * @param msg - The message sent to the widget.
	     *
	     * #### Notes
	     * Subclasses may reimplement this method as needed.
	     */
	    Widget.prototype.processMessage = function (msg) {
	        switch (msg.type) {
	            case 'resize':
	                this.notifyLayout(msg);
	                this.onResize(msg);
	                break;
	            case 'update-request':
	                this.notifyLayout(msg);
	                this.onUpdateRequest(msg);
	                break;
	            case 'after-show':
	                this.setFlag(WidgetFlag.IsVisible);
	                this.notifyLayout(msg);
	                this.onAfterShow(msg);
	                break;
	            case 'before-hide':
	                this.notifyLayout(msg);
	                this.onBeforeHide(msg);
	                this.clearFlag(WidgetFlag.IsVisible);
	                break;
	            case 'after-attach':
	                var visible = !this.isHidden && (!this.parent || this.parent.isVisible);
	                if (visible)
	                    this.setFlag(WidgetFlag.IsVisible);
	                this.setFlag(WidgetFlag.IsAttached);
	                this.notifyLayout(msg);
	                this.onAfterAttach(msg);
	                break;
	            case 'before-detach':
	                this.notifyLayout(msg);
	                this.onBeforeDetach(msg);
	                this.clearFlag(WidgetFlag.IsVisible);
	                this.clearFlag(WidgetFlag.IsAttached);
	                break;
	            case 'activate-request':
	                this.notifyLayout(msg);
	                this.onActivateRequest(msg);
	                break;
	            case 'deactivate-request':
	                this.notifyLayout(msg);
	                this.onDeactivateRequest(msg);
	                break;
	            case 'close-request':
	                this.notifyLayout(msg);
	                this.onCloseRequest(msg);
	                break;
	            case 'child-added':
	                this.notifyLayout(msg);
	                this.onChildAdded(msg);
	                break;
	            case 'child-removed':
	                this.notifyLayout(msg);
	                this.onChildRemoved(msg);
	                break;
	            default:
	                this.notifyLayout(msg);
	                break;
	        }
	    };
	    /**
	     * Invoke the message processing routine of the widget's layout.
	     *
	     * @param msg - The message to dispatch to the layout.
	     *
	     * #### Notes
	     * This is a no-op if the widget does not have a layout.
	     *
	     * This will not typically be called directly by user code.
	     */
	    Widget.prototype.notifyLayout = function (msg) {
	        if (this._layout)
	            this._layout.processParentMessage(msg);
	    };
	    /**
	     * A message handler invoked on a `'close-request'` message.
	     *
	     * #### Notes
	     * The default implementation unparents or detaches the widget.
	     */
	    Widget.prototype.onCloseRequest = function (msg) {
	        if (this.parent) {
	            this.parent = null;
	        }
	        else if (this.isAttached) {
	            Widget.detach(this);
	        }
	    };
	    /**
	     * A message handler invoked on a `'resize'` message.
	     *
	     * #### Notes
	     * The default implementation of this handler is a no-op.
	     */
	    Widget.prototype.onResize = function (msg) { };
	    /**
	     * A message handler invoked on an `'update-request'` message.
	     *
	     * #### Notes
	     * The default implementation of this handler is a no-op.
	     */
	    Widget.prototype.onUpdateRequest = function (msg) { };
	    /**
	     * A message handler invoked on an `'activate-request'` message.
	     *
	     * #### Notes
	     * The default implementation of this handler is a no-op.
	     */
	    Widget.prototype.onActivateRequest = function (msg) { };
	    /**
	     * A message handler invoked on a `'deactivate-request'` message.
	     *
	     * #### Notes
	     * The default implementation of this handler is a no-op.
	     */
	    Widget.prototype.onDeactivateRequest = function (msg) { };
	    /**
	     * A message handler invoked on an `'after-show'` message.
	     *
	     * #### Notes
	     * The default implementation of this handler is a no-op.
	     */
	    Widget.prototype.onAfterShow = function (msg) { };
	    /**
	     * A message handler invoked on a `'before-hide'` message.
	     *
	     * #### Notes
	     * The default implementation of this handler is a no-op.
	     */
	    Widget.prototype.onBeforeHide = function (msg) { };
	    /**
	     * A message handler invoked on an `'after-attach'` message.
	     *
	     * #### Notes
	     * The default implementation of this handler is a no-op.
	     */
	    Widget.prototype.onAfterAttach = function (msg) { };
	    /**
	     * A message handler invoked on a `'before-detach'` message.
	     *
	     * #### Notes
	     * The default implementation of this handler is a no-op.
	     */
	    Widget.prototype.onBeforeDetach = function (msg) { };
	    /**
	     * A message handler invoked on a `'child-added'` message.
	     *
	     * #### Notes
	     * The default implementation of this handler is a no-op.
	     */
	    Widget.prototype.onChildAdded = function (msg) { };
	    /**
	     * A message handler invoked on a `'child-removed'` message.
	     *
	     * #### Notes
	     * The default implementation of this handler is a no-op.
	     */
	    Widget.prototype.onChildRemoved = function (msg) { };
	    return Widget;
	}());
	exports.Widget = Widget;
	// Define the signals for the `Widget` class.
	signaling_1.defineSignal(Widget.prototype, 'disposed');
	/**
	 * The namespace for the `Widget` class statics.
	 */
	var Widget;
	(function (Widget) {
	    // TODO - should this be an instance method?
	    /**
	     * Attach a widget to a host DOM node.
	     *
	     * @param widget - The widget of interest.
	     *
	     * @param host - The DOM node to use as the widget's host.
	     *
	     * #### Notes
	     * This will throw an error if the widget is not a root widget, if
	     * the widget is already attached, or if the host is not attached
	     * to the DOM.
	     */
	    function attach(widget, host) {
	        if (widget.parent) {
	            throw new Error('Cannot attach child widget.');
	        }
	        if (widget.isAttached || document.body.contains(widget.node)) {
	            throw new Error('Widget already attached.');
	        }
	        if (!document.body.contains(host)) {
	            throw new Error('Host not attached.');
	        }
	        host.appendChild(widget.node);
	        messaging_1.sendMessage(widget, WidgetMessage.AfterAttach);
	    }
	    Widget.attach = attach;
	    // TODO - should this be an instance method?
	    /**
	     * Detach the widget from its host DOM node.
	     *
	     * @param widget - The widget of interest.
	     *
	     * #### Notes
	     * This will throw an error if the widget is not a root widget, or
	     * if the widget is not attached to the DOM.
	     */
	    function detach(widget) {
	        if (widget.parent) {
	            throw new Error('Cannot detach child widget.');
	        }
	        if (!widget.isAttached || !document.body.contains(widget.node)) {
	            throw new Error('Widget not attached.');
	        }
	        messaging_1.sendMessage(widget, WidgetMessage.BeforeDetach);
	        widget.node.parentNode.removeChild(widget.node);
	    }
	    Widget.detach = detach;
	    /**
	     * Prepare a widget for absolute layout geometry.
	     *
	     * @param widget - The widget of interest.
	     *
	     * #### Notes
	     * This sets the inline style position of the widget to `absolute`.
	     */
	    function prepareGeometry(widget) {
	        widget.node.style.position = 'absolute';
	    }
	    Widget.prepareGeometry = prepareGeometry;
	    /**
	     * Reset the layout geometry of a widget.
	     *
	     * @param widget - The widget of interest.
	     *
	     * #### Notes
	     * This clears the inline style position and geometry of the widget.
	     */
	    function resetGeometry(widget) {
	        var style = widget.node.style;
	        var rect = Private.rectProperty.get(widget);
	        rect.top = NaN;
	        rect.left = NaN;
	        rect.width = NaN;
	        rect.height = NaN;
	        style.position = '';
	        style.top = '';
	        style.left = '';
	        style.width = '';
	        style.height = '';
	    }
	    Widget.resetGeometry = resetGeometry;
	    /**
	     * Set the absolute layout geometry of a widget.
	     *
	     * @param widget - The widget of interest.
	     *
	     * @param left - The desired offset left position of the widget.
	     *
	     * @param top - The desired offset top position of the widget.
	     *
	     * @param width - The desired offset width of the widget.
	     *
	     * @param height - The desired offset height of the widget.
	     *
	     * #### Notes
	     * All dimensions are assumed to be pixels with coordinates relative
	     * to the origin of the widget's offset parent.
	     *
	     * The widget's node is assumed to be position `absolute`.
	     *
	     * If the widget is resized from its previous size, a `ResizeMessage`
	     * will be automatically sent to the widget.
	     */
	    function setGeometry(widget, left, top, width, height) {
	        var resized = false;
	        var style = widget.node.style;
	        var rect = Private.rectProperty.get(widget);
	        if (rect.top !== top) {
	            rect.top = top;
	            style.top = top + "px";
	        }
	        if (rect.left !== left) {
	            rect.left = left;
	            style.left = left + "px";
	        }
	        if (rect.width !== width) {
	            resized = true;
	            rect.width = width;
	            style.width = width + "px";
	        }
	        if (rect.height !== height) {
	            resized = true;
	            rect.height = height;
	            style.height = height + "px";
	        }
	        if (resized) {
	            messaging_1.sendMessage(widget, new ResizeMessage(width, height));
	        }
	    }
	    Widget.setGeometry = setGeometry;
	})(Widget = exports.Widget || (exports.Widget = {}));
	/**
	 * An abstract base class for creating Phosphor layouts.
	 *
	 * #### Notes
	 * A layout is used to add widgets to a parent and to arrange those
	 * widgets within the parent's DOM node.
	 *
	 * This class implements the base functionality which is required of
	 * nearly all layouts. It must be subclassed in order to be useful.
	 *
	 * Notably, this class does not define a uniform interface for adding
	 * widgets to the layout. A subclass should define that API in a way
	 * which is meaningful for its intended use.
	 */
	var Layout = (function () {
	    function Layout() {
	        this._disposed = false;
	        this._parent = null;
	    }
	    /**
	     * Dispose of the resources held by the layout.
	     *
	     * #### Notes
	     * This should be reimplemented to clear and dispose of the widgets.
	     *
	     * All reimplementations should call the superclass method.
	     *
	     * This method is called automatically when the parent is disposed.
	     */
	    Layout.prototype.dispose = function () {
	        this._disposed = true;
	        this._parent = null;
	        signaling_1.clearSignalData(this);
	        properties_1.clearPropertyData(this);
	    };
	    Object.defineProperty(Layout.prototype, "isDisposed", {
	        /**
	         * Test whether the layout is disposed.
	         *
	         * #### Notes
	         * This is a read-only property.
	         */
	        get: function () {
	            return this._disposed;
	        },
	        enumerable: true,
	        configurable: true
	    });
	    Object.defineProperty(Layout.prototype, "parent", {
	        /**
	         * Get the parent widget of the layout.
	         */
	        get: function () {
	            return this._parent;
	        },
	        /**
	         * Set the parent widget of the layout.
	         *
	         * #### Notes
	         * This is set automatically when installing the layout on the parent
	         * widget. The parent widget should not be set directly by user code.
	         */
	        set: function (value) {
	            if (!value) {
	                throw new Error('Cannot set parent widget to null.');
	            }
	            if (this._parent === value) {
	                return;
	            }
	            if (this._parent) {
	                throw new Error('Cannot change parent widget.');
	            }
	            if (value.layout !== this) {
	                throw new Error('Invalid parent widget.');
	            }
	            this._parent = value;
	        },
	        enumerable: true,
	        configurable: true
	    });
	    /**
	     * Process a message sent to the parent widget.
	     *
	     * @param msg - The message sent to the parent widget.
	     *
	     * #### Notes
	     * This method is called by the parent widget to process a message.
	     *
	     * Subclasses may reimplement this method as needed.
	     */
	    Layout.prototype.processParentMessage = function (msg) {
	        switch (msg.type) {
	            case 'resize':
	                this.onResize(msg);
	                break;
	            case 'update-request':
	                this.onUpdateRequest(msg);
	                break;
	            case 'fit-request':
	                this.onFitRequest(msg);
	                break;
	            case 'after-show':
	                this.onAfterShow(msg);
	                break;
	            case 'before-hide':
	                this.onBeforeHide(msg);
	                break;
	            case 'after-attach':
	                this.onAfterAttach(msg);
	                break;
	            case 'before-detach':
	                this.onBeforeDetach(msg);
	                break;
	            case 'child-removed':
	                this.onChildRemoved(msg);
	                break;
	            case 'child-shown':
	                this.onChildShown(msg);
	                break;
	            case 'child-hidden':
	                this.onChildHidden(msg);
	                break;
	            case 'layout-changed':
	                this.onLayoutChanged(msg);
	                break;
	        }
	    };
	    /**
	     * A message handler invoked on a `'resize'` message.
	     *
	     * #### Notes
	     * The layout should ensure that its widgets are resized according
	     * to the specified layout space, and that they are sent a `'resize'`
	     * message if appropriate.
	     *
	     * The default implementation of this method sends an `UnknownSize`
	     * resize message to all widgets.
	     *
	     * This may be reimplemented by subclasses as needed.
	     */
	    Layout.prototype.onResize = function (msg) {
	        iteration_1.each(this, function (widget) { messaging_1.sendMessage(widget, ResizeMessage.UnknownSize); });
	    };
	    /**
	     * A message handler invoked on an `'update-request'` message.
	     *
	     * #### Notes
	     * The layout should ensure that its widgets are resized according
	     * to the available layout space, and that they are sent a `'resize'`
	     * message if appropriate.
	     *
	     * The default implementation of this method sends an `UnknownSize`
	     * resize message to all widgets.
	     *
	     * This may be reimplemented by subclasses as needed.
	     */
	    Layout.prototype.onUpdateRequest = function (msg) {
	        iteration_1.each(this, function (widget) { messaging_1.sendMessage(widget, ResizeMessage.UnknownSize); });
	    };
	    /**
	     * A message handler invoked on an `'after-attach'` message.
	     *
	     * #### Notes
	     * The default implementation of this method forwards the message
	     * to all widgets. It assumes all widget nodes are attached to the
	     * parent widget node.
	     *
	     * This may be reimplemented by subclasses as needed.
	     */
	    Layout.prototype.onAfterAttach = function (msg) {
	        iteration_1.each(this, function (widget) { messaging_1.sendMessage(widget, msg); });
	    };
	    /**
	     * A message handler invoked on a `'before-detach'` message.
	     *
	     * #### Notes
	     * The default implementation of this method forwards the message
	     * to all widgets. It assumes all widget nodes are attached to the
	     * parent widget node.
	     *
	     * This may be reimplemented by subclasses as needed.
	     */
	    Layout.prototype.onBeforeDetach = function (msg) {
	        iteration_1.each(this, function (widget) { messaging_1.sendMessage(widget, msg); });
	    };
	    /**
	     * A message handler invoked on an `'after-show'` message.
	     *
	     * #### Notes
	     * The default implementation of this method forwards the message to
	     * all non-hidden widgets. It assumes all widget nodes are attached
	     * to the parent widget node.
	     *
	     * This may be reimplemented by subclasses as needed.
	     */
	    Layout.prototype.onAfterShow = function (msg) {
	        iteration_1.each(this, function (widget) { if (!widget.isHidden)
	            messaging_1.sendMessage(widget, msg); });
	    };
	    /**
	     * A message handler invoked on a `'before-hide'` message.
	     *
	     * #### Notes
	     * The default implementation of this method forwards the message to
	     * all non-hidden widgets. It assumes all widget nodes are attached
	     * to the parent widget node.
	     *
	     * This may be reimplemented by subclasses as needed.
	     */
	    Layout.prototype.onBeforeHide = function (msg) {
	        iteration_1.each(this, function (widget) { if (!widget.isHidden)
	            messaging_1.sendMessage(widget, msg); });
	    };
	    /**
	     * A message handler invoked on a `'fit-request'` message.
	     *
	     * #### Notes
	     * The default implementation of this handler is a no-op.
	     */
	    Layout.prototype.onFitRequest = function (msg) { };
	    /**
	     * A message handler invoked on a `'child-shown'` message.
	     *
	     * #### Notes
	     * The default implementation of this handler is a no-op.
	     */
	    Layout.prototype.onChildShown = function (msg) { };
	    /**
	     * A message handler invoked on a `'child-hidden'` message.
	     *
	     * #### Notes
	     * The default implementation of this handler is a no-op.
	     */
	    Layout.prototype.onChildHidden = function (msg) { };
	    return Layout;
	}());
	exports.Layout = Layout;
	// TODO should this be in the Widget namespace?
	/**
	 * An enum of widget bit flags.
	 */
	(function (WidgetFlag) {
	    /**
	     * The widget has been disposed.
	     */
	    WidgetFlag[WidgetFlag["IsDisposed"] = 1] = "IsDisposed";
	    /**
	     * The widget is attached to the DOM.
	     */
	    WidgetFlag[WidgetFlag["IsAttached"] = 2] = "IsAttached";
	    /**
	     * The widget is hidden.
	     */
	    WidgetFlag[WidgetFlag["IsHidden"] = 4] = "IsHidden";
	    /**
	     * The widget is visible.
	     */
	    WidgetFlag[WidgetFlag["IsVisible"] = 8] = "IsVisible";
	    /**
	     * A layout cannot be set on the widget.
	     */
	    WidgetFlag[WidgetFlag["DisallowLayout"] = 16] = "DisallowLayout";
	})(exports.WidgetFlag || (exports.WidgetFlag = {}));
	var WidgetFlag = exports.WidgetFlag;
	// TODO should this be in the Widget namespace?
	/**
	 * A collection of stateless messages related to widgets.
	 */
	var WidgetMessage;
	(function (WidgetMessage) {
	    /**
	     * A singleton `'after-show'` message.
	     *
	     * #### Notes
	     * This message is sent to a widget after it becomes visible.
	     *
	     * This message is **not** sent when the widget is being attached.
	     */
	    WidgetMessage.AfterShow = new messaging_1.Message('after-show');
	    /**
	     * A singleton `'before-hide'` message.
	     *
	     * #### Notes
	     * This message is sent to a widget before it becomes not-visible.
	     *
	     * This message is **not** sent when the widget is being detached.
	     */
	    WidgetMessage.BeforeHide = new messaging_1.Message('before-hide');
	    /**
	     * A singleton `'after-attach'` message.
	     *
	     * #### Notes
	     * This message is sent to a widget after it is attached.
	     */
	    WidgetMessage.AfterAttach = new messaging_1.Message('after-attach');
	    /**
	     * A singleton `'before-detach'` message.
	     *
	     * #### Notes
	     * This message is sent to a widget before it is detached.
	     */
	    WidgetMessage.BeforeDetach = new messaging_1.Message('before-detach');
	    /**
	     * A singleton `'parent-changed'` message.
	     *
	     * #### Notes
	     * This message is sent to a widget when its parent has changed.
	     */
	    WidgetMessage.ParentChanged = new messaging_1.Message('parent-changed');
	    /**
	     * A singleton `'layout-changed'` message.
	     *
	     * #### Notes
	     * This message is sent to a widget when its layout has changed.
	     */
	    WidgetMessage.LayoutChanged = new messaging_1.Message('layout-changed');
	    /**
	     * A singleton conflatable `'update-request'` message.
	     *
	     * #### Notes
	     * This message can be dispatched to supporting widgets in order to
	     * update their content based on the current widget state. Not all
	     * widgets will respond to messages of this type.
	     *
	     * For widgets with a layout, this message will inform the layout to
	     * update the position and size of its child widgets.
	     */
	    WidgetMessage.UpdateRequest = new messaging_1.ConflatableMessage('update-request');
	    /**
	     * A singleton conflatable `'fit-request'` message.
	     *
	     * #### Notes
	     * For widgets with a layout, this message will inform the layout to
	     * recalculate its size constraints to fit the space requirements of
	     * its child widgets, and to update their position and size. Not all
	     * layouts will respond to messages of this type.
	     */
	    WidgetMessage.FitRequest = new messaging_1.ConflatableMessage('fit-request');
	    /**
	     * A singleton conflatable `'activate-request'` message.
	     *
	     * #### Notes
	     * This message should be dispatched to a widget when it should
	     * perform the actions necessary to activate the widget, which
	     * may include focusing its node or descendant node.
	     */
	    WidgetMessage.ActivateRequest = new messaging_1.ConflatableMessage('activate-request');
	    /**
	     * A singleton conflatable `'deactivate-request'` message.
	     *
	     * #### Notes
	     * This message should be dispatched to a widget when it should
	     * perform the actions necessary to decactivate the widget, which
	     * may include blurring its node or descendant node.
	     */
	    WidgetMessage.DeactivateRequest = new messaging_1.ConflatableMessage('deactivate-request');
	    /**
	     * A singleton conflatable `'close-request'` message.
	     *
	     * #### Notes
	     * This message should be dispatched to a widget when it should close
	     * and remove itself from the widget hierarchy.
	     */
	    WidgetMessage.CloseRequest = new messaging_1.ConflatableMessage('close-request');
	})(WidgetMessage = exports.WidgetMessage || (exports.WidgetMessage = {}));
	// TODO should this be in the Widget namespace?
	/**
	 * A message class for child related messages.
	 */
	var ChildMessage = (function (_super) {
	    __extends(ChildMessage, _super);
	    /**
	     * Construct a new child message.
	     *
	     * @param type - The message type.
	     *
	     * @param child - The child widget for the message.
	     */
	    function ChildMessage(type, child) {
	        _super.call(this, type);
	        this._child = child;
	    }
	    Object.defineProperty(ChildMessage.prototype, "child", {
	        /**
	         * The child widget for the message.
	         *
	         * #### Notes
	         * This is a read-only property.
	         */
	        get: function () {
	            return this._child;
	        },
	        enumerable: true,
	        configurable: true
	    });
	    return ChildMessage;
	}(messaging_1.Message));
	exports.ChildMessage = ChildMessage;
	// TODO should this be in the Widget namespace?
	/**
	 * A message class for `'resize'` messages.
	 */
	var ResizeMessage = (function (_super) {
	    __extends(ResizeMessage, _super);
	    /**
	     * Construct a new resize message.
	     *
	     * @param width - The **offset width** of the widget, or `-1` if
	     *   the width is not known.
	     *
	     * @param height - The **offset height** of the widget, or `-1` if
	     *   the height is not known.
	     */
	    function ResizeMessage(width, height) {
	        _super.call(this, 'resize');
	        this._width = width;
	        this._height = height;
	    }
	    Object.defineProperty(ResizeMessage.prototype, "width", {
	        /**
	         * The offset width of the widget.
	         *
	         * #### Notes
	         * This will be `-1` if the width is unknown.
	         *
	         * This is a read-only property.
	         */
	        get: function () {
	            return this._width;
	        },
	        enumerable: true,
	        configurable: true
	    });
	    Object.defineProperty(ResizeMessage.prototype, "height", {
	        /**
	         * The offset height of the widget.
	         *
	         * #### Notes
	         * This will be `-1` if the height is unknown.
	         *
	         * This is a read-only property.
	         */
	        get: function () {
	            return this._height;
	        },
	        enumerable: true,
	        configurable: true
	    });
	    return ResizeMessage;
	}(messaging_1.Message));
	exports.ResizeMessage = ResizeMessage;
	/**
	 * The namespace for the `ResizeMessage` class statics.
	 */
	var ResizeMessage;
	(function (ResizeMessage) {
	    /**
	     * A singleton `'resize'` message with an unknown size.
	     */
	    ResizeMessage.UnknownSize = new ResizeMessage(-1, -1);
	})(ResizeMessage = exports.ResizeMessage || (exports.ResizeMessage = {}));
	/**
	 * The namespace for the private module data.
	 */
	var Private;
	(function (Private) {
	    /**
	     * A property descriptor for a widget absolute geometry rect.
	     */
	    Private.rectProperty = new properties_1.AttachedProperty({
	        name: 'rect',
	        create: function () { return ({ top: NaN, left: NaN, width: NaN, height: NaN }); },
	    });
	    /**
	     * An attached property for the widget title object.
	     */
	    Private.titleProperty = new properties_1.AttachedProperty({
	        name: 'title',
	        create: function (owner) { return new title_1.Title({ owner: owner }); },
	    });
	    /**
	     * Create a DOM node for the given widget options.
	     */
	    function createNode(options) {
	        return options.node || document.createElement('div');
	    }
	    Private.createNode = createNode;
	})(Private || (Private = {}));
	
})
/** END DEFINE BLOCK for phosphor@0.6.1/lib/ui/widget.js **/


/** START DEFINE BLOCK for phosphor@0.6.1/lib/algorithm/iteration.js **/
jupyter.define('phosphor@0.6.1/lib/algorithm/iteration.js', function (module, exports, __jupyter_require__) {
	/*-----------------------------------------------------------------------------
	| Copyright (c) 2014-2016, PhosphorJS Contributors
	|
	| Distributed under the terms of the BSD 3-Clause License.
	|
	| The full license is in the file LICENSE, distributed with this software.
	|----------------------------------------------------------------------------*/
	"use strict";
	/**
	 * Create an iterator for an iterable or array-like object.
	 *
	 * @param object - The iterable or array-like object of interest.
	 *
	 * @returns A new iterator for the given object.
	 *
	 * #### Notes
	 * This function allows iteration algorithms to operate on user-defined
	 * iterable types and builtin array-like objects in a uniform fashion.
	 */
	function iter(object) {
	    var it;
	    if (typeof object.iter === 'function') {
	        it = object.iter();
	    }
	    else {
	        it = new ArrayIterator(object, 0);
	    }
	    return it;
	}
	exports.iter = iter;
	/**
	 * Create an array from an iterable of values.
	 *
	 * @param object - The iterable or array-like object of interest.
	 *
	 * @returns A new array of values from the given object.
	 */
	function toArray(object) {
	    var value;
	    var result = [];
	    var it = iter(object);
	    while ((value = it.next()) !== void 0) {
	        result[result.length] = value;
	    }
	    return result;
	}
	exports.toArray = toArray;
	/**
	 * An iterator which is always empty.
	 */
	var EmptyIterator = (function () {
	    /**
	     * Construct a new empty iterator.
	     */
	    function EmptyIterator() {
	    }
	    /**
	     * Create an iterator over the object's values.
	     *
	     * @returns A reference to `this` iterator.
	     */
	    EmptyIterator.prototype.iter = function () {
	        return this;
	    };
	    /**
	     * Create an independent clone of the current iterator.
	     *
	     * @returns A new independent clone of the current iterator.
	     */
	    EmptyIterator.prototype.clone = function () {
	        return new EmptyIterator();
	    };
	    /**
	     * Get the next value from the iterator.
	     *
	     * @returns Always `undefined`.
	     */
	    EmptyIterator.prototype.next = function () {
	        return void 0;
	    };
	    return EmptyIterator;
	}());
	exports.EmptyIterator = EmptyIterator;
	/**
	 * The namespace for the `EmptyIterator` class statics.
	 */
	var EmptyIterator;
	(function (EmptyIterator) {
	    /**
	     * A singleton instance of an empty iterator.
	     */
	    EmptyIterator.instance = new EmptyIterator();
	})(EmptyIterator = exports.EmptyIterator || (exports.EmptyIterator = {}));
	/**
	 * An iterator for an array-like object.
	 *
	 * #### Notes
	 * This iterator can be used for any builtin JS array-like object.
	 */
	var ArrayIterator = (function () {
	    /**
	     * Construct a new array iterator.
	     *
	     * @param source - The array-like object of interest.
	     *
	     * @param start - The starting index for iteration.
	     */
	    function ArrayIterator(source, start) {
	        this._source = source;
	        this._index = start;
	    }
	    /**
	     * Create an iterator over the object's values.
	     *
	     * @returns A reference to `this` iterator.
	     */
	    ArrayIterator.prototype.iter = function () {
	        return this;
	    };
	    /**
	     * Create an independent clone of the current iterator.
	     *
	     * @returns A new independent clone of the current iterator.
	     *
	     * #### Notes
	     * The source array is shared among clones.
	     */
	    ArrayIterator.prototype.clone = function () {
	        return new ArrayIterator(this._source, this._index);
	    };
	    /**
	     * Get the next value from the source array.
	     *
	     * @returns The next value from the source array, or `undefined`
	     *   if the iterator is exhausted.
	     */
	    ArrayIterator.prototype.next = function () {
	        if (this._index >= this._source.length) {
	            return void 0;
	        }
	        return this._source[this._index++];
	    };
	    return ArrayIterator;
	}());
	exports.ArrayIterator = ArrayIterator;
	/**
	 * Invoke a function for each value in an iterable.
	 *
	 * @param object - The iterable or array-like object of interest.
	 *
	 * @param fn - The callback function to invoke for each value.
	 *
	 * #### Notes
	 * Iteration cannot be terminated early.
	 */
	function each(object, fn) {
	    var value;
	    var it = iter(object);
	    while ((value = it.next()) !== void 0) {
	        fn(value);
	    }
	}
	exports.each = each;
	/**
	 * Test whether all values in an iterable satisfy a predicate.
	 *
	 * @param object - The iterable or array-like object of interest.
	 *
	 * @param fn - The predicate function to invoke for each value.
	 *
	 * @returns `true` if all values pass the test, `false` otherwise.
	 *
	 * #### Notes
	 * Iteration terminates on the first `false` predicate result.
	 */
	function every(object, fn) {
	    var value;
	    var it = iter(object);
	    while ((value = it.next()) !== void 0) {
	        if (!fn(value))
	            return false;
	    }
	    return true;
	}
	exports.every = every;
	/**
	 * Test whether any value in an iterable satisfies a predicate.
	 *
	 * @param object - The iterable or array-like object of interest.
	 *
	 * @param fn - The predicate function to invoke for each value.
	 *
	 * @returns `true` if any value passes the test, `false` otherwise.
	 *
	 * #### Notes
	 * Iteration terminates on the first `true` predicate result.
	 */
	function some(object, fn) {
	    var value;
	    var it = iter(object);
	    while ((value = it.next()) !== void 0) {
	        if (fn(value))
	            return true;
	    }
	    return false;
	}
	exports.some = some;
	function reduce(object, fn, initial) {
	    // Setup the iterator and fetch the first value.
	    var it = iter(object);
	    var first = it.next();
	    // An empty iterator and no initial value is an error.
	    if (first === void 0 && initial === void 0) {
	        throw new TypeError('Reduce of empty iterable with no initial value.');
	    }
	    // If the iterator is empty, return the initial value.
	    if (first === void 0) {
	        return initial;
	    }
	    // If the iterator has a single item and no initial value, the
	    // reducer is not invoked and the first item is the return value.
	    var second = it.next();
	    if (second === void 0 && initial === void 0) {
	        return first;
	    }
	    // If iterator has a single item and an initial value is provided,
	    // the reducer is invoked and that result is the return value.
	    if (second === void 0) {
	        return fn(initial, first);
	    }
	    // Setup the initial accumulator value.
	    var accumulator;
	    if (initial === void 0) {
	        accumulator = fn(first, second);
	    }
	    else {
	        accumulator = fn(fn(initial, first), second);
	    }
	    // Iterate the rest of the values, updating the accumulator.
	    var next;
	    while ((next = it.next()) !== void 0) {
	        accumulator = fn(accumulator, next);
	    }
	    // Return the final accumulated value.
	    return accumulator;
	}
	exports.reduce = reduce;
	/**
	 * Filter an iterable for values which pass a test.
	 *
	 * @param object - The iterable or array-like object of interest.
	 *
	 * @param fn - The predicate function to invoke for each value.
	 *
	 * @returns An iterator which yields the values which pass the test.
	 */
	function filter(object, fn) {
	    return new FilterIterator(iter(object), fn);
	}
	exports.filter = filter;
	/**
	 * An iterator which yields values which pass a test.
	 */
	var FilterIterator = (function () {
	    /**
	     * Construct a new filter iterator.
	     *
	     * @param source - The iterator of values of interest.
	     *
	     * @param fn - The predicate function to invoke for each value in
	     *   the iterator. It returns whether the value passes the test.
	     */
	    function FilterIterator(source, fn) {
	        this._source = source;
	        this._fn = fn;
	    }
	    /**
	     * Create an iterator over the object's values.
	     *
	     * @returns A reference to `this` iterator.
	     */
	    FilterIterator.prototype.iter = function () {
	        return this;
	    };
	    /**
	     * Create an independent clone of the current iterator.
	     *
	     * @returns A new independent clone of the current iterator.
	     *
	     * #### Notes
	     * The source iterator must be cloneable.
	     *
	     * The predicate function is shared among clones.
	     */
	    FilterIterator.prototype.clone = function () {
	        return new FilterIterator(this._source.clone(), this._fn);
	    };
	    /**
	     * Get the next value which passes the test.
	     *
	     * @returns The next value from the source iterator which passes
	     *   the predicate, or `undefined` if the iterator is exhausted.
	     */
	    FilterIterator.prototype.next = function () {
	        var value;
	        var fn = this._fn;
	        var it = this._source;
	        while ((value = it.next()) !== void 0) {
	            if (fn(value))
	                return value;
	        }
	        return void 0;
	    };
	    return FilterIterator;
	}());
	exports.FilterIterator = FilterIterator;
	/**
	 * Transform the values of an iterable with a mapping function.
	 *
	 * @param object - The iterable or array-like object of interest.
	 *
	 * @param fn - The mapping function to invoke for each value.
	 *
	 * @returns An iterator which yields the transformed values.
	 */
	function map(object, fn) {
	    return new MapIterator(iter(object), fn);
	}
	exports.map = map;
	/**
	 * An iterator which transforms values using a mapping function.
	 */
	var MapIterator = (function () {
	    /**
	     * Construct a new map iterator.
	     *
	     * @param source - The iterator of values of interest.
	     *
	     * @param fn - The mapping function to invoke for each value in the
	     *   iterator. It returns the transformed value.
	     */
	    function MapIterator(source, fn) {
	        this._source = source;
	        this._fn = fn;
	    }
	    /**
	     * Create an iterator over the object's values.
	     *
	     * @returns A reference to `this` iterator.
	     */
	    MapIterator.prototype.iter = function () {
	        return this;
	    };
	    /**
	     * Create an independent clone of the current iterator.
	     *
	     * @returns A new independent clone of the current iterator.
	     *
	     * #### Notes
	     * The source iterator must be cloneable.
	     *
	     * The mapping function is shared among clones.
	     */
	    MapIterator.prototype.clone = function () {
	        return new MapIterator(this._source.clone(), this._fn);
	    };
	    /**
	     * Get the next mapped value from the source iterator.
	     *
	     * @returns The next value from the source iterator transformed
	     *   by the mapper, or `undefined` if the iterator is exhausted.
	     */
	    MapIterator.prototype.next = function () {
	        var value = this._source.next();
	        if (value === void 0) {
	            return void 0;
	        }
	        return this._fn.call(void 0, value);
	    };
	    return MapIterator;
	}());
	exports.MapIterator = MapIterator;
	/**
	 * Attach an incremental index to an iterable.
	 *
	 * @param object - The iterable or array-like object of interest.
	 *
	 * @param start - The initial value of the index. The default is zero.
	 *
	 * @returns An iterator which yields `[index, value]` tuples.
	 */
	function enumerate(object, start) {
	    if (start === void 0) { start = 0; }
	    return new EnumerateIterator(iter(object), start);
	}
	exports.enumerate = enumerate;
	/**
	 * An iterator which attaches an incremental index to a source.
	 */
	var EnumerateIterator = (function () {
	    /**
	     * Construct a new enumerate iterator.
	     *
	     * @param source - The iterator of values of interest.
	     *
	     * @param start - The initial value of the index.
	     */
	    function EnumerateIterator(source, start) {
	        this._source = source;
	        this._index = start;
	    }
	    /**
	     * Create an iterator over the object's values.
	     *
	     * @returns A reference to `this` iterator.
	     */
	    EnumerateIterator.prototype.iter = function () {
	        return this;
	    };
	    /**
	     * Create an independent clone of the enumerate iterator.
	     *
	     * @returns A new iterator starting with the current value.
	     *
	     * #### Notes
	     * The source iterator must be cloneable.
	     */
	    EnumerateIterator.prototype.clone = function () {
	        return new EnumerateIterator(this._source.clone(), this._index);
	    };
	    /**
	     * Get the next value from the enumeration.
	     *
	     * @returns The next value from the enumeration, or `undefined` if
	     *   the iterator is exhausted.
	     */
	    EnumerateIterator.prototype.next = function () {
	        var value = this._source.next();
	        if (value === void 0) {
	            return void 0;
	        }
	        return [this._index++, value];
	    };
	    return EnumerateIterator;
	}());
	exports.EnumerateIterator = EnumerateIterator;
	/**
	 * Iterate several iterables in lockstep.
	 *
	 * @param objects - The iterables or array-like objects of interest.
	 *
	 * @returns An iterator which yields successive tuples of values where
	 *   each value is taken in turn from the provided iterables. It will
	 *   be as long as the shortest provided iterable.
	 */
	function zip() {
	    var objects = [];
	    for (var _i = 0; _i < arguments.length; _i++) {
	        objects[_i - 0] = arguments[_i];
	    }
	    return new ZipIterator(objects.map(iter));
	}
	exports.zip = zip;
	/**
	 * An iterator which iterates several sources in lockstep.
	 */
	var ZipIterator = (function () {
	    /**
	     * Construct a new zip iterator.
	     *
	     * @param source - The iterators of interest.
	     */
	    function ZipIterator(source) {
	        this._source = source;
	    }
	    /**
	     * Create an iterator over the object's values.
	     *
	     * @returns A reference to `this` iterator.
	     */
	    ZipIterator.prototype.iter = function () {
	        return this;
	    };
	    /**
	     * Create an independent clone of the zip iterator.
	     *
	     * @returns A new iterator starting with the current value.
	     *
	     * #### Notes
	     * The source iterators must be cloneable.
	     */
	    ZipIterator.prototype.clone = function () {
	        return new ZipIterator(this._source.map(function (it) { return it.clone(); }));
	    };
	    /**
	     * Get the next zipped value from the iterator.
	     *
	     * @returns The next zipped value from the iterator, or `undefined`
	     *   when the first source iterator is exhausted.
	     */
	    ZipIterator.prototype.next = function () {
	        var iters = this._source;
	        var result = new Array(iters.length);
	        for (var i = 0, n = iters.length; i < n; ++i) {
	            var value = iters[i].next();
	            if (value === void 0) {
	                return void 0;
	            }
	            result[i] = value;
	        }
	        return result;
	    };
	    return ZipIterator;
	}());
	exports.ZipIterator = ZipIterator;
	/**
	 * Iterate over an iterable using a stepped increment.
	 *
	 * @param object - The iterable or array-like object of interest.
	 *
	 * @param step - The distance to step on each iteration. A value
	 *   of less than `1` will behave the same as a value of `1`.
	 *
	 * @returns An iterator which traverses the iterable step-wise.
	 */
	function stride(object, step) {
	    return new StrideIterator(iter(object), step);
	}
	exports.stride = stride;
	/**
	 * An iterator which traverses a source iterator step-wise.
	 */
	var StrideIterator = (function () {
	    /**
	     * Construct a new stride iterator.
	     *
	     * @param source - The iterator of values of interest.
	     *
	     * @param step - The distance to step on each iteration. A value
	     *   of less than `1` will behave the same as a value of `1`.
	     */
	    function StrideIterator(source, step) {
	        this._source = source;
	        this._step = step;
	    }
	    /**
	     * Create an iterator over the object's values.
	     *
	     * @returns A reference to `this` iterator.
	     */
	    StrideIterator.prototype.iter = function () {
	        return this;
	    };
	    /**
	     * Create an independent clone of the stride iterator.
	     *
	     * @returns A new iterator starting with the current value.
	     *
	     * #### Notes
	     * The source iterator must be cloneable.
	     */
	    StrideIterator.prototype.clone = function () {
	        return new StrideIterator(this._source.clone(), this._step);
	    };
	    /**
	     * Get the next stepped value from the iterator.
	     *
	     * @returns The next stepped value from the iterator, or `undefined`
	     *   when the source iterator is exhausted.
	     */
	    StrideIterator.prototype.next = function () {
	        var value = this._source.next();
	        if (value === void 0) {
	            return void 0;
	        }
	        var step = this._step;
	        while (--step > 0) {
	            this._source.next();
	        }
	        return value;
	    };
	    return StrideIterator;
	}());
	exports.StrideIterator = StrideIterator;
	
})
/** END DEFINE BLOCK for phosphor@0.6.1/lib/algorithm/iteration.js **/


/** START DEFINE BLOCK for phosphor@0.6.1/lib/core/messaging.js **/
jupyter.define('phosphor@0.6.1/lib/core/messaging.js', function (module, exports, __jupyter_require__) {
	/* WEBPACK VAR INJECTION */(function(setImmediate) {"use strict";
	var __extends = (this && this.__extends) || function (d, b) {
	    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
	    function __() { this.constructor = d; }
	    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
	};
	/*-----------------------------------------------------------------------------
	| Copyright (c) 2014-2016, PhosphorJS Contributors
	|
	| Distributed under the terms of the BSD 3-Clause License.
	|
	| The full license is in the file LICENSE, distributed with this software.
	|----------------------------------------------------------------------------*/
	var iteration_1 = __jupyter_require__('phosphor@~0.6.1/lib/algorithm/iteration.js');
	var queue_1 = __jupyter_require__('phosphor@~0.6.1/lib/collections/queue.js');
	/**
	 * A message which can be delivered to a message handler.
	 *
	 * #### Notes
	 * This class may be subclassed to create complex message types.
	 *
	 * **See also:** [[postMessage]] and [[sendMessage]].
	 */
	var Message = (function () {
	    /**
	     * Construct a new message.
	     *
	     * @param type - The type of the message.
	     */
	    function Message(type) {
	        this._type = type;
	    }
	    Object.defineProperty(Message.prototype, "type", {
	        /**
	         * The type of the message.
	         *
	         * #### Notes
	         * This value can be used to cast the message to a derived type.
	         *
	         * This is a read-only property.
	         */
	        get: function () {
	            return this._type;
	        },
	        enumerable: true,
	        configurable: true
	    });
	    Object.defineProperty(Message.prototype, "isConflatable", {
	        /**
	         * Test whether the message is conflatable.
	         *
	         * #### Notes
	         * Message conflation is an advanced topic. Most message types will
	         * not make use of this feature.
	         *
	         * If a conflatable message is posted to the event queue when another
	         * conflatable message of the same type and handler has already been
	         * posted, the `conflate()` method of the existing message will be
	         * invoked. If that method returns `true`, the new message will not
	         * be enqueued. This allows messages to be compressed, so that only
	         * a single instance of the message type is processed per cycle, no
	         * matter how many times messages of that type are posted.
	         *
	         * Custom message types may reimplement this property. The default
	         * implementation is always `false`.
	         *
	         * This is a read-only property.
	         *
	         * **See also:** [[conflateMessage]]
	         */
	        get: function () {
	            return false;
	        },
	        enumerable: true,
	        configurable: true
	    });
	    /**
	     * Conflate this message with another message of the same `type`.
	     *
	     * @param other - A conflatable message of the same `type`.
	     *
	     * @returns `true` if the message was successfully conflated, or
	     *   `false` otherwise.
	     *
	     * #### Notes
	     * Message conflation is an advanced topic. Most message types will
	     * not make use of this feature.
	     *
	     * This method is called automatically by the message loop when the
	     * given message is posted to the handler paired with this message.
	     * This message will already be enqueued and conflatable, and the
	     * given message will have the same `type` and also be conflatable.
	     *
	     * This method should merge the state of the other message into this
	     * message as needed so that when this message is finally delivered
	     * to the handler, it receives the most up-to-date information.
	     *
	     * If this method returns `true`, it signals that the other message
	     * was successfully conflated and it will not be enqueued.
	     *
	     * If this method returns `false`, the other message will be enqueued
	     * for normal delivery.
	     *
	     * Custom message types may reimplement this method. The default
	     * implementation always returns `false`.
	     *
	     * **See also:** [[isConflatable]]
	     */
	    Message.prototype.conflate = function (other) {
	        return false;
	    };
	    return Message;
	}());
	exports.Message = Message;
	/**
	 * A convenience message class which conflates automatically.
	 *
	 * #### Notes
	 * Message conflation is an advanced topic. Most user code will not
	 * make use of this class.
	 *
	 * This message class is useful for creating message instances which
	 * should be conflated, but which have no state other than `type`.
	 *
	 * If conflation of stateful messages is required, a custom `Message`
	 * subclass should be created.
	 */
	var ConflatableMessage = (function (_super) {
	    __extends(ConflatableMessage, _super);
	    function ConflatableMessage() {
	        _super.apply(this, arguments);
	    }
	    Object.defineProperty(ConflatableMessage.prototype, "isConflatable", {
	        /**
	         * Test whether the message is conflatable.
	         *
	         * #### Notes
	         * This property is always `true`.
	         *
	         * This is a read-only property.
	         */
	        get: function () {
	            return true;
	        },
	        enumerable: true,
	        configurable: true
	    });
	    /**
	     * Conflate this message with another message of the same `type`.
	     *
	     * #### Notes
	     * This method always returns `true`.
	     */
	    ConflatableMessage.prototype.conflate = function (other) {
	        return true;
	    };
	    return ConflatableMessage;
	}(Message));
	exports.ConflatableMessage = ConflatableMessage;
	/**
	 * Send a message to a message handler to process immediately.
	 *
	 * @param handler - The handler which should process the message.
	 *
	 * @param msg - The message to deliver to the handler.
	 *
	 * #### Notes
	 * The message will first be sent through any installed message hooks
	 * for the handler. If the message passes all hooks, it will then be
	 * delivered to the `processMessage` method of the handler.
	 *
	 * The message will not be conflated with pending posted messages.
	 *
	 * Exceptions in hooks and handlers will be caught and logged.
	 */
	function sendMessage(handler, msg) {
	    MessageLoop.sendMessage(handler, msg);
	}
	exports.sendMessage = sendMessage;
	/**
	 * Post a message to the message handler to process in the future.
	 *
	 * @param handler - The handler which should process the message.
	 *
	 * @param msg - The message to post to the handler.
	 *
	 * #### Notes
	 * The message will be conflated with the pending posted messages for
	 * the handler, if possible. If the message is not conflated, it will
	 * be queued for normal delivery on the next cycle of the event loop.
	 *
	 * Exceptions in hooks and handlers will be caught and logged.
	 */
	function postMessage(handler, msg) {
	    MessageLoop.postMessage(handler, msg);
	}
	exports.postMessage = postMessage;
	/**
	 * Install a message hook for a message handler.
	 *
	 * @param handler - The message handler of interest.
	 *
	 * @param hook - The message hook to install.
	 *
	 * #### Notes
	 * A message hook is invoked before a message is delivered to the
	 * handler. If the hook returns `false`, no other hooks will be
	 * invoked and the message will not be delivered to the handler.
	 *
	 * The most recently installed message hook is executed first.
	 *
	 * If the hook is already installed, it will be moved to the front.
	 *
	 * **See also:** [[removeMessageHook]]
	 */
	function installMessageHook(handler, hook) {
	    MessageLoop.installMessageHook(handler, hook);
	}
	exports.installMessageHook = installMessageHook;
	/**
	 * Remove an installed message hook for a message handler.
	 *
	 * @param handler - The message handler of interest.
	 *
	 * @param hook - The message hook to remove.
	 *
	 * #### Notes
	 * If the hook is not installed, this is a no-op.
	 *
	 * It is safe to call this function while the hook is executing.
	 */
	function removeMessageHook(handler, hook) {
	    MessageLoop.removeMessageHook(handler, hook);
	}
	exports.removeMessageHook = removeMessageHook;
	/**
	 * Clear all message data associated with a message handler.
	 *
	 * @param handler - The message handler of interest.
	 *
	 * #### Notes
	 * This will clear all pending messages and hooks for the handler.
	 */
	function clearMessageData(handler) {
	    MessageLoop.clearMessageData(handler);
	}
	exports.clearMessageData = clearMessageData;
	/**
	 * The namespace for the global singleton message loop.
	 */
	var MessageLoop;
	(function (MessageLoop) {
	    /**
	     * Send a message to a handler for immediate processing.
	     *
	     * This will first call all message hooks for the handler. If any
	     * hook rejects the message, the message will not be delivered.
	     */
	    function sendMessage(handler, msg) {
	        // Handle the common case of no message hooks.
	        var node = hooks.get(handler);
	        if (node === void 0) {
	            invokeHandler(handler, msg);
	            return;
	        }
	        // Run the message hooks and bail early if any hook returns false.
	        // A null hook indicates the hook was removed during dispatch.
	        for (; node !== null; node = node.next) {
	            if (node.hook !== null && !invokeHook(node.hook, handler, msg)) {
	                return;
	            }
	        }
	        // All message hooks returned true, so invoke the handler.
	        invokeHandler(handler, msg);
	    }
	    MessageLoop.sendMessage = sendMessage;
	    /**
	     * Post a message to a handler for processing in the future.
	     *
	     * This will first conflate the message, if possible. If it cannot
	     * be conflated, it will be queued for delivery on the next cycle
	     * of the event loop.
	     */
	    function postMessage(handler, msg) {
	        // Handle the common case a non-conflatable message first.
	        if (!msg.isConflatable) {
	            enqueueMessage(handler, msg);
	            return;
	        }
	        // Conflate message if possible.
	        var conflated = iteration_1.some(queue, function (posted) {
	            if (posted.handler !== handler) {
	                return false;
	            }
	            if (posted.msg.type !== msg.type) {
	                return false;
	            }
	            if (!posted.msg.isConflatable) {
	                return false;
	            }
	            return posted.msg.conflate(msg);
	        });
	        // If the message was not conflated, enqueue the message.
	        if (!conflated)
	            enqueueMessage(handler, msg);
	    }
	    MessageLoop.postMessage = postMessage;
	    /**
	     * Install a message hook for a handler.
	     *
	     * This will first remove the hook if it exists, then install the
	     * hook in front of other hooks for the handler.
	     */
	    function installMessageHook(handler, hook) {
	        // Remove the message hook if it's already installed.
	        removeMessageHook(handler, hook);
	        // Install the hook at the front of the list.
	        var next = hooks.get(handler) || null;
	        hooks.set(handler, { next: next, hook: hook });
	    }
	    MessageLoop.installMessageHook = installMessageHook;
	    /**
	     * Remove a message hook for a handler, if it exists.
	     */
	    function removeMessageHook(handler, hook) {
	        // Traverse the list and find the matching hook. If found, clear
	        // the reference to the hook and remove the node from the list.
	        // The node's next reference is *not* cleared so that dispatch
	        // may continue when the hook is removed during dispatch.
	        var prev = null;
	        var node = hooks.get(handler) || null;
	        for (; node !== null; prev = node, node = node.next) {
	            if (node.hook === hook) {
	                if (prev === null && node.next === null) {
	                    hooks.delete(handler);
	                }
	                else if (prev === null) {
	                    hooks.set(handler, node.next);
	                }
	                else {
	                    prev.next = node.next;
	                }
	                node.hook = null;
	                return;
	            }
	        }
	    }
	    MessageLoop.removeMessageHook = removeMessageHook;
	    /**
	     * Clear all message data for a handler.
	     *
	     * This will remove all message hooks and clear pending messages.
	     */
	    function clearMessageData(handler) {
	        // Clear all message hooks.
	        var node = hooks.get(handler) || null;
	        for (; node !== null; node = node.next) {
	            node.hook = null;
	        }
	        // Remove the handler from the hooks map.
	        hooks.delete(handler);
	        // Clear all pending messages.
	        iteration_1.each(queue, function (posted) {
	            if (posted.handler === handler) {
	                posted.handler = null;
	            }
	        });
	    }
	    MessageLoop.clearMessageData = clearMessageData;
	    /**
	     * The queue of posted message pairs.
	     */
	    var queue = new queue_1.Queue();
	    /**
	     * A mapping of handler to list of installed message hooks.
	     */
	    var hooks = new WeakMap();
	    /**
	     * A local reference to an event loop callback.
	     */
	    var defer = (function () {
	        var ok = typeof requestAnimationFrame === 'function';
	        return ok ? requestAnimationFrame : setImmediate;
	    })();
	    /**
	     * Whether a message loop cycle is pending.
	     */
	    var cyclePending = false;
	    /**
	     * Invoke a message hook with the specified handler and message.
	     *
	     * Returns the result of the hook, or `true` if the hook throws.
	     *
	     * Exceptions in the hook will be caught and logged.
	     */
	    function invokeHook(hook, handler, msg) {
	        var result;
	        try {
	            result = hook(handler, msg);
	        }
	        catch (err) {
	            result = true;
	            console.error(err);
	        }
	        return result;
	    }
	    /**
	     * Invoke a message handler with the specified message.
	     *
	     * Exceptions in the handler will be caught and logged.
	     */
	    function invokeHandler(handler, msg) {
	        try {
	            handler.processMessage(msg);
	        }
	        catch (err) {
	            console.error(err);
	        }
	    }
	    /**
	     * Add a message to the end of the message queue.
	     *
	     * This will automatically schedule a cycle of the loop.
	     */
	    function enqueueMessage(handler, msg) {
	        queue.pushBack({ handler: handler, msg: msg });
	        scheduleMessageLoop();
	    }
	    /**
	     * Schedule a message loop cycle to process any pending messages.
	     *
	     * This is a no-op if a loop cycle is already pending.
	     */
	    function scheduleMessageLoop() {
	        if (!cyclePending) {
	            defer(runMessageLoop);
	            cyclePending = true;
	        }
	    }
	    /**
	     * Run an iteration of the message loop.
	     *
	     * This will process all pending messages in the queue. If a message
	     * is added to the queue while the message loop is running, it will
	     * be processed on the next cycle of the loop.
	     */
	    function runMessageLoop() {
	        // Clear the pending flag so the next loop can be scheduled.
	        cyclePending = false;
	        // If the queue is empty, there is nothing else to do.
	        if (queue.isEmpty) {
	            return;
	        }
	        // Add a sentinel value to the end of the queue. The queue will
	        // only be processed up to the sentinel. Messages posted during
	        // this cycle will execute on the next cycle.
	        var sentinel = { handler: null, msg: null };
	        queue.pushBack(sentinel);
	        // Enter the message loop.
	        while (!queue.isEmpty) {
	            // Remove the first posted message in the queue.
	            var posted = queue.popFront();
	            // If the value is the sentinel, exit the loop.
	            if (posted === sentinel) {
	                return;
	            }
	            // Dispatch the message if the handler has not been cleared.
	            if (posted.handler !== null) {
	                sendMessage(posted.handler, posted.msg);
	            }
	        }
	    }
	})(MessageLoop || (MessageLoop = {}));
	
	/* WEBPACK VAR INJECTION */}.call(exports, __jupyter_require__('timers-browserify@1.4.2/main.js').setImmediate))
})
/** END DEFINE BLOCK for phosphor@0.6.1/lib/core/messaging.js **/


/** START DEFINE BLOCK for timers-browserify@1.4.2/main.js **/
jupyter.define('timers-browserify@1.4.2/main.js', function (module, exports, __jupyter_require__) {
	/* WEBPACK VAR INJECTION */(function(setImmediate, clearImmediate) {var nextTick = __jupyter_require__('process@~0.11.0/browser.js').nextTick;
	var apply = Function.prototype.apply;
	var slice = Array.prototype.slice;
	var immediateIds = {};
	var nextImmediateId = 0;
	
	// DOM APIs, for completeness
	
	exports.setTimeout = function() {
	  return new Timeout(apply.call(setTimeout, window, arguments), clearTimeout);
	};
	exports.setInterval = function() {
	  return new Timeout(apply.call(setInterval, window, arguments), clearInterval);
	};
	exports.clearTimeout =
	exports.clearInterval = function(timeout) { timeout.close(); };
	
	function Timeout(id, clearFn) {
	  this._id = id;
	  this._clearFn = clearFn;
	}
	Timeout.prototype.unref = Timeout.prototype.ref = function() {};
	Timeout.prototype.close = function() {
	  this._clearFn.call(window, this._id);
	};
	
	// Does not start the time, just sets up the members needed.
	exports.enroll = function(item, msecs) {
	  clearTimeout(item._idleTimeoutId);
	  item._idleTimeout = msecs;
	};
	
	exports.unenroll = function(item) {
	  clearTimeout(item._idleTimeoutId);
	  item._idleTimeout = -1;
	};
	
	exports._unrefActive = exports.active = function(item) {
	  clearTimeout(item._idleTimeoutId);
	
	  var msecs = item._idleTimeout;
	  if (msecs >= 0) {
	    item._idleTimeoutId = setTimeout(function onTimeout() {
	      if (item._onTimeout)
	        item._onTimeout();
	    }, msecs);
	  }
	};
	
	// That's not how node.js implements it but the exposed api is the same.
	exports.setImmediate = typeof setImmediate === "function" ? setImmediate : function(fn) {
	  var id = nextImmediateId++;
	  var args = arguments.length < 2 ? false : slice.call(arguments, 1);
	
	  immediateIds[id] = true;
	
	  nextTick(function onNextTick() {
	    if (immediateIds[id]) {
	      // fn.call() is faster so we optimize for the common use-case
	      // @see http://jsperf.com/call-apply-segu
	      if (args) {
	        fn.apply(null, args);
	      } else {
	        fn.call(null);
	      }
	      // Prevent ids from leaking
	      exports.clearImmediate(id);
	    }
	  });
	
	  return id;
	};
	
	exports.clearImmediate = typeof clearImmediate === "function" ? clearImmediate : function(id) {
	  delete immediateIds[id];
	};
	/* WEBPACK VAR INJECTION */}.call(exports, __jupyter_require__('timers-browserify@1.4.2/main.js').setImmediate, __jupyter_require__('timers-browserify@1.4.2/main.js').clearImmediate))
})
/** END DEFINE BLOCK for timers-browserify@1.4.2/main.js **/


/** START DEFINE BLOCK for process@0.11.9/browser.js **/
jupyter.define('process@0.11.9/browser.js', function (module, exports, __jupyter_require__) {
	// shim for using process in browser
	var process = module.exports = {};
	
	// cached from whatever global is present so that test runners that stub it
	// don't break things.  But we need to wrap it in a try catch in case it is
	// wrapped in strict mode code which doesn't define any globals.  It's inside a
	// function because try/catches deoptimize in certain engines.
	
	var cachedSetTimeout;
	var cachedClearTimeout;
	
	function defaultSetTimout() {
	    throw new Error('setTimeout has not been defined');
	}
	function defaultClearTimeout () {
	    throw new Error('clearTimeout has not been defined');
	}
	(function () {
	    try {
	        if (typeof setTimeout === 'function') {
	            cachedSetTimeout = setTimeout;
	        } else {
	            cachedSetTimeout = defaultSetTimout;
	        }
	    } catch (e) {
	        cachedSetTimeout = defaultSetTimout;
	    }
	    try {
	        if (typeof clearTimeout === 'function') {
	            cachedClearTimeout = clearTimeout;
	        } else {
	            cachedClearTimeout = defaultClearTimeout;
	        }
	    } catch (e) {
	        cachedClearTimeout = defaultClearTimeout;
	    }
	} ())
	function runTimeout(fun) {
	    if (cachedSetTimeout === setTimeout) {
	        //normal enviroments in sane situations
	        return setTimeout(fun, 0);
	    }
	    // if setTimeout wasn't available but was latter defined
	    if ((cachedSetTimeout === defaultSetTimout || !cachedSetTimeout) && setTimeout) {
	        cachedSetTimeout = setTimeout;
	        return setTimeout(fun, 0);
	    }
	    try {
	        // when when somebody has screwed with setTimeout but no I.E. maddness
	        return cachedSetTimeout(fun, 0);
	    } catch(e){
	        try {
	            // When we are in I.E. but the script has been evaled so I.E. doesn't trust the global object when called normally
	            return cachedSetTimeout.call(null, fun, 0);
	        } catch(e){
	            // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error
	            return cachedSetTimeout.call(this, fun, 0);
	        }
	    }
	
	
	}
	function runClearTimeout(marker) {
	    if (cachedClearTimeout === clearTimeout) {
	        //normal enviroments in sane situations
	        return clearTimeout(marker);
	    }
	    // if clearTimeout wasn't available but was latter defined
	    if ((cachedClearTimeout === defaultClearTimeout || !cachedClearTimeout) && clearTimeout) {
	        cachedClearTimeout = clearTimeout;
	        return clearTimeout(marker);
	    }
	    try {
	        // when when somebody has screwed with setTimeout but no I.E. maddness
	        return cachedClearTimeout(marker);
	    } catch (e){
	        try {
	            // When we are in I.E. but the script has been evaled so I.E. doesn't  trust the global object when called normally
	            return cachedClearTimeout.call(null, marker);
	        } catch (e){
	            // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error.
	            // Some versions of I.E. have different rules for clearTimeout vs setTimeout
	            return cachedClearTimeout.call(this, marker);
	        }
	    }
	
	
	
	}
	var queue = [];
	var draining = false;
	var currentQueue;
	var queueIndex = -1;
	
	function cleanUpNextTick() {
	    if (!draining || !currentQueue) {
	        return;
	    }
	    draining = false;
	    if (currentQueue.length) {
	        queue = currentQueue.concat(queue);
	    } else {
	        queueIndex = -1;
	    }
	    if (queue.length) {
	        drainQueue();
	    }
	}
	
	function drainQueue() {
	    if (draining) {
	        return;
	    }
	    var timeout = runTimeout(cleanUpNextTick);
	    draining = true;
	
	    var len = queue.length;
	    while(len) {
	        currentQueue = queue;
	        queue = [];
	        while (++queueIndex < len) {
	            if (currentQueue) {
	                currentQueue[queueIndex].run();
	            }
	        }
	        queueIndex = -1;
	        len = queue.length;
	    }
	    currentQueue = null;
	    draining = false;
	    runClearTimeout(timeout);
	}
	
	process.nextTick = function (fun) {
	    var args = new Array(arguments.length - 1);
	    if (arguments.length > 1) {
	        for (var i = 1; i < arguments.length; i++) {
	            args[i - 1] = arguments[i];
	        }
	    }
	    queue.push(new Item(fun, args));
	    if (queue.length === 1 && !draining) {
	        runTimeout(drainQueue);
	    }
	};
	
	// v8 likes predictible objects
	function Item(fun, array) {
	    this.fun = fun;
	    this.array = array;
	}
	Item.prototype.run = function () {
	    this.fun.apply(null, this.array);
	};
	process.title = 'browser';
	process.browser = true;
	process.env = {};
	process.argv = [];
	process.version = ''; // empty string to avoid regexp issues
	process.versions = {};
	
	function noop() {}
	
	process.on = noop;
	process.addListener = noop;
	process.once = noop;
	process.off = noop;
	process.removeListener = noop;
	process.removeAllListeners = noop;
	process.emit = noop;
	
	process.binding = function (name) {
	    throw new Error('process.binding is not supported');
	};
	
	process.cwd = function () { return '/' };
	process.chdir = function (dir) {
	    throw new Error('process.chdir is not supported');
	};
	process.umask = function() { return 0; };
	
})
/** END DEFINE BLOCK for process@0.11.9/browser.js **/


/** START DEFINE BLOCK for phosphor@0.6.1/lib/collections/queue.js **/
jupyter.define('phosphor@0.6.1/lib/collections/queue.js', function (module, exports, __jupyter_require__) {
	"use strict";
	/*-----------------------------------------------------------------------------
	| Copyright (c) 2014-2016, PhosphorJS Contributors
	|
	| Distributed under the terms of the BSD 3-Clause License.
	|
	| The full license is in the file LICENSE, distributed with this software.
	|----------------------------------------------------------------------------*/
	var iteration_1 = __jupyter_require__('phosphor@~0.6.1/lib/algorithm/iteration.js');
	/**
	 * A generic FIFO queue data structure.
	 */
	var Queue = (function () {
	    /**
	     * Construct a new queue.
	     *
	     * @param values - The initial values for the queue.
	     */
	    function Queue(values) {
	        var _this = this;
	        this._length = 0;
	        this._front = null;
	        this._back = null;
	        if (values)
	            iteration_1.each(values, function (value) { _this.pushBack(value); });
	    }
	    Object.defineProperty(Queue.prototype, "isEmpty", {
	        /**
	         * Test whether the queue is empty.
	         *
	         * @returns `true` if the queue is empty, `false` otherwise.
	         *
	         * #### Notes
	         * This is a read-only property.
	         *
	         * #### Complexity
	         * Constant.
	         *
	         * #### Iterator Validity
	         * No changes.
	         */
	        get: function () {
	            return this._length === 0;
	        },
	        enumerable: true,
	        configurable: true
	    });
	    Object.defineProperty(Queue.prototype, "length", {
	        /**
	         * Get the length of the queue.
	         *
	         * @return The number of values in the queue.
	         *
	         * #### Notes
	         * This is a read-only property.
	         *
	         * #### Complexity
	         * Constant.
	         *
	         * #### Iterator Validity
	         * No changes.
	         */
	        get: function () {
	            return this._length;
	        },
	        enumerable: true,
	        configurable: true
	    });
	    Object.defineProperty(Queue.prototype, "front", {
	        /**
	         * Get the value at the front of the queue.
	         *
	         * @returns The value at the front of the queue, or `undefined` if
	         *   the queue is empty.
	         *
	         * #### Notes
	         * This is a read-only property.
	         *
	         * #### Complexity
	         * Constant.
	         *
	         * #### Iterator Validity
	         * No changes.
	         */
	        get: function () {
	            return this._front ? this._front.value : void 0;
	        },
	        enumerable: true,
	        configurable: true
	    });
	    Object.defineProperty(Queue.prototype, "back", {
	        /**
	         * Get the value at the back of the queue.
	         *
	         * @returns The value at the back of the queue, or `undefined` if
	         *   the queue is empty.
	         *
	         * #### Notes
	         * This is a read-only property.
	         *
	         * #### Complexity
	         * Constant.
	         *
	         * #### Iterator Validity
	         * No changes.
	         */
	        get: function () {
	            return this._back ? this._back.value : void 0;
	        },
	        enumerable: true,
	        configurable: true
	    });
	    /**
	     * Create an iterator over the values in the queue.
	     *
	     * @returns A new iterator starting at the front of the queue.
	     *
	     * #### Complexity
	     * Constant.
	     *
	     * #### Iterator Validity
	     * No changes.
	     */
	    Queue.prototype.iter = function () {
	        return new QueueIterator(this._front);
	    };
	    /**
	     * Add a value to the back of the queue.
	     *
	     * @param value - The value to add to the back of the queue.
	     *
	     * @returns The new length of the queue.
	     *
	     * #### Complexity
	     * Constant.
	     *
	     * #### Iterator Validity
	     * No changes.
	     */
	    Queue.prototype.pushBack = function (value) {
	        var node = new QueueNode(value);
	        if (this._length === 0) {
	            this._front = node;
	            this._back = node;
	        }
	        else {
	            this._back.next = node;
	            this._back = node;
	        }
	        return ++this._length;
	    };
	    /**
	     * Remove and return the value at the front of the queue.
	     *
	     * @returns The value at the front of the queue, or `undefined` if
	     *   the queue is empty.
	     *
	     * #### Complexity
	     * Constant.
	     *
	     * #### Iterator Validity
	     * Iterators pointing at the removed value are invalidated.
	     */
	    Queue.prototype.popFront = function () {
	        if (this._length === 0) {
	            return void 0;
	        }
	        var node = this._front;
	        if (this._length === 1) {
	            this._front = null;
	            this._back = null;
	        }
	        else {
	            this._front = node.next;
	            node.next = null;
	        }
	        this._length--;
	        return node.value;
	    };
	    /**
	     * Remove all values from the queue.
	     *
	     * #### Complexity
	     * Linear.
	     *
	     * #### Iterator Validity
	     * All current iterators are invalidated.
	     */
	    Queue.prototype.clear = function () {
	        var node = this._front;
	        while (node) {
	            var next = node.next;
	            node.next = null;
	            node = next;
	        }
	        this._length = 0;
	        this._front = null;
	        this._back = null;
	    };
	    /**
	     * Swap the contents of the queue with the contents of another.
	     *
	     * @param other - The other queue holding the contents to swap.
	     *
	     * #### Complexity
	     * Constant.
	     *
	     * #### Iterator Validity
	     * All current iterators remain valid, but will now point to the
	     * contents of the other queue involved in the swap.
	     */
	    Queue.prototype.swap = function (other) {
	        var length = other._length;
	        var front = other._front;
	        var back = other._back;
	        other._length = this._length;
	        other._front = this._front;
	        other._back = this._back;
	        this._length = length;
	        this._front = front;
	        this._back = back;
	    };
	    return Queue;
	}());
	exports.Queue = Queue;
	/**
	 * An iterator for a queue.
	 */
	var QueueIterator = (function () {
	    /**
	     * Construct a new queue iterator.
	     *
	     * @param node - The node at the front of range.
	     */
	    function QueueIterator(node) {
	        this._node = node;
	    }
	    /**
	     * Create an iterator over the object's values.
	     *
	     * @returns A reference to `this` iterator.
	     */
	    QueueIterator.prototype.iter = function () {
	        return this;
	    };
	    /**
	     * Create an independent clone of the queue iterator.
	     *
	     * @returns A new iterator starting with the current value.
	     */
	    QueueIterator.prototype.clone = function () {
	        return new QueueIterator(this._node);
	    };
	    /**
	     * Get the next value from the queue.
	     *
	     * @returns The next value from the queue, or `undefined` if the
	     *   iterator is exhausted.
	     */
	    QueueIterator.prototype.next = function () {
	        if (!this._node) {
	            return void 0;
	        }
	        var value = this._node.value;
	        this._node = this._node.next;
	        return value;
	    };
	    return QueueIterator;
	}());
	/**
	 * The node type for a queue.
	 */
	var QueueNode = (function () {
	    /**
	     * Construct a new queue node.
	     *
	     * @param value - The value for the node.
	     */
	    function QueueNode(value) {
	        /**
	         * The next node the queue.
	         */
	        this.next = null;
	        this.value = value;
	    }
	    return QueueNode;
	}());
	
})
/** END DEFINE BLOCK for phosphor@0.6.1/lib/collections/queue.js **/


/** START DEFINE BLOCK for phosphor@0.6.1/lib/core/properties.js **/
jupyter.define('phosphor@0.6.1/lib/core/properties.js', function (module, exports, __jupyter_require__) {
	/*-----------------------------------------------------------------------------
	| Copyright (c) 2014-2016, PhosphorJS Contributors
	|
	| Distributed under the terms of the BSD 3-Clause License.
	|
	| The full license is in the file LICENSE, distributed with this software.
	|----------------------------------------------------------------------------*/
	"use strict";
	/**
	 * A class which attaches a value to an external object.
	 *
	 * #### Notes
	 * Attached properties are used to extend the state of an object with
	 * semantic data from an unrelated class. They also encapsulate value
	 * creation, coercion, and notification.
	 *
	 * Because attached property values are stored in a hash table, which
	 * in turn is stored in a WeakMap keyed on the owner object, there is
	 * non-trivial storage overhead involved in their use. The pattern is
	 * therefore best used for the storage of rare data.
	 */
	var AttachedProperty = (function () {
	    /**
	     * Construct a new attached property.
	     *
	     * @param options - The options for initializing the property.
	     */
	    function AttachedProperty(options) {
	        this._pid = nextPID();
	        this._name = options.name;
	        this._value = options.value;
	        this._create = options.create;
	        this._coerce = options.coerce;
	        this._compare = options.compare;
	        this._changed = options.changed;
	    }
	    Object.defineProperty(AttachedProperty.prototype, "name", {
	        /**
	         * Get the human readable name for the property.
	         *
	         * #### Notes
	         * This is a read-only property.
	         */
	        get: function () {
	            return this._name;
	        },
	        enumerable: true,
	        configurable: true
	    });
	    /**
	     * Get the current value of the property for a given owner.
	     *
	     * @param owner - The property owner of interest.
	     *
	     * @returns The current value of the property.
	     *
	     * #### Notes
	     * If the value has not yet been set, the default value will be
	     * computed and assigned as the current value of the property.
	     */
	    AttachedProperty.prototype.get = function (owner) {
	        var value;
	        var map = ensureMap(owner);
	        if (this._pid in map) {
	            value = map[this._pid];
	        }
	        else {
	            value = map[this._pid] = this._createValue(owner);
	        }
	        return value;
	    };
	    /**
	     * Set the current value of the property for a given owner.
	     *
	     * @param owner - The property owner of interest.
	     *
	     * @param value - The value for the property.
	     *
	     * #### Notes
	     * If the value has not yet been set, the default value will be
	     * computed and used as the previous value for the comparison.
	     */
	    AttachedProperty.prototype.set = function (owner, value) {
	        var oldValue;
	        var map = ensureMap(owner);
	        if (this._pid in map) {
	            oldValue = map[this._pid];
	        }
	        else {
	            oldValue = map[this._pid] = this._createValue(owner);
	        }
	        var newValue = this._coerceValue(owner, value);
	        this._maybeNotify(owner, oldValue, map[this._pid] = newValue);
	    };
	    /**
	     * Explicitly coerce the current property value for a given owner.
	     *
	     * @param owner - The property owner of interest.
	     *
	     * #### Notes
	     * If the value has not yet been set, the default value will be
	     * computed and used as the previous value for the comparison.
	     */
	    AttachedProperty.prototype.coerce = function (owner) {
	        var oldValue;
	        var map = ensureMap(owner);
	        if (this._pid in map) {
	            oldValue = map[this._pid];
	        }
	        else {
	            oldValue = map[this._pid] = this._createValue(owner);
	        }
	        var newValue = this._coerceValue(owner, oldValue);
	        this._maybeNotify(owner, oldValue, map[this._pid] = newValue);
	    };
	    /**
	     * Get or create the default value for the given owner.
	     */
	    AttachedProperty.prototype._createValue = function (owner) {
	        var create = this._create;
	        return create ? create(owner) : this._value;
	    };
	    /**
	     * Coerce the value for the given owner.
	     */
	    AttachedProperty.prototype._coerceValue = function (owner, value) {
	        var coerce = this._coerce;
	        return coerce ? coerce(owner, value) : value;
	    };
	    /**
	     * Compare the old value and new value for equality.
	     */
	    AttachedProperty.prototype._compareValue = function (oldValue, newValue) {
	        var compare = this._compare;
	        return compare ? compare(oldValue, newValue) : oldValue === newValue;
	    };
	    /**
	     * Run the change notification if the given values are different.
	     */
	    AttachedProperty.prototype._maybeNotify = function (owner, oldValue, newValue) {
	        if (!this._changed || this._compareValue(oldValue, newValue)) {
	            return;
	        }
	        this._changed.call(void 0, owner, oldValue, newValue);
	    };
	    return AttachedProperty;
	}());
	exports.AttachedProperty = AttachedProperty;
	/**
	 * Clear the stored property data for the given property owner.
	 *
	 * @param owner - The property owner of interest.
	 *
	 * #### Notes
	 * This will clear all property values for the owner, but it will
	 * **not** run the change notification for any of the properties.
	 */
	function clearPropertyData(owner) {
	    ownerData.delete(owner);
	}
	exports.clearPropertyData = clearPropertyData;
	/**
	 * A weak mapping of property owner to property map.
	 */
	var ownerData = new WeakMap();
	/**
	 * A function which computes successive unique property ids.
	 */
	var nextPID = (function () {
	    var id = 0;
	    return function () {
	        var rand = Math.random();
	        var stem = ("" + rand).slice(2);
	        return "pid-" + stem + "-" + id++;
	    };
	})();
	/**
	 * Lookup the data map for the property owner.
	 *
	 * This will create the map if one does not already exist.
	 */
	function ensureMap(owner) {
	    var map = ownerData.get(owner);
	    if (map !== void 0)
	        return map;
	    map = Object.create(null);
	    ownerData.set(owner, map);
	    return map;
	}
	
})
/** END DEFINE BLOCK for phosphor@0.6.1/lib/core/properties.js **/


/** START DEFINE BLOCK for phosphor@0.6.1/lib/core/signaling.js **/
jupyter.define('phosphor@0.6.1/lib/core/signaling.js', function (module, exports, __jupyter_require__) {
	/* WEBPACK VAR INJECTION */(function(setImmediate) {/*-----------------------------------------------------------------------------
	| Copyright (c) 2014-2016, PhosphorJS Contributors
	|
	| Distributed under the terms of the BSD 3-Clause License.
	|
	| The full license is in the file LICENSE, distributed with this software.
	|----------------------------------------------------------------------------*/
	"use strict";
	/**
	 * Define a signal property on a prototype object.
	 *
	 * @param target - The prototype for the class of interest.
	 *
	 * @param name - The name of the signal property.
	 *
	 * #### Notes
	 * The defined signal property is read-only.
	 *
	 * #### Example
	 * ```typescript
	 * class SomeClass {
	 *   valueChanged: ISignal<SomeClass, number>;
	 * }
	 *
	 * defineSignal(SomeClass.prototype, 'valueChanged');
	 */
	function defineSignal(target, name) {
	    var token = Object.freeze({});
	    Object.defineProperty(target, name, {
	        get: function () { return new Signal(this, token); }
	    });
	}
	exports.defineSignal = defineSignal;
	/**
	 * Remove all connections where the given object is the sender.
	 *
	 * @param sender - The sender object of interest.
	 *
	 * #### Example
	 * ```typescript
	 * disconnectSender(someObject);
	 * ```
	 */
	function disconnectSender(sender) {
	    // If there are no receivers, there is nothing to do.
	    var receiverList = senderData.get(sender);
	    if (receiverList === void 0) {
	        return;
	    }
	    // Clear the connections and schedule a cleanup of the
	    // receiver's corresponding list of sender connections.
	    for (var i = 0, n = receiverList.length; i < n; ++i) {
	        var conn = receiverList[i];
	        var senderList = receiverData.get(conn.thisArg || conn.slot);
	        scheduleCleanup(senderList);
	        conn.token = null;
	    }
	    // Schedule a cleanup of the receiver list.
	    scheduleCleanup(receiverList);
	}
	exports.disconnectSender = disconnectSender;
	/**
	 * Remove all connections where the given object is the receiver.
	 *
	 * @param receiver - The receiver object of interest.
	 *
	 * #### Notes
	 * If a `thisArg` is provided when connecting a signal, that object
	 * is considered the receiver. Otherwise, the `callback` is used as
	 * the receiver.
	 *
	 * #### Example
	 * ```typescript
	 * // disconnect a regular object receiver
	 * disconnectReceiver(myObject);
	 *
	 * // disconnect a plain callback receiver
	 * disconnectReceiver(myCallback);
	 * ```
	 */
	function disconnectReceiver(receiver) {
	    // If there are no senders, there is nothing to do.
	    var senderList = receiverData.get(receiver);
	    if (senderList === void 0) {
	        return;
	    }
	    // Clear the connections and schedule a cleanup of the
	    // senders's corresponding list of receiver connections.
	    for (var i = 0, n = senderList.length; i < n; ++i) {
	        var conn = senderList[i];
	        var receiverList = senderData.get(conn.sender);
	        scheduleCleanup(receiverList);
	        conn.token = null;
	    }
	    // Schedule a cleanup of the sender list.
	    scheduleCleanup(senderList);
	}
	exports.disconnectReceiver = disconnectReceiver;
	/**
	 * Clear all signal data associated with the given object.
	 *
	 * @param obj - The object for which the signal data should be cleared.
	 *
	 * #### Notes
	 * This removes all signal connections where the object is used as
	 * either the sender or the receiver.
	 *
	 * #### Example
	 * ```typescript
	 * clearSignalData(someObject);
	 * ```
	 */
	function clearSignalData(obj) {
	    disconnectSender(obj);
	    disconnectReceiver(obj);
	}
	exports.clearSignalData = clearSignalData;
	/**
	 * A concrete implementation of `ISignal`.
	 */
	var Signal = (function () {
	    /**
	     * Construct a new signal.
	     *
	     * @param sender - The object which owns the signal.
	     *
	     * @param token - The unique token identifying the signal.
	     */
	    function Signal(sender, token) {
	        this._sender = sender;
	        this._token = token;
	    }
	    /**
	     * Connect a slot to the signal.
	     *
	     * @param slot - The slot to invoke when the signal is emitted.
	     *
	     * @param thisArg - The `this` context for the slot. If provided,
	     *   this must be a non-primitive object.
	     *
	     * @returns `true` if the connection succeeds, `false` otherwise.
	     */
	    Signal.prototype.connect = function (slot, thisArg) {
	        return connect(this._sender, this._token, slot, thisArg);
	    };
	    /**
	     * Disconnect a slot from the signal.
	     *
	     * @param slot - The slot to disconnect from the signal.
	     *
	     * @param thisArg - The `this` context for the slot. If provided,
	     *   this must be a non-primitive object.
	     *
	     * @returns `true` if the connection is removed, `false` otherwise.
	     */
	    Signal.prototype.disconnect = function (slot, thisArg) {
	        return disconnect(this._sender, this._token, slot, thisArg);
	    };
	    /**
	     * Emit the signal and invoke the connected slots.
	     *
	     * @param args - The args to pass to the connected slots.
	     */
	    Signal.prototype.emit = function (args) {
	        emit(this._sender, this._token, args);
	    };
	    return Signal;
	}());
	/**
	 * A weak mapping of sender to list of receiver connections.
	 */
	var senderData = new WeakMap();
	/**
	 * A weak mapping of receiver to list of sender connections.
	 */
	var receiverData = new WeakMap();
	/**
	 * A set of connection lists which are pending cleanup.
	 */
	var dirtySet = new Set();
	/**
	 * A local reference to an event loop callback.
	 */
	var defer = (function () {
	    var ok = typeof requestAnimationFrame === 'function';
	    return ok ? requestAnimationFrame : setImmediate;
	})();
	/**
	 * Connect a slot to a signal.
	 *
	 * @param sender - The object emitting the signal.
	 *
	 * @param token - The unique token for the signal.
	 *
	 * @param slot - The slot to connect to the signal.
	 *
	 * @param thisArg - The `this` context for the slot.
	 *
	 * @returns `true` if the connection succeeds, `false` otherwise.
	 *
	 * #### Notes
	 * Signal connections are unique. If a connection already exists for
	 * the given `slot` and `thisArg`, this function returns `false`.
	 *
	 * A newly connected slot will not be invoked until the next time the
	 * signal is emitted, even if the slot is connected while the signal
	 * is dispatching.
	 */
	function connect(sender, token, slot, thisArg) {
	    // Coerce a `null` thisArg to `undefined`.
	    thisArg = thisArg || void 0;
	    // Ensure the sender's receiver list is created.
	    var receiverList = senderData.get(sender);
	    if (receiverList === void 0) {
	        receiverList = [];
	        senderData.set(sender, receiverList);
	    }
	    // Bail if a matching connection already exists.
	    if (findConnection(receiverList, token, slot, thisArg) !== null) {
	        return false;
	    }
	    // Ensure the receiver's sender list is created.
	    var receiver = thisArg || slot;
	    var senderList = receiverData.get(receiver);
	    if (senderList === void 0) {
	        senderList = [];
	        receiverData.set(receiver, senderList);
	    }
	    // Create a new connection and add it to the end of each list.
	    var connection = { sender: sender, token: token, slot: slot, thisArg: thisArg };
	    receiverList.push(connection);
	    senderList.push(connection);
	    // Indicate a successful connection.
	    return true;
	}
	/**
	 * Disconnect a slot from a signal.
	 *
	 * @param sender - The object emitting the signal.
	 *
	 * @param token - The unique token for the signal.
	 *
	 * @param slot - The slot to disconnect from the signal.
	 *
	 * @param thisArg - The `this` context for the slot.
	 *
	 * @returns `true` if the connection is removed, `false` otherwise.
	 *
	 * #### Notes
	 * If no connection exists for the given `slot` and `thisArg`, this
	 * function returns `false`.
	 *
	 * A disconnected slot will no longer be invoked, even if the slot
	 * is disconnected while the signal is dispatching.
	 */
	function disconnect(sender, token, slot, thisArg) {
	    // Coerce a `null` thisArg to `undefined`.
	    thisArg = thisArg || void 0;
	    // Lookup the list of receivers, and bail if none exist.
	    var receiverList = senderData.get(sender);
	    if (receiverList === void 0) {
	        return false;
	    }
	    // Bail if no matching connection exits.
	    var conn = findConnection(receiverList, token, slot, thisArg);
	    if (conn === null) {
	        return false;
	    }
	    // Lookup the list of senders, which is now known to exist.
	    var senderList = receiverData.get(thisArg || slot);
	    // Clear the connection and schedule list cleanup.
	    conn.token = null;
	    scheduleCleanup(receiverList);
	    scheduleCleanup(senderList);
	    // Indicate a successful disconnection.
	    return true;
	}
	/**
	 * Emit a signal and invoke the connected slots.
	 *
	 * @param sender - The object emitting the signal.
	 *
	 * @param token - The unique token for the signal.
	 *
	 * @param args - The args to pass to the connected slots.
	 *
	 * #### Notes
	 * Connected slots are invoked synchronously, in the order in which
	 * they are connected.
	 *
	 * Exceptions thrown by connected slots will be caught and logged.
	 */
	function emit(sender, token, args) {
	    // If there are no receivers, there is nothing to do.
	    var receiverList = senderData.get(sender);
	    if (receiverList === void 0) {
	        return;
	    }
	    // Invoke the connections which match the given token.
	    for (var i = 0, n = receiverList.length; i < n; ++i) {
	        var conn = receiverList[i];
	        if (conn.token === token) {
	            invokeSlot(conn, args);
	        }
	    }
	}
	/**
	 * Safely invoke a non-empty connection.
	 *
	 * @param conn - The connection of interest
	 *
	 * @param args - The arguments to pass to the slot.
	 *
	 * #### Notes
	 * Any exception thrown by the slot will be caught and logged.
	 */
	function invokeSlot(conn, args) {
	    try {
	        conn.slot.call(conn.thisArg, conn.sender, args);
	    }
	    catch (err) {
	        console.error(err);
	    }
	}
	/**
	 * Find a connection which matches the given parameters.
	 *
	 * @param list - The list of connections to search.
	 *
	 * @param token - The unique token for the signal.
	 *
	 * @param slot - The slot of interest.
	 *
	 * @param thisArg - The `this` context for the slot.
	 *
	 * @returns The first connection which matches the supplied parameters,
	 *   or null if no matching connection is found.
	 */
	function findConnection(list, token, slot, thisArg) {
	    for (var i = 0, n = list.length; i < n; ++i) {
	        var conn = list[i];
	        if (conn.token === token &&
	            conn.slot === slot &&
	            conn.thisArg === thisArg) {
	            return conn;
	        }
	    }
	    return null;
	}
	/**
	 * Schedule a cleanup of a connection list.
	 *
	 * @param list - The list of connections to cleanup.
	 *
	 * #### Notes
	 * This will add the list to the dirty set and schedule a deferred
	 * cleanup of the list contents. On cleanup, any connection with a
	 * null token will be removed from the array.
	 */
	function scheduleCleanup(list) {
	    if (dirtySet.size === 0) {
	        defer(cleanupDirtySet);
	    }
	    dirtySet.add(list);
	}
	/**
	 * Cleanup the connection lists in the dirty set.
	 *
	 * #### Notes
	 * This function should only be invoked asynchronously, when the stack
	 * frame is guaranteed to not be on the path of a signal dispatch.
	 */
	function cleanupDirtySet() {
	    dirtySet.forEach(cleanupList);
	    dirtySet.clear();
	}
	/**
	 * Cleanup the dirty connections in a connection list.
	 *
	 * @param list - The list of connection to cleanup.
	 *
	 * #### Notes
	 * This will remove any connection with a null token from the list,
	 * while retaining the relative order of the other connections.
	 *
	 * This function should only be invoked asynchronously, when the stack
	 * frame is guaranteed to not be on the path of a signal dispatch.
	 */
	function cleanupList(list) {
	    var count = 0;
	    for (var i = 0, n = list.length; i < n; ++i) {
	        var conn = list[i];
	        if (conn.token === null) {
	            count++;
	        }
	        else {
	            list[i - count] = conn;
	        }
	    }
	    list.length -= count;
	}
	
	/* WEBPACK VAR INJECTION */}.call(exports, __jupyter_require__('timers-browserify@1.4.2/main.js').setImmediate))
})
/** END DEFINE BLOCK for phosphor@0.6.1/lib/core/signaling.js **/


/** START DEFINE BLOCK for phosphor@0.6.1/lib/ui/title.js **/
jupyter.define('phosphor@0.6.1/lib/ui/title.js', function (module, exports, __jupyter_require__) {
	"use strict";
	/*-----------------------------------------------------------------------------
	| Copyright (c) 2014-2016, PhosphorJS Contributors
	|
	| Distributed under the terms of the BSD 3-Clause License.
	|
	| The full license is in the file LICENSE, distributed with this software.
	|----------------------------------------------------------------------------*/
	var signaling_1 = __jupyter_require__('phosphor@~0.6.1/lib/core/signaling.js');
	/**
	 * An object which holds data related to a widget's title.
	 *
	 * #### Notes
	 * A title object is intended to hold the data necessary to display a
	 * header for a particular widget. A common example is the `TabPanel`,
	 * which uses the widget title to populate the tab for a child widget.
	 */
	var Title = (function () {
	    /**
	     * Construct a new title.
	     *
	     * @param options - The options for initializing the title.
	     */
	    function Title(options) {
	        if (options === void 0) { options = {}; }
	        this._label = '';
	        this._icon = '';
	        this._caption = '';
	        this._mnemonic = -1;
	        this._className = '';
	        this._closable = false;
	        this._owner = null;
	        if (options.owner !== void 0) {
	            this._owner = options.owner;
	        }
	        if (options.label !== void 0) {
	            this._label = options.label;
	        }
	        if (options.mnemonic !== void 0) {
	            this._mnemonic = options.mnemonic;
	        }
	        if (options.icon !== void 0) {
	            this._icon = options.icon;
	        }
	        if (options.caption !== void 0) {
	            this._caption = options.caption;
	        }
	        if (options.closable !== void 0) {
	            this._closable = options.closable;
	        }
	        if (options.className !== void 0) {
	            this._className = options.className;
	        }
	    }
	    Object.defineProperty(Title.prototype, "owner", {
	        /**
	         * Get the object which owns the title.
	         *
	         * #### Notes
	         * This will be `null` if the title has no owner.
	         *
	         * This is a read-only property.
	         */
	        get: function () {
	            return this._owner;
	        },
	        enumerable: true,
	        configurable: true
	    });
	    Object.defineProperty(Title.prototype, "label", {
	        /**
	         * Get the label for the title.
	         *
	         * #### Notes
	         * The default value is an empty string.
	         */
	        get: function () {
	            return this._label;
	        },
	        /**
	         * Set the label for the title.
	         */
	        set: function (value) {
	            if (this._label === value) {
	                return;
	            }
	            this._label = value;
	            this.changed.emit(void 0);
	        },
	        enumerable: true,
	        configurable: true
	    });
	    Object.defineProperty(Title.prototype, "mnemonic", {
	        /**
	         * Get the mnemonic index for the title.
	         *
	         * #### Notes
	         * The default value is `-1`.
	         */
	        get: function () {
	            return this._mnemonic;
	        },
	        /**
	         * Set the mnemonic index for the title.
	         */
	        set: function (value) {
	            if (this._mnemonic === value) {
	                return;
	            }
	            this._mnemonic = value;
	            this.changed.emit(void 0);
	        },
	        enumerable: true,
	        configurable: true
	    });
	    Object.defineProperty(Title.prototype, "icon", {
	        /**
	         * Get the icon class name for the title.
	         *
	         * #### Notes
	         * The default value is an empty string.
	         */
	        get: function () {
	            return this._icon;
	        },
	        /**
	         * Set the icon class name for the title.
	         *
	         * #### Notes
	         * Multiple class names can be separated with whitespace.
	         */
	        set: function (value) {
	            if (this._icon === value) {
	                return;
	            }
	            this._icon = value;
	            this.changed.emit(void 0);
	        },
	        enumerable: true,
	        configurable: true
	    });
	    Object.defineProperty(Title.prototype, "caption", {
	        /**
	         * Get the caption for the title.
	         *
	         * #### Notes
	         * The default value is an empty string.
	         */
	        get: function () {
	            return this._caption;
	        },
	        /**
	         * Set the caption for the title.
	         */
	        set: function (value) {
	            if (this._caption === value) {
	                return;
	            }
	            this._caption = value;
	            this.changed.emit(void 0);
	        },
	        enumerable: true,
	        configurable: true
	    });
	    Object.defineProperty(Title.prototype, "className", {
	        /**
	         * Get the extra class name for the title.
	         *
	         * #### Notes
	         * The default value is an empty string.
	         */
	        get: function () {
	            return this._className;
	        },
	        /**
	         * Set the extra class name for the title.
	         *
	         * #### Notes
	         * Multiple class names can be separated with whitespace.
	         */
	        set: function (value) {
	            if (this._className === value) {
	                return;
	            }
	            this._className = value;
	            this.changed.emit(void 0);
	        },
	        enumerable: true,
	        configurable: true
	    });
	    Object.defineProperty(Title.prototype, "closable", {
	        /**
	         * Get the closable state for the title.
	         *
	         * #### Notes
	         * The default value is `false`.
	         */
	        get: function () {
	            return this._closable;
	        },
	        /**
	         * Set the closable state for the title.
	         *
	         * #### Notes
	         * This controls the presence of a close icon when applicable.
	         */
	        set: function (value) {
	            if (this._closable === value) {
	                return;
	            }
	            this._closable = value;
	            this.changed.emit(void 0);
	        },
	        enumerable: true,
	        configurable: true
	    });
	    return Title;
	}());
	exports.Title = Title;
	// Define the signals for the `Title` class.
	signaling_1.defineSignal(Title.prototype, 'changed');
	
})
/** END DEFINE BLOCK for phosphor@0.6.1/lib/ui/title.js **/
