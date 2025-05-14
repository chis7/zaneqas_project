/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { EmployeeDocumentKanbanRecord } from "@employee/js/employee_document_kanban/employee_document_kanban_record";
import { FileUploadProgressContainer } from "@web/core/file_upload/file_upload_progress_container";
import { FileUploadProgressKanbanRecord } from "@web/core/file_upload/file_upload_progress_record";

export class EmployeeDocumentKanbanRenderer extends KanbanRenderer {
    setup() {
        super.setup();
        this.fileUploadService = useService("file_upload");
    }
}

EmployeeDocumentKanbanRenderer.components = {
    ...KanbanRenderer.components,
    FileUploadProgressContainer,
    FileUploadProgressKanbanRecord,
    KanbanRecord: EmployeeDocumentKanbanRecord,
};
EmployeeDocumentKanbanRenderer.template = "employee.EmployeeDocumentKanbanRenderer";
