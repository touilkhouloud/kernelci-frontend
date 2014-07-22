# Copyright (C) 2014 Linaro Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import (
    abort,
    render_template,
)

from flask.views import View

from dashboard.utils.backend import (
    extract_response_metadata,
    get_job,
    today_date,
)

PAGE_TITLE = 'Kernel CI Dashboard &mdash; Boot Reports'


class BootsView(View):

    def dispatch_request(self):

        results_title = 'Available Boot Reports'

        return render_template(
            'boots.html',
            page_title=PAGE_TITLE,
            server_date=today_date(),
            results_title=results_title
        )


class BootIdView(View):

    def dispatch_request(self, **kwargs):

        page_title = PAGE_TITLE + '&nbsp;&dash;Board&nbsp;%(board)s' % kwargs
        body_title = 'Details for board&nbsp;%(board)s' % kwargs

        return render_template(
            'boot.html',
            page_title=page_title,
            body_title=body_title,
            board=kwargs['board'],
            job=kwargs['job'],
            kernel=kwargs['kernel'],
            defconfig=kwargs['defconfig'],
        )


class BootJobKernelView(View):

    def dispatch_request(self, **kwargs):

        job = kwargs['job']
        kernel = kwargs['kernel']
        job_id = '%s-%s' % (job, kernel)
        storage_id = 'boot-' + job_id

        body_title = body_title = 'Details for&nbsp;%s&nbsp;&dash;&nbsp;%s' % (
            job, kernel
        )

        params = {'id': job_id}
        response = get_job(**params)

        metadata = {}
        base_url = ''
        commit_url = ''

        if response.status_code == 200:
            metadata, base_url, commit_url, result = extract_response_metadata(
                response
            )

            return render_template(
                'boots-job-kernel.html',
                page_title=PAGE_TITLE,
                body_title=body_title,
                base_url=base_url,
                commit_url=commit_url,
                job_id=job_id,
                job=job,
                kernel=kernel,
                metadata=metadata,
                storage_id=storage_id,
            )
        else:
            abort(response.status_code)
