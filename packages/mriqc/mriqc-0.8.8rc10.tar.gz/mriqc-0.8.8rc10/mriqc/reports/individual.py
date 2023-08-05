#!/usr/bin/env python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
# pylint: disable=no-member
#
# @Author: oesteban
# @Date:   2016-01-05 11:33:39
# @Email:  code@oscaresteban.es
# @Last modified by:   oesteban
""" Encapsulates report generation functions """
from __future__ import print_function, division, absolute_import, unicode_literals

def individual_html(in_iqms, exclude_index=0, in_plots=None,
                    wf_details=None):
    import os.path as op  #pylint: disable=W0404
    import datetime
    import re
    from json import load
    from mriqc import __version__ as ver
    from mriqc.reports.utils import iqms2html
    from mriqc.data import IndividualTemplate
    from mriqc import logging
    from io import open  #pylint: disable=W0622
    MRIQC_REPORT_LOG = logging.getLogger('mriqc.report')
    MRIQC_REPORT_LOG.setLevel(logging.INFO)

    with open(in_iqms) as f:
        iqms_dict = load(f)

    if in_plots is None:
        in_plots = []

    if wf_details is None:
        wf_details = []

    svg_files = []
    for pfile in in_plots:
        with open(pfile) as f:
            svg_content_lines = f.read().split('\n')
            svg_lines_corrected = []
            for line in svg_content_lines:
                if "<svg " in line:
                    line = re.sub(' height="[0-9.]+[a-z]*"', '', line)
                    line = re.sub(' width="[0-9.]+[a-z]*"', '', line)
                svg_lines_corrected.append(line)

            svg_files.append('\n'.join(svg_lines_corrected))

    sub_id = iqms_dict.pop('subject_id')
    ses_id = iqms_dict.pop('session_id')
    run_id = iqms_dict.pop('run_id')
    qctype = iqms_dict.pop('qc_type')
    if qctype == 'anat':
        qctype = 'anatomical'
        msk_vals = []
        for k in ['snr_d_csf', 'snr_d_gm', 'snr_d_wm', 'fber']:
            elements = k.split('_')
            iqm = iqms_dict[elements[0]]
            if len(elements) == 1:
                msk_vals.append(iqm < 0.)
            else:
                msk_vals.append(iqm['_'.join(elements[1:])] < 0.)

        if any(msk_vals):
            wf_details.append('Noise variance in the background is very low')
            if all(msk_vals):
                wf_details[-1] += (' for all measures: <span class="problematic">'
                                   'the original file could be masked</span>.')
            else:
                wf_details[-1] += '.'

    if qctype == 'func':
        qctype = 'functional'

    out_file = op.abspath('{}_sub-{}_ses-{}_run-{}_report.html'.format(
        qctype, sub_id[4:] if sub_id.startswith('sub-') else sub_id,
        ses_id, run_id))

    tpl = IndividualTemplate()
    tpl.generate_conf({
            'qctype': qctype,
            'sub_id': sub_id,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d, %H:%M"),
            'version': ver,
            'imparams': iqms2html(iqms_dict),
            'svg_files': svg_files,
            'exclude_index': exclude_index,
            'workflow_details': wf_details
        }, out_file)

    MRIQC_REPORT_LOG.info('Generated individual log (%s)', out_file)
    return out_file
