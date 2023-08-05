/**
 * jquery.quickapi.js - jQuery plugin for QuickAPI application
 * 
 * Copyright 2014-2015 Grigoriy Kramarenko <root@rosix.ru>
 *
 * This file is part of QuickAPI.
 *
 * QuickAPI is free software: you can redistribute it and/or
 * modify it under the terms of the GNU Affero General Public License
 * as published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version.
 *
 * QuickAPI is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public
 * License along with QuickAPI. If not, see
 * <http://www.gnu.org/licenses/>.
 * 
 */



(function ($) {
    /* Общая функция для работы с django-quickapi
     * 
     * Документация:
     * https://docs.rosix.org/django-quickapi/wiki/jquery.html#quickapi
     * 
     */

    $.quickAPI = function(opts) {

        var data, options = opts || new Object();

        // `args` is deprecation option
        if (!options.data) options.data = options.args || { method: "quickapi.test" };

        if (options.simple || options.type == 'GET') {

            data = options.data;
            if (!data.language) data.language = options.language || window.LANGUAGE_CODE

        } else {

            data = {
                jsonData: $.toJSON(options.data),
                language: options.language || window.LANGUAGE_CODE
            }

        }

        var jqxhr,
            settings = {
                type: options.type || "POST",
                async: options.sync === true ? false : options.async === false ? false : true,
                timeout: options.timeout || window.AJAX_TIMEOUT || 3000,
                url: options.url || window.QUICKAPI_URL || location.pathname,
                data: data,
                dataType: 'json',
            },
            callback = options.callback || function(json, status, xhr) {},
            showAlert = options.handlerShowAlert || window.handlerShowAlert || function(head, msg, cls, cb) {

                var match;

                if ($.type(msg) == 'object') {
                    msg = $.toJSON(msg)
                                .replace(/\,\"/g, ', "')
                                .replace(/\"\:/g, '": ')
                }
                else if (msg.match(/<\!DOCTYPE/)) {
                    match = msg.match(/<[title,TITLE]+>(.*)<\/[title,TITLE]+>/);
                    if (match) head = match[1];

                    match = msg.match(/<[body,BODY]+>([^+]*)<\/[body,BODY]+>/);
                    if (match) {
                        msg = match[1]
                            .replace(/<\/?[^>]+>/g, '')
                            .replace(/ [ ]+/g, ' ')
                            .replace(/\n[\n]+/g, '\n')
                    } else {
                        msg = '';
                    }
                }

                if (msg.length > 512) {
                    msg = msg.substring(0, 512) + ' ...'
                };

                alert(head +'\n'+ msg);

                if (cb) { return cb() };

                return null
            };

        jqxhr = $.ajax(settings)
                // Обработка ошибок протокола HTTP
                .fail(function(xhr, status, err) {

                    // Если есть переадресация, то выполняем её
                    if (xhr.getResponseHeader('Location')) {

                        location.replace(xhr.getResponseHeader('Location'));

                    } else if (xhr.responseText) {
                        // Иначе извещаем пользователя ответом и в консоль
                        console.error("ERROR:", xhr.responseText);

                        showAlert("ERROR:", xhr.responseText, 'alert-danger')
                    }
                })

                // Обработка полученных данных
                .done(function(json, status, xhr) {

                    if (options.log && window.DEBUG) {console.debug(options.log)};

                    /* При переадресации нужно отобразить сообщение на некоторое время,
                     * а затем выполнить переход по ссылке
                     */
                    if ((json.status >=300) && (json.status <400) && (json.data.Location != undefined)) {

                        var loc = json.data.Location, redirect;

                        redirect = function() { location.replace(loc) };

                        console.info("REDIRECT:" + loc);

                        if (json.message) {
                            showAlert("REDIRECT:", json.message, 'alert-danger', redirect)
                        } else {
                            redirect()
                        }
                    }
                    /* При ошибках извещаем пользователя полученным сообщением */
                    else if (json.status >=400) {
                        showAlert("ERROR:", json.message, 'alert-danger');
                    }
                    /* При нормальном возврате в debug-режиме выводим в консоль
                     * сообщение
                     */
                    else {
                        if (window.DEBUG) {
                            console.debug($.toJSON(json.message));

                            if (options.data.method == "quickapi.test") {
                                console.debug(json.data)
                            }
                        };

                        return callback(json, status, xhr)
                    }
                });

        return jqxhr
    }

}(jQuery));


/* 
 * jquery.quicktable.js - jQuery plugin for QuickAPI application
 * 
 * depends:
 *      jquery.quickapi.js - jQuery plugin for QuickAPI
 * recommends:
 *      Twitter bootstrap >= 3.0
 * 
 * Copyright 2014-2015 Grigoriy Kramarenko <root@rosix.ru>
 *
 * This file is part of QuickAPI.
 *
 * QuickAPI is free software: you can redistribute it and/or
 * modify it under the terms of the GNU Affero General Public License
 * as published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version.
 *
 * QuickAPI is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public
 * License along with QuickAPI. If not, see
 * <http://www.gnu.org/licenses/>.
 * 
 */



(function ($) {
    /* Плагин для работы с QuickTable из состава django-quickapi
     * 
     * Документация:
     * https://docs.rosix.org/django-quickapi/wiki/jquery.html#quicktable
     * 
     */
    var pluginName = "quickTable";

    $.fn[pluginName] = function(options) {

        if (!this.size()) { console.error('The selector found nothing'); return undefined };

        if (!options.method) {
            console.error(
                "Not valid options for "+pluginName,
                { method:options.method },
                'method must be defined!'
            );
        };

        if ($.type(options.columns) != 'array' || $.isEmptyObject(options.columns)) {

            console.error(
                "Not valid options for "+pluginName,
                { columns:options.columns },
                'columns must be not empty array!'
            );

            console.info('EXAMPLE:\n',
            'columns = [ {name:"id", hidden:true, notmanaged:true}, {name:"name", title:"Name"} ]\n',
            'where `name` - object attribute, `hidden` - hidden column,',
            ' `notmanaged` - the column is not managed, `title` - title of column.'
            );

        };


        var table = this[0], id, opts;

        id = $(table).attr('id');
        if (!id) { return this }; // not valid

        opts = $.extend({
            //url: undefined,
            //method: undefined,
            //columns: undefined,
            //handlerShowAlert: undefined,
            timeout: 10000,
            async: true,
            autoload: true,
            autorender_settings: true,
            delay: 500,
            page: 1,
            limit: 25,
            limit_list: [25, 50, 75, 100],
            filters: {},
            ordering: [],
            multiordering: false,
            table_type: 'table', // variants: 'stack' or 'pager'
            text_pager_prev: '&laquo;',
            text_pager_next: '&raquo;',
            // the following variables are strongly advised not to change
            _selector_filtering: '[data-filtering='+id+']',
            _selector_ordering: '#'+id+' th[class^=sorting][name]',
            _selector_limiting: 'input[data-limiting='+id+']:checked, select[data-limiting='+id+']',
            _selector_colswitcher: 'input[data-colswitcher='+id+']',
            _selector_settings: '#'+id+'_settings',
            _selector_pager: '#'+id+'_pager',
            _selector_pager_links: '#'+id+'_pager li:not(.disabled) a:not(.disabled)',
            _selector_info: '#'+id+'_info',
            _selector_thead: '#'+id+' thead',
            _selector_tbody: '#'+id+' tbody',
            _selector_alert_not_found: '[data-notfound='+id+']',
            _default_filter_key: '_search_',
            _managed_columns: [],
            _column_names: {},
        }, options);

        table.opts = opts; // link
        table.request = null; // current jqxhr
        table.fn = {}; // storage for functions

        opts.replace = true; // append or overwrite tbody

        $.each(opts.columns, function(i, col) {
            opts._column_names[col.name] = col;
            if (col.hidden) $(table).addClass('table-col-'+(i+1)+'-hidden');
        });

        /*** START FUNCTIONS ***/

        /* Delay for keyup in filters */
        table.fn.delay = (function(){

            var tid = 0;

            return function(callback, ms){
                clearTimeout(tid);
                tid = setTimeout(callback, ms);
            };

        })();

        /* Twitter bootstrap .pager as stack */
        table.fn._render_bs_stack = function(page, num_pages) {

            var p = opts._selector_pager, a = opts._selector_pager_links;

            if (page < num_pages) {
                $(a).data('page', (page+1));
                $(p).show();
            } else {
                $(a).data('page', '');
                $(p).hide();
            }
        };

        /* Twitter bootstrap .pager inner HTML */
        table.fn._render_bs_pager = function(page, num_pages, hide_prev) {

            var html = '', tp = opts.text_pager_prev, tn = opts.text_pager_next;

            if (page >1 && !hide_prev) {
                html += '<li><a href="#" data-page="'+(page-1)+'">'+tp+'</a></li>';
            } else {
                html += '<li class="disabled"><span>'+tp+'</span></li>';
            }

            if (page < num_pages) {
                html += '<li><a href="#" data-page="'+(page+1)+'">'+tn+'</a></li>';
            } else {
                html += '<li class="disabled"><span>'+tn+'</span></li>';
            }

            $(opts._selector_pager).html(html);

        };

        /* Twitter bootstrap .pagination inner HTML */
        table.fn._render_bs_pagination = function(page, num_pages, on_each_side, on_ends) {

            var html = '',
                on_each_side=on_each_side||3,
                on_ends=on_ends||2,
                dot='.',
                page_range = [],
                _push;

            if (page >1) {
                html += '<li><a href="#" data-page="'+(page-1)+'">'+opts.text_pager_prev+'</a></li>';
            } else {
                html += '<li class="disabled"><span>'+opts.text_pager_prev+'</span></li>';
            }

            _push = function(s, e) { for(var i=s; i<e; i++) { page_range.push(i) } };

            if (num_pages > 9) {

                if (page > (on_each_side + on_ends)) {
                    _push(1, on_each_side);
                    page_range.push(dot);
                    _push(page+1-on_each_side, page+1);
                } else {
                    _push(1, page+1)
                }

                if (page < (num_pages - on_each_side - on_ends + 1)) {
                    _push(page+1, page+on_each_side);
                    page_range.push(dot);
                    _push(num_pages-on_ends+1, num_pages+1);
                } else {
                    _push(page+1, num_pages+1)
                }
            } else {
                page_range = $.map($(Array(num_pages)), function(val, i) { return i+1; })
            };

            $.each(page_range, function(i, item) {

                if (item == dot) {
                    html += '<li class="disabled"><span>...</span></li>';
                } else if (item == page) {
                    html += '<li class="active"><span>'+page+'</span></li>';
                } else {
                    html += '<li><a href="#" data-page="'+item+'">'+item+'</a></li>';
                }

            });

            if (page < num_pages) {
                html += '<li><a href="#" data-page="'+(page+1)+'">'+opts.text_pager_next+'</a></li>';
            } else {
                html += '<li class="disabled"><span>'+opts.text_pager_next+'</span></li>';
            }

            $(opts._selector_pager).html(html);

        };

        /* Use default pagination */
        table.fn.render_pager = function(page, num_pages) {

            if (opts.table_type == 'stack') {
                return table.fn._render_bs_stack(page, num_pages)
            }
            else if (opts.table_type == 'pager') {
                return table.fn._render_bs_pager(page, num_pages, true)
            }

            return table.fn._render_bs_pagination(page, num_pages);

        }

        /* Show/hide not found text */
        table.fn.alert_not_found = function(show) {

            var $alert = $(opts._selector_alert_not_found);

            show ? $alert.show() : $alert.hide();
        };

        /* Rendering information */
        table.fn.render_info = function(html) {
            $(opts._selector_info).html(html);
        };

        /* Rendering settings */
        table.fn.render_settings = function() {

            var html = '';

            $.each(opts.columns, function(i, col) {

                if (!col.notmanaged) {
                    html += '<label>'
                         +'<input type="checkbox" name="'+id+'_colswitcher" value="'+(i+1)+'" '
                         +(!col.hidden ? ' checked' : '')+'/>'
                         +(col.title||col.name)
                         +'</label>'
                }

            });

            html += '<div class="btn-group" data-toggle="buttons">'

            $.each(opts.limit_list, function(i, limit) {

                html += '<label class="btn'+(opts.limit == limit ? ' active': '')+'">'
                        +'<input type="checkbox" name="'+id+'_limit" '
                        +(opts.limit == limit ? ' checked': '')+'>'
                        + limit
                        +'</label>'

            });

            html += '</div>'

            $(opts._selector_settings).html(html);

        };

        /* Returns class for <tr> */
        table.fn.get_class_tr = function(object) { return object ? '' : 'danger' };

        /* Rendering one object */
        table.fn.render_object = function(index, object) {

            if (object == null) return;

            var html = '';

            html += '<tr class="'+table.fn.get_class_tr(object)+'">';

            $.each(opts.columns, function(i, col) {

                html += '<td>'+object[col.name]+'</td>';

            });

            html += '</tr>';

            $(opts._selector_tbody).append(html);

        };

        /* Callback of jqxhr. Rendering all objects, pagination, etc. */
        table.fn.render = function(json, replace) {

            var data = json.data;

            if (replace) $(opts._selector_tbody).html('');

            if ($.isEmptyObject(data.objects)) {
                table.fn.alert_not_found(true)
            } else {
                table.fn.alert_not_found(false)
                $.each(data.objects, function(i, item) {
                    table.fn.render_object(i, item)
                })
            }

            table.fn.render_pager(data.page, data.num_pages);

            if (data.info) table.fn.render_info(data.info);

        };

        /* Request to server on quickAPI. Returns jqxhr. */
        table.fn.get = function(filters) {

            var replace = opts['replace'], F = filters || {};

            if (table.request) table.request.abort();

            table.request = $.quickAPI({
                url: opts.url,
                timeout: opts.timeout,
                //type: 'POST',
                async: opts.async,
                args: {
                    method: opts.method,
                    kwargs: {
                        filters: $.extend({}, opts.filters, F),
                        ordering: opts.ordering,
                        page: opts.page,
                        limit: opts.limit,
                    },
                },
                callback: function(json, status, xhr) { return table.fn.render(json, replace) },
                handlerShowAlert: opts.handlerShowAlert,
            })
            .always(function() {table.request = null});

            return table.request

        };

        /* Request to server from first page by force. */
        table.fn.get_first_page = function(filters) {

            opts.page = 1;
            opts.replace = true;

            return table.fn.get(filters);

        };

        /*** END FUNCTIONS ***/

        /*** START BINDING TABLE CONTROLLERS ON DOCUMENT BODY ***/

        $('body')

        /* Keyup on character filters */
        .off('keyup', opts._selector_filtering+':not(input[type=checkbox])')
        .on('keyup', opts._selector_filtering+':not(input[type=checkbox])', function(e) {

            var fname = this.name || opts._default_filter_key,
                old = opts.filters[fname],
                min = Number($(this).data('minimum')) || 0, // minimum chars for query
                len = this.value.length;

            if (this.value != old && (!len || len >= min)) {

                opts.filters[fname] = this.value;
                table.fn.delay(table.fn.get_first_page, opts.delay);

            }

        })

        /* change on boolean filters */
        .off('change', opts._selector_filtering+'[type=checkbox]')
        .on('change', opts._selector_filtering+'[type=checkbox]', function(e) {

            var fname = this.name;

            if (fname && this.checked != opts.filters[fname]) {

                opts.filters[fname] = this.checked;
                table.fn.delay(table.fn.get_first_page, 0);

            }

        })

        /* Change limit on page */
        .off('change', opts._selector_limiting)
        .on('change', opts._selector_limiting, function(e) {

            opts.limit = this.value;
            table.fn.get_first_page();

        })

        /* Change visible of column */
        .off('change', opts._selector_colswitcher)
        .on('change', opts._selector_colswitcher, function(e) {

            var n = this.value,
                cls = 'table-col-'+n+'-hidden';

            if (!n) return;

            if (this.checked) {
                $(table).removeClass(cls);
                opts.columns[n-1].hidden = false;
            } else {
                $(table).addClass(cls);
                opts.columns[n-1].hidden = true;
            }

        })

        /* Change ordering on columns */
        .off('click', opts._selector_ordering)
        .on('click', opts._selector_ordering, function(e) {

            var column = $(this).attr('name'), L, i;
            
            if (!column) return;

            L = opts.ordering;
            i = $.inArray(column, L);

            if (!opts.multiordering) {
                $(opts._selector_ordering).removeClass('sorting-asc')
                                             .removeClass('sorting-desc')
                                             .addClass('sorting');
            }

            if (i > -1) {
                //~ console.debug('exists', i, column);
                if (!opts.multiordering) {
                    L = ['-'+column];
                } else {
                    L[i] = '-'+column;
                }

                $(this).removeClass('sorting').addClass('sorting-desc');
            } else {
                //~ console.debug('not exists', i, column);
                i = $.inArray('-'+column, L);
                if (i > -1) {
                    //~ console.debug('remove', i, '-'+column);
                    if (!opts.multiordering) {
                        L = [];
                    } else {
                        L = L.slice(0,i).concat(L.slice(i+1));
                    }

                    $(this).removeClass('sorting-desc').addClass('sorting');
                }
            }

            if (i == -1){
                //~ console.debug('not exists', i, '-'+column);
                if (!opts.multiordering) {
                    L = [column];
                } else {
                    L.push(column);
                }

                $(this).removeClass('sorting').addClass('sorting-asc');
            }

            opts.ordering = L;

            table.fn.get_first_page();

        })

        /* Click on pagination */
        .off('click', opts._selector_pager_links)
        .on('click', opts._selector_pager_links, function(e) {

            e.preventDefault();
            opts.page = $(this).data('page');
            if (opts.table_type == 'stack') { opts.replace = false };
            table.fn.get();

        });

        /*** END BINDING TABLE CONTROLLERS ***/

        /* Starting table */
        if (opts.autorender_settings) table.fn.render_settings();
        if (opts.autoload) table.fn.get_first_page();
 
        return table;
 
    };

}(jQuery));


