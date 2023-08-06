import os
import json
import shutil
import pkgutil
from distutils.spawn import find_executable

import jinja2

from .. import utils
from ..exceptions import ServError


class Base(object):
    def __init__(self, logger=None, **params):
        """Provide defaults for all other subclasses.

        This should always be supered.

        `self.logger` is the default logger.
        `self.params` are all parameters for the service passed from the
         CLI or the API.

        `self.init_system` is the name of the init system (e.g. systemd).
        `self.cmd` is the command to run.
        `self.name` is the name of the service.
        """
        self.logger = logger
        self.params = params

        self.init_system = params.get('init_sys')
        self.cmd = params.get('cmd')
        self.name = params.get('name')
        self._set_default_parameter_values()

        self._validate_service_params()

    def _set_default_parameter_values(self):
        params = self.params
        params['description'] = params.get(
            'description', 'no description given')
        params['chdir'] = params.get('chdir', '/')
        params['chroot'] = params.get('chroot', '/')
        params['user'] = params.get('user', 'root')
        params['group'] = params.get('group', 'root')

    def _validate_service_params(self):
        niceness = self.params.get('nice')
        if niceness is not None and (niceness < -20 or niceness > 19):
            raise ServError('`niceness` level must be between -20 and 19')

        limit_params = [
            'limit_coredump',
            'limit_cputime',
            'limit_data',
            'limit_file_size',
            'limit_locked_memory',
            'limit_open_files',
            'limit_user_processes',
            'limit_physical_memory',
            'limit_stack_size',
        ]

        def _raise_limit_error(limit_type, limit):
            raise ServError(
                'All limits must be integers greater than 0 or ulimited. '
                'You provided a {0} with value {1}'.format(limit_type, limit))

        for limit_type in limit_params:
            limit = self.params.get(limit_type)
            if limit not in (None, 'ulimited'):
                try:
                    value = int(limit)
                except (ValueError, TypeError):
                    _raise_limit_error(limit_type, limit)
                if value < 1:
                    _raise_limit_error(limit_type, limit)

    def generate(self, overwrite):
        """Generate service files.

        This exposes several comforts.

        `self.files` is a list into which all generated file paths will be
        appended. It is later returned by `generate` to be consumed by any
        program that wants to do something with it.

        `self.templates` is the directory in which all templates are
        stored. New init system implementations can use this to easily
        pull template files.

        `self.template_prefix` is a prefix for all template files.
        Since all template files should be named
        `<INIT_SYS_NAME>*`, this will basically just
        provide the prefix before the * for you to use.

        `self.generate_into_prefix` is a prefix for the path into which
        files will be generated. This is NOT the destination path for the
        file when deploying the service.

        `self.overwrite` automatically deals with overwriting files so that
        the developer doesn't have to address this. It is provided by the API
        or by the CLI and propagated.
        """
        self.files = []
        tmp = utils.get_tmp_dir(self.init_system, self.name)
        self.templates = os.path.join(os.path.dirname(__file__), 'templates')
        self.template_prefix = self.init_system
        self.generate_into_prefix = os.path.join(tmp, self.name)
        self.overwrite = overwrite

    def install(self):
        """Install a service on the local machine.

        This is relevant for init systems like systemd where you have to
        `sudo systemctl enable #SERVICE#` before starting a service.

        When trying to install a service, if the executable for the command
        is not found, this will fail miserably.
        """
        if not find_executable(self.cmd):
            raise ServError('Executable {0} could not be found'.format(
                self.cmd))

    def start(self):
        """Start a service.
        """

    def stop(self):
        """Stop a service.
        """

    def uninstall(self):
        """Uninstall a service.

        This should include any cleanups required.
        """
        # raise NotImplementedError('Must be implemented by a subclass')

    def status(self, **kwargs):
        """Retrieve the status of a service `name` or all services
        for the current init system.
        """
        self.services = dict(
            init_system=self.init_system,
            services=[]
        )

    def is_system_exists(self):
        """Return True if the init system exists on the current machine
        or False if it doesn't.
        """

    def is_service_exists(self):
        """Return True if the service is installed on the current machine
        and False if it isn't.
        """

    def validate_platform(self):
        """Validate that the platform the user is trying to install the
        service on is valid.
        """

    def generate_file_from_template(self, template, destination):
        """Generate a file from a Jinja2 `template` and writes it to
        `destination` using `params`.

        `overwrite` allows to overwrite existing files. It is passed to
        the `generate` method.

        This is used by the different init implementations to generate
        init scripts/configs and deploy them to the relevant directories.
        Templates are looked up under init/templates/`template`.

        If the `destination` directory doesn't exist, it will alert
        the user and exit. We don't want to be creating any system
        related directories out of the blue. The exception to the rule is
        with nssm.
        While it may seem a bit weird, not all relevant directories exist
        out of the box. For instance, `/etc/sysconfig` doesn't necessarily
        exist even if systemd is used by default.
        """
        # We cast the object to a string before passing it on as py3.x
        # will fail on Jinja2 if there are ints/bytes (not strings) in the
        # template which will not allow `env.from_string(template)` to
        # take place.
        templates = str(pkgutil.get_data(__name__, os.path.join(
            'templates', template)))

        pretty_params = json.dumps(self.params, indent=4, sort_keys=True)
        self.logger.debug(
            'Rendering %s with params: %s...', template, pretty_params)
        generated = jinja2.Environment().from_string(
            templates).render(self.params)
        self.logger.debug('Writing generated file to %s...', destination)
        self._should_overwrite(destination)
        with open(destination, 'w') as f:
            f.write(generated)
        self.files.append(destination)

    def _should_overwrite(self, destination):
        # TODO: this should probably move to serv.py and check for overwriting
        # on service creation/installation.
        if os.path.isfile(destination):
            if self.overwrite:
                self.logger.debug('Overwriting: %s', destination)
            else:
                raise ServError('File already exists: {0}'.format(
                    destination))

    def _handle_service_directory(self, init_system_file, create_directory):
        dirname = os.path.dirname(init_system_file)
        if not os.path.isdir(dirname):
            if create_directory:
                self.logger.debug('Creating directory %s...', dirname)
                os.makedirs(dirname)
            else:
                raise ServError(
                    'Directory {0} does not exist and is required for {1}. '
                    'Terminating...'.format(dirname, init_system_file))

    def deploy_service_file(self, source, destination, create_directory=False):
        self._should_overwrite(destination)
        self._handle_service_directory(destination, create_directory)
        self.logger.info('Deploying %s to %s...', source, destination)
        shutil.move(source, destination)
