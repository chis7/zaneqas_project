/** @odoo-module **/

import { registry } from "@web/core/registry";
import { BinaryField, binaryField } from "@web/views/fields/binary/binary_field";

export class LicenseUploadField extends BinaryField {}
LicenseUploadField.template = "hrms_core.LicenseUploadField";

export const licenseUploadField = {
    ...binaryField,
    component: LicenseUploadField,
};

registry.category("fields").add("license_upload", licenseUploadField);
