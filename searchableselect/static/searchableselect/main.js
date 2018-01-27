(function() {
    var $ = jQuery.noConflict(true);
    // https://github.com/ariya/phantomjs/issues/10522
    if (!Function.prototype.bind) {
        Function.prototype.bind = function(oThis) {
            if (typeof this !== 'function') {
                // closest thing possible to the ECMAScript 5
                // internal IsCallable function
                throw new TypeError('Function.prototype.bind - what is trying to be bound is not callable');
            }

            var aArgs = Array.prototype.slice.call(arguments, 1),
                fToBind = this,
                fNOP = function() {},
                fBound = function() {
                    return fToBind.apply(this instanceof fNOP ?
                        this :
                        oThis,
                        aArgs.concat(Array.prototype.slice.call(arguments)));
                };

            if (this.prototype) {
                // Function.prototype doesn't have a prototype property
                fNOP.prototype = this.prototype;
            }
            fBound.prototype = new fNOP();

            return fBound;
        };
    }

    $(window).ready(function() {
        $.fn.completion = function (opts) {
            if (!opts.url) {
                console.log('Completion error: url not specified.');
                return;
            }
            if (!opts.onSelect) {
                console.log('Completion error: onSelect not specified.');
                return;
            }

            var $element = $(this);

            var objects = new Bloodhound({
                datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
                queryTokenizer: Bloodhound.tokenizers.whitespace,
                limit: Infinity,
                remote: {
                    url: opts.url,
                    replace: function (url, q) {
                        var $menu = $element.parent().find('.tt-menu');
                        $menu.find('.tt-dataset').html('<div class="tt-nothing-found">Loading</div>');
                        return url + encodeURIComponent(q);
                    },
                    wildcard: '%QUERY',
                    transform: function (data) {
                        if (opts.spinner) {
                            opts.spinner.addClass('a-hidden');
                        }
                        return data.result;
                    }
                }
            });

            objects.initialize();

            $element.typeahead(null, {
                name: 'objects',
                source: objects.ttAdapter(),
                displayKey: 'matched_name',
                limit: Infinity,
                templates: {
                    loading: '<div class="tt-nothing-found">Loading</div>',
                    empty: '<div class="tt-nothing-found">Nothing found</div>',
                    suggestion: function (item) {
                        var $tpl = $('<div/>');
                        $tpl.html(item.name);
                        return $tpl.get(0);
                    }
                }
            }).on('typeahead:selected', (function (e, data) {
                opts.onSelect(data);
            }).bind(this)).on('input', function () {
            }).on('keypress', (function (e) {
                if (e.which == 13) {
                    opts.onEnter && opts.onEnter.call(this);
                }
            }).bind(this));
        };

        $('.searchable-select').each(function() {
            var $select = $(this);
            $select.closest('.form-row').addClass('form-row-no-overflows');
            (function($select) {
                var $chips = $('#' + $select.attr('id') + '-chips');

                $chips.on('click', '.chip', function() {
                    var $this = $(this);
                    $this.addClass('minimized');

                    window.setTimeout(function() {
                        $this.remove();
                    }, 200);
                });

                $select.completion({
                    url: $select.attr('data-url') + '?model=' + $select.attr('data-model') + '&search_field=' + $select.attr('data-search-field') + '&limit=' + $select.attr('data-limit') + '&q=',
                    onSelect: function (data) {
                        var $chip = $('<div/>').addClass('chip minimized').html(data.name).append(
                            $('<input/>').attr('type', 'hidden').attr('name', $select.attr('data-name')).attr('value', data.pk)
                        );
                        if($select.attr('data-many') == '1') {
                            $chips.append($chip);
                        } else {
                            $chips.html($chip);
                        }
                        $select.typeahead('val', '');
                        window.setTimeout(function () {
                            $chip.removeClass('minimized');
                        }, 0);
                    },
                    onEnter: function () {
                        $(this).parent().find('.tt-dataset .tt-suggestion.tt-selectable').first().trigger('click');
                    }
                });
            })($select);
        });
    });
})();
