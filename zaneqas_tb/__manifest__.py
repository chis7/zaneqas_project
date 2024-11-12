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
        'wizard/zaneqas_tb_xpert_results_wizard_views.xml',
        'views/zaneqas_tb_xpert_eqa_results_views.xml',
        'views/zaneqas_tb_xpert_eqa_cycles_views.xml',
        'views/zaneqas_tb_xpert_eqa_expected_results_views.xml',
        'views/zaneqas_tb_xpert_eqa_participant_submission_views.xml',
        'views/zaneqas_tb_xpert_eqa_config_rounds_views.xml',
        'views/zaneqas_tb_xpert_eqa_config_assays_views.xml',
        'views/zaneqas_tb_actions.xml',
        'views/zaneqas_tb_menus.xml',
        'report/zaneqas_tb_xpert_eqa_results_report.xml',
        'report/gene_xpert_eqa_results_template.xml',

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
