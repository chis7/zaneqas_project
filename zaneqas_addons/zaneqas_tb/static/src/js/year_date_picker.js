// zaneqas_addons/zaneqas_tb/static/src/js/year_date_picker.js

odoo.define('zaneqas_tb.year_date_picker', function (require) {
    "use strict";

    var fieldRegistry = require('web.field_registry');
    var FieldDate = require('web.basic_fields').FieldDate;

    var YearDatePicker = FieldDate.extend({
        _render: function () {
            this._super.apply(this, arguments);
            this.$input.datepicker('option', 'dateFormat', 'yy');
            this.$input.datepicker('option', 'changeYear', true);
            this.$input.datepicker('option', 'showButtonPanel', true);
            this.$input.datepicker('option', 'onClose', function (dateText, inst) {
                var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
                $(this).datepicker('setDate', new Date(year, 1));
            });
        },
    });

    fieldRegistry.add('year_date_picker', YearDatePicker);
});