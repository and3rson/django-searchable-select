(function() {
    var $ = jQuery.noConflict(true);

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
                templates: {
                    loading: '<div class="tt-nothing-found">Loading</div>',
                    empty: '<div class="tt-nothing-found">Nothing found</div>',
                    suggestion: function (item) {
                        var $tpl = $('<div/>');
                        $tpl.html(item.name);
                        return $tpl.get(0);
                    }
                }
            }).on('typeahead:selected', function (e, data) {
                opts.onSelect(data);
            }.bind(this)).on('input', function () {
            }).on('keypress', function (e) {
                if (e.which == 13) {
                    opts.onEnter && opts.onEnter.call(this);
                }
            }.bind(this));
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
                    url: $select.attr('data-url') + '?model=' + $select.attr('data-model') + '&search_field=' + $select.attr('data-search-field') + '&q=',
                    onSelect: function (data) {
                        var $chip = $('<div/>').addClass('chip minimized').html(data.name).append(
                            $('<input/>').attr('type', 'hidden').attr('name', $select.attr('data-name')).attr('value', data.pk)
                        );
                        $chips.append($chip);
                        console.log($chips);
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
