define([
    'jquery',
    'require',
    'base/js/namespace',
    'base/js/page',
    'base/js/utils',
    'services/config',
    'base/js/events',
    'notebook/js/quickhelp',
    'nbextensions/nbextensions_configurator/render/render',
    'nbextensions/nbextensions_configurator/kse_components',
    // only loaded, not used:
    'jqueryui',
    'bootstrap'
], function(
    $,
    require,
    Jupyter,
    page,
    utils,
    configmod,
    events,
    quickhelp,
    rendermd,
    kse_comp
) {
    'use strict';

    var base_url = utils.get_body_data('baseUrl');
    var first_load_done = false; // flag used to not push history on first load
    var extensions_dict = {}; // dictionary storing nbextensions by their 'require' value
    var filter_timeout_id = null; // timeout ref used to prevent lots of consecutive requests

    /**
     * function for comparing arbitrary version numbers, taken from
     * http://stackoverflow.com/questions/7717109/how-can-i-compare-arbitrary-version-numbers
     */
    function version_compare (a, b) {
        var cmp, trailing_re = /(\.0)+[^\.]*$/;
        a = (a + '').replace(trailing_re, '').split('.');
        b = (b + '').replace(trailing_re, '').split('.');
        var len = Math.min(a.length, b.length);
        for (var ii = 0; ii < len; ii++) {
            cmp = parseInt(a[ii], 10) - parseInt(b[ii], 10);
            if( cmp !== 0 ) {
                return cmp;
            }
        }
        return a.length - b.length;
    }

    /**
     * create configs var from json files on server.
     * we still need to call configs[].load later to actually fetch them though!
     */
    var configs = {
        'notebook' : new configmod.ConfigSection('notebook', {base_url: base_url}),
        'edit' : new configmod.ConfigSection('edit', {base_url: base_url}),
        'tree' : new configmod.ConfigSection('tree', {base_url: base_url}),
        'common'   : new configmod.ConfigSection('common', {base_url: base_url}),
    };

    // tags used to filter visible nbextensions
    var tags = [];

    // the prefix added to all parameter input id's
    var param_id_prefix = 'input_';
    // class added to the body tag when we're in a standalone page.
    // Used as a flag to decide whether to set window.location.search
    var page_class = 'nbextensions_configurator_page';

    /**
     * check whether a dot-notation key exists in a given ConfigSection object
     *
     * @param {ConfigSection} conf - the config section to query
     * @param {string} key - the (dot-notation) key to check for
     * @return {Boolean} - `true` if the key exists, `false` otherwise
     */
    function conf_dot_key_exists(conf, key) {
        var obj = conf.data;
        key = key.split('.');
        while (key.length > 0) {
            var partkey = key.shift();
            if (!obj.hasOwnProperty(partkey)) {
                return false;
            }
            obj = obj[partkey];
        }
        return true;
    }

    /**
     * get the value for a dot-notation key in a given ConfigSection object
     *
     * @param {ConfigSection} conf - the config section to query
     * @param {string} key - the (dot-notation) key to get the value of
     * @return - the value associated with the given key
     */
    function conf_dot_get (conf, key) {
        var obj = conf.data;
        key = key.split('.');
        while (key.length > 0) {
            obj = obj[key.shift()];
        }
        return obj;
    }

    /**
     * update the value for a dot-notation key in a given ConfigSection object
     *
     * @param {ConfigSection} conf - the config section to update
     * @param {string} key - the (dot-notation) key to update the value of
     * @param value - the new value to set. null results in removal of the key
     * @return - the return value of the ConfigSection.update call
     */
    function conf_dot_update (conf, key, value) {
        key = key.split('.');
        var root = {};
        var curr = root;
        while (key.length > 1) {
            curr = curr[key.shift()] = {};
        }
        curr[key.shift()] = value;
        return conf.update(root);
    }

    /**
     * Remove the value for a dot-notation key in a given ConfigSection object.
     *
     * @param {ConfigSection} conf - the config section to update
     * @param {string[]} dotted_keys - the (dot-notation) keys to remove
     */
    function conf_dot_delete_keys(conf, dotted_keys) {
        return conf.load().then(function (data) {
            for (var ii=0; ii < dotted_keys.length; ii++) {
                var obj = data;
                var key_parts = dotted_keys[ii].split('.');
                while (key_parts.length > 0) {
                    var partkey = key_parts.shift();
                    if (key_parts.length === 0) {
                        delete obj[partkey];
                        break;
                    }
                    if (!obj.hasOwnProperty(partkey)) {
                        break;
                    }
                    obj = obj[partkey];
                }
            }
            // Modify the config values stored by calling api directly
            // (set endpoint isn't yet implemented in js class)
            return utils.promising_ajax(conf.api_url(), {
                processData: false,
                type : "PUT",
                data: JSON.stringify(data),
                dataType : "json",
                contentType: 'application/json',
            });
        });
    }

    /**
     * Update server's json config file to reflect changed enable state
     */
    function set_config_enabled (extension, state) {
        state = state === undefined ? true : Boolean(state);
        console.log('Notebook extension "' + extension.Name + '"', state ? 'enabled' : 'disabled');
        // for pre-4.2 versions, the javascript loading nbextensions actually
        // ignores the true/false state, so to disable we have to delete the key
        if ((version_compare(Jupyter.version, '4.2') < 0) && !state) {
            state = null;
        }
        var to_load = {};
        to_load[extension.require] = state;
        configs[extension.Section].update({load_extensions: to_load});
    }

    /**
     * Callback function for clicking on a collapsible panel heading
     */
    function panel_showhide_callback (evt) {
        evt.preventDefault();
        evt.stopPropagation();
        var head = $(evt.currentTarget);
        var body = head.next();
        var show = !body.is(':visible');
        head.find('i.fa').first()
            .toggleClass('fa-caret-down', show)
            .toggleClass('fa-caret-right', !show);
        body
            .slideToggle({show: show, duration: 200});
    }

    /**
     * Update buttons to reflect changed enable state
     */
    function set_buttons_enabled (extension, state) {
        state = (state === true);

        extension.selector_link.find('.nbext-enable-toggle').toggleClass('nbext-enabled', state);

        var btns = $(extension.ui).find('.nbext-enable-btns').children();
        btns.eq(0)
            .prop('disabled', state)
            .toggleClass('btn-default disabled', state)
            .toggleClass('btn-primary', !state);
        btns.eq(1)
            .prop('disabled', !state)
            .toggleClass('btn-default disabled', !state)
            .toggleClass('btn-primary', state);
    }

    /**
     * Handle button click event to enable/disable nbextension
     */
    function handle_buttons_click (evt) {
        var btn = $(evt.target);
        var state = btn.is(':first-child');
        var extension = btn.closest('.nbext-ext-row').data('extension');
        set_buttons_enabled(extension, state);
        set_config_enabled(extension, state);
    }

    /*
     * Get the useful value (dependent on element type) from an input element
     */
    function get_input_value (input) {
        input = $(input);
        var input_type = input.data('param_type');

        switch (input_type) {
            case 'hotkey':
                return input.find('.hotkey').data('pre-humanized');
            case 'list':
                var val = [];
                input.find('.nbext-list-element').children().not('a').each(
                    function () {
                        // "this" is the current child element of input in the loop
                        val.push(get_input_value(this));
                    }
                );
                return val;
            case 'checkbox':
                return input.prop('checked') ? true : false;
            default:
                return input.val();
        }
    }

    /*
     * Set the useful value (dependent on element type) from a js value
     */
    function set_input_value (input, new_value) {
        input = $(input);
        var input_type = input.data('param_type');
        switch (input_type) {
            case 'hotkey':
                input.find('.hotkey')
                    .html(quickhelp.humanize_sequence(new_value))
                    .data('pre-humanized', new_value);
                break;
            case 'list':
                var ul = input.children('ul');
                ul.empty();
                var list_element_param = input.data('list_element_param');
                for (var ii = 0; ii < new_value.length; ii++) {
                    var list_element_input = build_param_input(list_element_param);
                    list_element_input.on('change', handle_input);
                    set_input_value(list_element_input, new_value[ii]);
                    ul.append(wrap_list_input(list_element_input));
                }
                break;
            case 'checkbox':
                input.prop('checked', new_value ? true : false);
                break;
            default:
                input.val(new_value);
        }
    }

    /**
     * handle form input for nbextension parameters, updating parameters in
     * server's json config file
     */
    function handle_input (evt) {
        var input = $(evt.target);

        // list elements should alter their parent's config
        if (input.closest('.nbext-list-wrap').length > 0) {
            input = input.closest('.nbext-list-wrap');
        }
        // hotkeys need to find the correct tag
        else if (input.hasClass('hotkey')) {
            input = input.closest('.input-group');
        }

        // get param name by cutting off prefix
        var configkey = input.attr('id').substring(param_id_prefix.length);
        var configval = get_input_value(input);
        var configsection = input.data('section');
        console.log(configsection + '.' + configkey, '->', configval);
        conf_dot_update(configs[configsection], configkey, configval);
        return configval;
    }

    /**
     * wrap a single list-element input with the <li>, and move/remove buttons
     */
    function wrap_list_input (list_input) {
        var btn_remove = $('<a/>', {'class': 'btn btn-default input-group-addon nbext-list-el-btn-remove'});
        btn_remove.append($('<i/>', {'class': 'fa fa-fw fa-trash'}));
        btn_remove.on('click', function () {
            var list_el = $(this).closest('li');
            var list_input = list_el.closest('.nbext-list-wrap');
            list_el.remove();
            list_input.change(); // trigger change event
        });

        return $('<li/>', {'class' : 'nbext-list-element input-group'}).append(
            $('<a class="btn btn-default input-group-addon handle"/>').append(
                $('<i class="fa fa-fw fa-arrows-v"/>')
            ),
            [list_input, btn_remove]);
    }

    /**
     * Build and return an element used to edit a parameter
     */
    function build_param_input (param) {
        var input_type = (param.input_type || 'text').toLowerCase();
        var input;

        switch (input_type) {
            case 'hotkey':
                input = $('<div class="input-group"/>');
                input.append(
                    $('<span class="form-control form-control-static hotkey"/>')
                        .css(utils.platform === 'MasOS' ? {'letter-spacing': '1px'} : {})
                );
                input.append($('<div class="input-group-btn"/>').append(
                    $('<div class="btn-group"/>').append(
                        $('<a/>', {
                            type: 'button',
                            class: 'btn btn-primary',
                            text: 'Change'
                        }).on('click', function() {
                            var description = 'Change ' +
                                param.description +
                                ' from ' +
                                quickhelp.humanize_sequence(get_input_value(input)) +
                                ' to:';
                            var modal = kse_comp.KSE_modal({
                                'description': description,
                                'buttons': {
                                    'OK': {
                                        'class': 'btn-primary',
                                        'click': function () {
                                            var editor = $(this).find('#kse-editor');
                                            var new_value = (editor.data('kse_sequence') || []).join(',');
                                            set_input_value(input, new_value);
                                            // trigger write to config
                                            input.find('.hotkey').change();
                                        }
                                    },
                                    'Cancel': {}
                                },
                            });
                            modal.modal('show');
                        })
                    )
                ));
                break;
            case 'list':
                input = $('<div/>', {'class' : 'nbext-list-wrap'});
                input.append(
                    $('<ul/>', {'class': 'list-unstyled'})
                        .sortable({
                            handle: '.handle',
                            containment: 'window',
                            placeholder: 'nbext-list-element-placeholder',
                            update: function(event, ui) {
                                ui.item.closest('.nbext-list-wrap').change();
                            }
                        })
                );
                var list_element_param = param.list_element || {};
                // add the requested list param type to the list element using
                // jquery data api
                input.data('list_element_param', list_element_param);

                // add a button to add list elements
                var add_button = $('<a/>')
                    .addClass('btn btn-default input-group-btn nbext-list-btn-add')
                    .text(' new item')
                    .prepend('<i class="fa fa-plus"/>')
                    .on('click', function () {
                        $(this).parent().siblings('ul').append(
                            wrap_list_input(
                                build_param_input(list_element_param)
                                    .on('change', handle_input)
                            )
                        ).closest('.nbext-list-wrap').change();
                    });
                input.append($('<div class="input-group"/>').append(add_button));
                break;
            case 'textarea':
                input = $('<textarea/>');
                break;
            case 'number':
                input = $('<input/>', {'type': input_type});
                if (param.step !== undefined) input.attr('step', param.step);
                if (param.min !== undefined) input.attr('min', param.min);
                if (param.max !== undefined) input.attr('max', param.max);
                break;
            default:
                // detect html5 input tag support using scheme from
                // http://diveintohtml5.info/detect.html#input-types
                // If the browser supports the requested particular input type,
                // the type property will retain the value you set.
                // If the browser does not support the requested input type,
                // it will ignore the value you set
                // and the type property will still be "text".
                input = document.createElement('input');
                input.setAttribute('type', input_type);
                // wrap in jquery
                input = $(input);
        }
        // add the param type to the element using jquery data api
        input.data('param_type', input_type);
        input.data('section', param.section);
        var non_form_control_input_types = ['checkbox', 'list', 'hotkey'];
        if (non_form_control_input_types.indexOf(input_type) < 0) {
            input.addClass('form-control');
        }
        return input;
    }

    /*
     * Build and return a div containing the buttons to enable/disable an
     * nbextension with the given id.
     */
    function build_enable_buttons () {
        var div_buttons = $('<div class="btn-group nbext-enable-btns"/>');

        $('<button/>')
            .text('Enable')
            .attr('type', 'button')
            .addClass('btn btn-primary')
            .on('click', handle_buttons_click)
            .appendTo(div_buttons);

        $('<button/>')
            .text('Disable')
            .attr('type', 'button')
            .addClass('btn btn-default')
            .on('click', handle_buttons_click)
            .prop('disabled', true)
            .appendTo(div_buttons);

        return div_buttons;
    }

    /**
     * show/hide compatibility text, along with en/disabling the nav link
     */
    function set_hide_incompat (hide_incompat) {
        $('.nbext-compat-div').toggle(!hide_incompat);
        $('.nbext-selector .nbext-incompatible')
            .toggleClass('disabled', hide_incompat)
            .attr('title', hide_incompat ? 'possibly incompatible' : '');
        set_input_value(
            $('#' + param_id_prefix + 'nbext_hide_incompat'), hide_incompat);

        var selector = $('.nbext-selector');
        if (selector.find('li.active').first().hasClass('disabled')) {
            selector.find('li:not(.disabled):visible a').first().click();
        }
    }

    /**
     * if the nbextension's readme is a relative url with file extension .md,
     *     render the referenced markdown file
     * otherwise
     *     add an anchor element to the nbextension's description
     */
    function load_readme (extension) {
        var readme = $('.nbext-readme');
        var readme_contents = readme.children('.nbext-readme-contents').empty();
        var readme_title = readme.find('.nbext-readme-title').empty();

        if (extension.readme === undefined) {
            readme.slideUp(100);
            return;
        }
        readme.slideDown(100);

        var url = extension.readme;
        var is_absolute = /^(f|ht)tps?:\/\//i.test(url);
        if (is_absolute || (utils.splitext(url)[1] !== '.md')) {
            // provide a link only
            var desc = extension.ui.find('.nbext-desc');
            var link = desc.find('.nbext-readme-more-link');
            if (link.length === 0) {
                desc.append(' ');
                link = $('<a/>')
                    .addClass('nbext-readme-more-link')
                    .text('more...')
                    .attr('href', url)
                    .appendTo(desc);
            }
            return;
        }
        // relative urls are in nbextensions namespace
        url = require.toUrl(
            utils.url_path_join(
                base_url, 'nbextensions', utils.encode_uri_components(url)));
        // remove search component, as it's just a datestamp from require.js
        url = $('<a>').attr('href', url)[0].pathname;
        readme_title.text(url);
        // add rendered markdown to readme_contents. Use pre-fetched if present
        if (extension.readme_content) {
            rendermd.render_markdown(extension.readme_content, url)
                .addClass('rendered_html')
                .appendTo(readme_contents);
            return;
        }
        $.ajax({
            url: url,
            dataType: 'text',
            success: function (md_contents) {
                rendermd.render_markdown(md_contents, url)
                    .addClass('rendered_html')
                    .appendTo(readme_contents);
                // We can't rely on picking up the rendered html,
                // since render_markdown returns
                // before the actual rendering work is complete
                extension.readme_content = md_contents;
                if (! $('body').hasClass(page_class)) {
                    return;
                }
                // attempt to scroll to a location hash, if there is one.
                var hash = window.location.hash.replace(/^#/, '');
                if (hash) {
                    // Allow time for markdown to render
                    setTimeout( function () {
                        // use filter to avoid breaking jQuery selector syntax with weird id
                        var hdr = readme_contents.find(':header').filter(function (idx, elem) {
                            return elem.id === hash;
                        });
                        if (hdr.length > 0) {
                            var site = $('#site');
                            var adjust = hdr.offset().top - site.offset().top;
                            if (adjust > 0) {
                                site.animate(
                                    {scrollTop: site.scrollTop() + adjust},
                                    undefined, // time
                                    undefined, // easing function
                                    function () {
                                        if (hdr.effect !== undefined) {
                                            hdr.effect('highlight', {color: '#faf2cc'});
                                        }
                                    }
                                );
                            }
                        }
                    }, 100);
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                var error_div = $('<div class="text-danger bg-danger"/>')
                    .text(textStatus + ' : ' + jqXHR.status + ' ' + errorThrown)
                    .appendTo(readme_contents);
                if (jqXHR.status === 404) {
                    $('<p/>')
                        .text('no markdown file at ' + url)
                        .appendTo(error_div);
                }
            }
        });
    }

    /**
     * open the user interface for the nbextension corresponding to the given
     * link
     * @param extension the nbextension
     * @param opts options for the reveal animation
     */
    function open_ext_ui (extension, opts) {
        var default_opts = {duration: 100};
        opts = $.extend(true, {}, default_opts, opts);

        if (extension === undefined) {
            // just make a dummy to warn about selection
            extension = {
                ui: $('<div/>')
                    .data('extension', extension)
                    .addClass('row nbext-ext-row')
                    .css('display', 'none')
                    .insertBefore('.nbext-readme'),
                selector_link: $(),
            };
            var warning = $('<div/>')
                .addClass('alert alert-warning')
                .appendTo(extension.ui);
            $('<p/>')
                .text('No nbextensions match the applied filters!')
                .appendTo(warning);
        }

        /**
         * If we're in a standalone page,
         * Set window search string to allow reloading settings for a given
         * nbextension.
         * Use history.pushState if available, to avoid reloading the page
         */
        if (first_load_done && $('body').hasClass(page_class) && extension.require !== undefined) {
            var new_search = '?nbextension=' + utils.encode_uri_components(extension.require);
            if (window.history.pushState) {
                window.history.pushState(extension.require, undefined, new_search);
            }
            else {
                window.location.search = new_search;
            }
        }
        first_load_done = true;

        // ensure extension.ui exists
        if (extension.ui === undefined) {
            // use display: none since hide(0) doesn't do anything
            // for elements that aren't yet part of the DOM
            extension.ui = build_extension_ui(extension)
                .css('display', 'none')
                .insertBefore('.nbext-readme');

            var ext_enabled = extension.selector_link.find('.nbext-enable-toggle').hasClass('nbext-enabled');
            set_buttons_enabled(extension, ext_enabled);
        }

        $('.nbext-selector li')
            .removeClass('active');
        extension.selector_link.closest('li').addClass('active');

        $('.nbext-ext-row')
            .not(extension.ui)
            .slideUp(default_opts);
        extension.ui.slideDown(opts);
        load_readme(extension);
    }

    /**
     * Callback for the nav links
     * open the user interface for the nbextension corresponding to the clicked
     * link, and scroll it into view
     */
    function selector_nav_link_callback (evt) {
        evt.preventDefault();
        evt.stopPropagation();

        var a = $(evt.currentTarget);
        var extension = a.data('extension');
        if (a.closest('li').hasClass('disabled')) {
            return;
        }
        open_ext_ui(extension, {
            complete: function () {
                if (! $('body').hasClass(page_class)) {
                    return;
                }
                // scroll to ensure at least title is visible
                var site = $('#site');
                var title = extension.ui.children('h3:first');
                var adjust = (title.offset().top - site.offset().top) + (2 * title.outerHeight(true) - site.innerHeight());
                if (adjust > 0) {
                    site.animate({scrollTop: site.scrollTop() + adjust});
                }
            }
        });
    }

    /**
     * Callback for the nav links' enable checkboxes
     */
    function selector_checkbox_callback (evt) {
        evt.preventDefault();
        evt.stopPropagation();

        var a = $(evt.currentTarget).closest('a');
        if (!a.closest('li').hasClass('disabled')) {
            var extension = a.data('extension');
            var state = !$(evt.currentTarget).hasClass('nbext-enabled');
            set_buttons_enabled(extension, state);
            set_config_enabled(extension, state);
            open_ext_ui(extension);
        }
    }

    /**
     * delete all of the values for an nbextension's parameters from the config,
     * then rebuild their ui elements, to give default values.
     */
    function reset_params (extension) {
        // first remove config values:
        return conf_dot_delete_keys(
            configs[extension.Section],
            extension.Parameters.map(function (param) {
                return param.name;
            })
        ).then(function () {
            // now rebuild param ui
            extension.ui.find('.nbext-params > .list-group')
                .replaceWith(build_params_ui(extension.Parameters));
        });
    }

    /**
     * Callback for the rest parameters control
     */
    function reset_params_callback (evt) {
        evt.stopPropagation(); // don't want to toggle visibility too!
        var btn = $(evt.target);
        if (btn.children('.fa').length < 1) {
            btn.addClass('disabled');
            btn.children('.fa').addClass('fa-spin');
        }
        var extension = btn.closest('.nbext-ext-row').data('extension');
        reset_params(extension).then(function () {
            btn.removeClass('disabled');
            btn.children('.fa').removeClass('fa-spin');
        });
    }

    /**
     * build and return UI elements for a set of parameters
     */
    function build_params_ui (params) {
        // Assemble and add params
        var div_param_list = $('<div/>')
            .addClass('list-group');

        for (var pp in params) {
            var param = params[pp];
            var param_name = param.name;
            if (!param_name) {
                console.error('nbext param: unnamed parameter declared!');
                continue;
            }

            var param_div = $('<div/>')
                .addClass('form-group list-group-item')
                .appendTo(div_param_list);

            var param_id = param_id_prefix + param_name;

            // use param name / description as label
            $('<label/>')
                .attr('for', param_id)
                .html(
                    param.hasOwnProperty('description') ? param.description : param_name
                )
                .appendTo(param_div);

            // input to configure the param
            var input = build_param_input(param);
            input.on('change', handle_input);
            input.attr('id', param_id);
            var prepend_input_types = ['checkbox'];
            if (prepend_input_types.indexOf(param.input_type) < 0) {
                param_div.append(input);
            }
            else {
                param_div.prepend(' ');
                param_div.prepend(input);
            }

            // set input value from config or default, if poss
            if (conf_dot_key_exists(configs[param.section], param_name)) {
                var configval = conf_dot_get(configs[param.section], param_name);
                console.log(
                    'nbext param:', param_name,
                    'from config:', configval
                );
                set_input_value(input, configval);
            }
            else if (param.hasOwnProperty('default')) {
                set_input_value(input, param.default);
                console.log(
                    'nbext param:', param_name,
                    'default:', param.default
                );
            }
            else {
                console.log('nbext param:', param_name);
            }
        }
        return div_param_list;
    }

    /**
     * build and return UI elements for a single nbextension
     */
    function build_extension_ui (extension) {
        var ext_row = $('<div/>')
            .data('extension', extension)
            .addClass('row nbext-ext-row');

        try {
            /**
             * Name.
             * Take advantage of column wrapping by using the col-xs-12 class
             * to ensure the name takes up a whole row-width on its own,
             * so that the subsequent columns wrap onto a new line.
             */
            var ext_name_head = $('<h3>')
                .addClass('col-xs-12')
                .html(extension.Name)
                .appendTo(ext_row);

            /**
             * Columns
             */
            var col_left = $('<div/>')
                .addClass('col-xs-12')
                .appendTo(ext_row);

            // Icon
            if (extension.icon) {
                col_left
                    .addClass('col-sm-8 col-sm-pull-4 col-md-6 col-md-pull-6');
                // right precedes left in markup, so that it appears first when
                // the columns are wrapped each onto a single line.
                // The push and pull CSS classes are then used to get them to
                // be left/right correctly when next to each other
                var col_right = $('<div>')
                    .addClass('col-xs-12 col-sm-4 col-sm-push-8 col-md-6 col-md-push-6')
                    .insertBefore(col_left);
                $('<div/>')
                    .addClass('nbext-icon')
                    .append(
                        $('<img>')
                            .attr({
                                // extension.icon is in nbextensions namespace
                                'src': utils.url_path_join(base_url, 'nbextensions', utils.encode_uri_components(extension.icon)),
                                'alt': extension.Name + ' icon'
                            })
                    )
                    .appendTo(col_right);
            }

            // Duplicate warning
            if (extension.duplicate) {
                var duplicate_warning_p = $('<p/>').text([
                    'This nbextension\'s require url (' + extension.require + ')',
                    'is referenced by two different yaml files on the server.',
                    'This probably means that there are two installations of the',
                    'same nbextension in different directories on the server.',
                    'If they are different, only one will be loaded by the',
                    'notebook, and this may prevent configuration from working',
                    'correctly.',
                    'Check the jupyter server log for the paths of the relevant',
                    'yaml files.'].join(' '));
                $('<div/>')
                    .addClass('alert alert-warning')
                    .css('margin-top', '5px')
                    .append(duplicate_warning_p)
                    .appendTo(ext_row);
            }

            // Description
            var div_desc = $('<div/>')
                .addClass('nbext-desc')
                .appendTo(col_left);
            if (extension.hasOwnProperty('Description')) {
                $('<p/>')
                    .html(extension.Description)
                    .appendTo(div_desc);
            }

            // Section
            $('<div/>')
                .text('section: ' + extension.Section)
                .addClass('nbext-sect')
                .appendTo(col_left);

            // Require
            $('<div/>')
                .text('require path: ')
                .addClass('nbext-req')
                .append(
                    $('<span/>').addClass('rendered_html').append(
                        $('<code/>').text(extension.require)))
                .appendTo(col_left);

            // Compatibility
            var compat_txt = extension.Compatibility || '?.x';
            var compat_idx = compat_txt.toLowerCase().indexOf(
                Jupyter.version.substring(0, 2) + 'x');
            if (!extension.is_compatible) {
                ext_row.addClass('nbext-incompatible');
                compat_txt = $('<span/>')
                    .addClass('bg-danger text-danger')
                    .text(compat_txt);
            }
            else {
                compat_txt = $('<span/>')
                    .append(
                        compat_txt.substring(0, compat_idx)
                    )
                    .append(
                        $('<span/>')
                            .addClass('bg-success text-success')
                            .text(compat_txt.substring(compat_idx, compat_idx + 3))
                    )
                    .append(compat_txt.substring(compat_idx + 3, compat_txt.length));
            }
            $('<div/>')
                .addClass('nbext-compat-div')
                .text('compatibility: ')
                .append(compat_txt)
                .appendTo(col_left);

            // Enable/Disable buttons
            build_enable_buttons().appendTo(col_left);

            // Parameters
            if (extension.Parameters.length > 0) {
                for (var ii = 0; ii < extension.Parameters.length; ii++) {
                    extension.Parameters[ii].section = extension.Section;
                }
                var reset_control = $('<a/>')
                    .addClass('nbext-params-reset')
                    .on('click', reset_params_callback)
                    .addClass('pull-right')
                    .attr('href', '#')
                    .text(' reset');
                $('<i/>')
                    .addClass('fa fa-refresh')
                    .addClass()
                    .prependTo(reset_control);
                $('<div/>')
                    .addClass('panel panel-default nbext-params col-xs-12')
                    .append(
                        $('<div/>')
                            .addClass('panel-heading')
                            .text('Parameters')
                            .prepend('<i class="fa fa-fw fa-caret-down"/>')
                            .on('click', panel_showhide_callback)
                            .append(reset_control)
                    )
                    .append(
                        build_params_ui(extension.Parameters)
                    )
                    .appendTo(ext_row);
            }
        }
        catch (err) {
            console.error('[nbext] error loading nbextension', extension.Name);
            console.error(err);
            $('<div/>')
                .addClass('alert alert-warning')
                .css('margin-top', '5px')
                .append(
                    $('<p/>')
                        .text('[nbext] error loading nbextension ' + extension.Name)
                )
                .appendTo(ext_row);
        }
        finally {
            return ext_row;
        }
    }

    /**
     * callback function for changes to filters. This is essentially just a way
     * of preventing multiple callbacks from executing simultaneously, so that
     * huge numbers of filter change callbacks don't make the UI laggy.
     */
    function filter_callback_queue_refresh (evt) {
        clearTimeout(filter_timeout_id);
        filter_timeout_id = setTimeout(filter_refresh_visible_nbexts, 100);
    }

    function filter_refresh_visible_nbexts () {
        var to_show = [], to_hide = [];
        $('.nbext-selector ul li a').each(function (idx, el) {
            var ext = $(el).data('extension');
            var active_tag_elems = $('.nbext-filter-tag');
            var show = true;
            for (var ii=0; ii < active_tag_elems.length && show; ii++) {
                var tag = active_tag_elems.eq(ii).data('nbext_tag_object');
                switch (tag.category) {
                    case 'name':
                        show = show && (tag.value === ext.Name);
                        break;
                    case 'section':
                        show = show && (tag.value === ext.Section);
                        break;
                    case 'tag':
                        show = show && (ext.tags.indexOf(tag.value) > 0);
                        break;
                }
            }
            (show ? to_show: to_hide).push(ext.selector_link.parent()[0]);

        });
        $(to_hide).slideUp(100);
        to_show = $(to_show); // convert to jquery obj
        to_show.slideDown(100)
        // make sure a visible nbextensions is selected
        if (!to_show.is('.active')) {
            var candidate = to_show.filter(':not(.disabled)').first().children('a');
            if (candidate.length > 0 ) {
                candidate.click();
            }
            else {
                open_ext_ui(undefined);
            }
        }
    }

    function filter_build_tag_element (tag_object) {
        var tag_elem = $('<div>')
            .data('nbext_tag_object', tag_object)
            .addClass('nbext-filter-tag btn-group');
        $('<span/>')
            // .addClass('btn btn-primary')
            .text(tag_object.label)
            .appendTo(tag_elem);
        $('<span/>')
            // .addClass('btn btn-primary')
            .on('click', function (evt) {
                evt.preventDefault();
                tag_elem.remove();
                filter_callback_queue_refresh();
            })
            .append('<i class="fa fa-close">')
            .appendTo(tag_elem);
        return tag_elem;
    }

    function filter_register_new_tag (new_tag_object) {
        for (var ii=0; ii < tags.length; ii++) {
            if (tags[ii].value == new_tag_object.value && tags[ii].category == new_tag_object.category) {
                return //tag already exists, so don't insert
            }
        }
        new_tag_object.label = new_tag_object.category + ': ' + new_tag_object.value;
        tags.push(new_tag_object);
    }

    function filter_build_ui () {
        // define a custom jqueryui autocomplete widget
        $.widget('custom.nbextfilterer', $.ui.autocomplete, {
            _create: function () {
                this._super();
                this.widget().menu('option', 'items', '> :not(.nbext-filter-category)');
            },
            _renderMenu: function (ul, items) {
                ul.addClass('nbext-filter-menu dropdown-menu');
                ul.removeClass('ui-menu ui-autocomplete ui-front ui-widget ui-widget-content ui-corner-all');
                var nbextfiltererwidget = this;
                // leave already-applied tags out of the menu
                var active_tag_labels = $.map(
                    $(this.element).siblings('.nbext-filter-tag'),
                    function (elem, idx) {
                        return $(elem).data('nbext_tag_object').label;
                    }
                );
                $.each(items, function (index, item) {
                    if (active_tag_labels.indexOf(item.label) < 0) {
                        nbextfiltererwidget._renderItemData(ul, item);
                    }
                });
            }
        });

        var filter_input_group = $('<div/>')
            .attr('id', 'nbext-filter-grp')
            .addClass('nbext-filter-grp input-group');
        $('<span/>')
            .attr('id', 'nbext-filter-label')
            .addClass('nbext-filter-label input-group-addon')
            .appendTo(filter_input_group);
        // add a wrapper to hold both applied tags and an input.
        // It will be styled to look like an input using the form-control css class.
        var filter_input_wrap = $('<div/>')
            .addClass('nbext-filter-input-wrap form-control')
            .attr('aria-describedby', 'nbext-filter-label')
            .on('click', function (evt) {
                if (evt.target == this) { //only if we clicked the div, not a child of it
                    var input = $(this).find('input').first();
                    input.focus();
                    input.data('custom-nbextfilterer').search(input[0].value);
                }
            }).appendTo(filter_input_group);

        // add the actual input
        $('<input />')
            .on('focus', function (evt) {
                $(this).data('custom-nbextfilterer').search(this.value);
            })
            // register an extra keydown handler for stuff where we want to
            // override default autocomplete behaviour
            .on('keydown', function (evt) {
                var $this = $(this);
                if (evt.keyCode === $.ui.keyCode.TAB) {
                    // don't navigate away from the field on tab when selecting an item
                    var menu_active = $this.data('custom-nbextfilterer').menu.active;
                    if (menu_active) {
                        evt.preventDefault();
                    }
                    filter_callback_queue_refresh();
                }
                else if (evt.keyCode === $.ui.keyCode.BACKSPACE && !this.value) {
                    $this.siblings('.nbext-filter-tag').last().remove();
                    filter_callback_queue_refresh();
                }
            })
            .nbextfilterer({
                delay: 20,
                source: tags,
                minLength: 0,
                autoFocus: true,
                focus: function() {
                    return false; // prevent value inserted on focus
                },
                select: function(event, ui) {
                    // add the selected item (tag)
                    filter_build_tag_element(ui.item).insertBefore(this);
                    // clear input
                    this.value = '';
                    // queue updating filter
                    filter_callback_queue_refresh();
                    return false;
                }
            })
            .appendTo(filter_input_wrap);

        return filter_input_group;
    }

    function build_configurator_ui () {
        var config_ui = $('<div/>')
            .attr('id', 'nbextensions-configurator-container')
            .addClass('container');

        var selector = $('<div/>')
            .addClass('row nbext-row container-fluid nbext-selector')
            .appendTo(config_ui);

        $('<h3>Configurable nbextensions</h3>').appendTo(selector);

        var showhide = $('<div/>')
            .addClass('nbext-showhide-incompat')
            .append(
                build_param_input({
                    input_type: 'checkbox',
                    section: 'common'
                })
                    .attr('id', param_id_prefix + 'nbext_hide_incompat')
                    .on('change', function (evt) {
                        set_hide_incompat(handle_input(evt));
                    })
            )
            .append(' disable configuration for nbextensions without explicit compatibility (they may break your notebook environment, but can be useful to show for nbextension development)')
            .appendTo(selector);

        filter_build_ui().appendTo(selector);

        var selector_nav = $('<nav/>')
            .addClass('row')
            .append('<ul class="nav nav-pills"/>')
            .appendTo(selector);

        var readme = $('<div/>')
            .addClass('row nbext-readme panel panel-default')
            .css('display', 'none') // hide until an nbextension with a readme reveals it
            .appendTo(config_ui);
        $('<div class="panel-heading"/>')
            .append('<i class="fa fa-fw fa-caret-down"/>')
            .append('<span class="nbext-readme-title">')
            .on('click', panel_showhide_callback)
            .appendTo(readme);
        $('<div class="nbext-readme-contents panel-body"/>')
            .appendTo(readme);

        return config_ui;
    }

    function load_all_configs() {
        var config_promises = [];
        for (var section in configs) {
            config_promises.push(configs[section].loaded);
            configs[section].load();
        }
        return Promise.all(config_promises);
    }

    /**
     * build html body listing all nbextensions.
     */
    function build_page () {
        add_css('./main.css');
        $('body').addClass(page_class);

        var nbext_config_page = Jupyter.page = new page.Page();

        // prepare for rendermd usage
        rendermd.add_markdown_css();

        build_configurator_ui().appendTo('#site');

        nbext_config_page.show_header();
        events.trigger('resize-header.Page');

        load_all_configs().then(function () {
            // get list of nbextensions from value set by script embedded in page by the python backend
            build_extension_list(window.extension_list);
            nbext_config_page.show();
        });

        window.addEventListener('popstate', popstateCallback);
        setTimeout(popstateCallback, 0);

        return nbext_config_page;
    }

    /**
     * Callback for the window.popstate event, used to handle switching to the
     * correct selected nbextension
     */
    function popstateCallback (evt) {
        var require_url;
        if (evt === undefined) {
            // attempt to select an nbextension specified by a URL search parameter
            var queries = window.location.search.replace(/^\?/, '').split('&');
            for (var ii = 0; ii < queries.length; ii++) {
                var keyValuePair = queries[ii].split('=');
                if (decodeURIComponent(keyValuePair[0]) === 'nbextension') {
                    require_url = decodeURIComponent(keyValuePair[1]);
                    break;
                }
            }
        }
        else if (evt.state === null) {
            return; // as a result of setting window.location.hash
        }
        else {
            require_url = evt.state;
        }
        var selected_link;
        if (extensions_dict[require_url] === undefined || extensions_dict[require_url].selector_link.hasClass('disabled')) {
            selected_link = $('.nbext-selector').find('li:not(.disabled)').last().children('a');
        }
        else {
            selected_link = extensions_dict[require_url].selector_link;
        }
        selected_link.click();
    }

    /**
     * build html body listing all nbextensions.
     *
     * Since this function uses the contents of config.data,
     * it should only be called after config.load() has been executed
     */
    function build_extension_list (extension_list) {
        // add enabled-but-unconfigurable nbextensions to the list
        // construct a set of enabled nbextension urls from the configs
        // this is used later to add unconfigurable nbextensions to the list
        var unconfigurable_enabled_extensions = {};
        var section;
        for (section in configs) {
            unconfigurable_enabled_extensions[section] = $.extend({}, configs[section].data.load_extensions);
        }
        var i, extension;
        for (i = 0; i < extension_list.length; i++) {
            extension = extension_list[i];
            extension.Section = (extension.Section || 'notebook').toString();
            extension.Name = (extension.Name || (extension.Section + ':' + extension.require)).toString();
            // nbextension *is* configurable
            delete unconfigurable_enabled_extensions[extension.Section][extension.require];
        }
        // add any remaining unconfigurable nbextensions as stubs
        for (section in configs) {
            for (var require_url in unconfigurable_enabled_extensions[section]) {
                extension_list.push({
                    Name: require_url,
                    Description: 'This nbextension is enabled in the ' + section + ' json config, ' +
                        "but doesn't provide a yaml file to tell us how to configure it. " +
                        "You can still enable or disable it from here, though.",
                    Section: section,
                    require: require_url,
                    unconfigurable: true,
                });
            }
        }

        var container = $('#site > .container');

        var selector_nav = $('.nbext-selector ul');

        // sort nbextensions alphabetically
        extension_list.sort(function (a, b) {
            var an = (a.Name || '').toLowerCase();
            var bn = (b.Name || '').toLowerCase();
            if (an < bn) return -1;
            if (an > bn) return 1;
            return 0;
        });

        // fill the selector with nav links
        for (i = 0; i < extension_list.length; i++) {
            extension = extension_list[i];
            extensions_dict[extension.require] = extension;
            console.log('[nbext] found nbextension "' + extension.Name + '"');

            extension.is_compatible = (extension.Compatibility || '?.x').toLowerCase().indexOf(
                Jupyter.version.substring(0, 2) + 'x') >= 0;
            extension.Parameters = extension.Parameters || [];
            if (!extension.is_compatible) {
                // reveal the checkbox since we've found an incompatible nbext
                $('.nbext-showhide-incompat').show();
            }
            extension.selector_link = $('<a/>')
                .attr('href', '#')
                .data('extension', extension)
                .html(extension.Name)
                .toggleClass('text-warning bg-warning', extension.unconfigurable === true)
                .prepend(
                    $('<i>')
                        .addClass('fa fa-fw nbext-enable-toggle')
                );
            $('<li/>')
                .addClass('col-lg-3 col-md-4 col-sm-6 col-xs-12')
                .toggleClass('nbext-incompatible', !extension.is_compatible)
                .append(extension.selector_link)
                .appendTo(selector_nav);

            var ext_enabled = false;
            var conf = configs[extension.Section];
            if (conf === undefined) {
                console.warn("nbextension '" + extension.Name + "' specifies unknown Section of '" + extension.Section + "'. Can't determine enable status.");
            }
            else if (conf.data.hasOwnProperty('load_extensions')) {
                ext_enabled = (conf.data.load_extensions[extension.require] === true);
            }
            set_buttons_enabled(extension, ext_enabled);

            filter_register_new_tag({category: 'section', value: extension.Section});
            filter_register_new_tag({category: 'name', value: extension.Name});
            extension.tags = (extension.tags || []);
            for (var tt=0; tt < extension.tags.length; tt++) {
                filter_register_new_tag({category: 'tag', value: extension.tags[tt]});
            }
        }
        // sort tags
        tags.sort(function (a, b) {
            var cat_order = ['section', 'tag', 'name'];
            var an = cat_order.indexOf(a.category);
            var bn = cat_order.indexOf(b.category);
            if (an != bn) {
                return an - bn;
            }
            an = (a.label  || '').toLowerCase();
            bn = (b.label  || '').toLowerCase();
            if (an < bn) return -1;
            if (an > bn) return 1;
            return 0;
        });

        // attach click handlers
        $('.nbext-enable-toggle')
            .on('click', selector_checkbox_callback)
            .closest('a')
            .on('click', selector_nav_link_callback);

        // en/disable incompatible nbextensions
        var hide_incompat = true;
        if (configs['common'].data.hasOwnProperty('nbext_hide_incompat')) {
            hide_incompat = configs['common'].data.nbext_hide_incompat;
            console.log(
                'nbext_hide_incompat loaded from config as: ',
                hide_incompat
            );
        }
        set_hide_incompat(hide_incompat);

        // select a link
        selector_nav.children('li:not(.disabled)').last().children('a').click();
    }

    /**
     * Add CSS file to page
     *
     * @param name filename
     */
    function add_css (name) {
        var link = document.createElement('link');
        link.type = 'text/css';
        link.rel = 'stylesheet';
        link.href = require.toUrl(name);
        document.getElementsByTagName('head')[0].appendChild(link);
    }

    return {
        build_page : build_page,
        build_configurator_ui : build_configurator_ui,
        build_extension_list : build_extension_list,
        load_all_configs : load_all_configs
    };
});
