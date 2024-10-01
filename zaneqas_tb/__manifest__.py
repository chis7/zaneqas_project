# -*- coding: utf-8 -*-
##############################################################################
#
#    Ministry of Health GRZ
#    Copyright (C) 2024-TODAY Ministry of Health GRZ(<https://www.moh.gov.zm>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "ZANEQAS TB",
    'version': '17.0.1.0',
    'license': 'LGPL-3',
    'category': 'ZANEQAS',
    "sequence": 2,
    'summary': """ZANEQAS TB Module""",
    'description': """ZANEQAS Module for managing TB EQA Schemes""",
    'complexity': "easy",
    'author': 'Ministry of Health',
    'website': 'https://www.moh.gov.zm',
    'depends': [
        'base',
        'mail',
        'hr',
        'board',
    ],
    'data': [
        'security/training_security.xml',
        'security/ir.model.access.csv',
        # 'data/data.xml',
        'views/zaneqas_web_page_title.xml',
        'wizard/createTrainingPlanView.xml',
        'views/training_plan_views.xml',
        'views/training_type_views.xml',
        'views/study_field_views.xml',
        'views/course_evaluation_views.xml',
        'views/study_application_views.xml',
        'views/course_evaluation_views.xml',
        'views/post_training_evaluation.xml',
        'views/supervisors_post_training_evaluation.xml',
        'views/zaneqas_tb_xpert_eqa_results_views.xml',
        'views/zaneqas_tb_xpert_eqa_expected_results_views.xml',
        'views/zaneqas_tb_xpert_eqa_config_rounds_views.xml',
        'views/zaneqas_tb_xpert_eqa_config_assays_views.xml',
        'views/zaneqas_tb_actions.xml',
        'views/zaneqas_tb_menus.xml',
        'report/zaneqas_tb_xpert_eqa_results_report.xml',
        'report/gene_xpert_eqa_results_template.xml',
        # 'static/description/icon.svg',

    ],
    'assets': {
        'web.assets_backend': [
            'zaneqas_tb/static/description/icon.svg',
        ],
    },

    'demo': [],
    'images': [],
    'installable': True,
    'application': True,
}
