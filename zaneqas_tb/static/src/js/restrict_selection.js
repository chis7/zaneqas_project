odoo.define('zaneqas_tb.async_validation', function (require) {
    "use strict";

    console.log('async_validation.js loaded');
    var FormRenderer = require('web.FormRenderer');
    var rpc = require('web.rpc');

    FormRenderer.include({
        _onFieldChanged: function (event) {
            this._super.apply(this, arguments);
            var fieldName = event.data.changes;
            var tbDetectionFields = [
                'tb_detection_not_detected',
                'tb_detection_trace',
                'tb_detection_very_low',
                'tb_detection_low',
                'tb_detection_medium',
                'tb_detection_high'
            ];

            if (tbDetectionFields.includes(fieldName)) {
                var fieldValue = this.state.data[fieldName];
                rpc.query({
                    model: 'zaneqas.tb.xpert.eqa.result',
                    method: 'check_field_value',
                    args: [fieldName, fieldValue],
                }).then(function (result) {
                    if (!result.isValid) {
                        this.do_warn('Validation Error', result.message);
                        this.state.data[fieldName] = null; // Reset the field value
                        this.render();
                    }
                }.bind(this));
            }
        }
    });
});