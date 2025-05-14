
import { registry } from "@web/core/registry";

import { kanbanView } from "@web/views/kanban/kanban_view";
import { EmployeeDocumentKanbanController } from "@employee/js/employee_document_kanban/employee_document_kanban_controller";
import { EmployeeDocumentKanbanRenderer } from "@employee/js/employee_document_kanban/employee_document_kanban_renderer";

export const employeeDocumentKanbanView = {
    ...kanbanView,
    Controller: EmployeeDocumentKanbanController,
    Renderer: EmployeeDocumentKanbanRenderer,
    buttonTemplate: "employee.EmployeeDocumentKanbanView.Buttons",
};

registry.category("views").add("employee_documents_kanban", employeeDocumentKanbanView);
